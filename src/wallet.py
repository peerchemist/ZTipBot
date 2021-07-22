from bitcoinrpc.authproxy import AuthServiceProxy

from . import util
from . import db
import datetime
import logging
from .conf import (RPC_PORT,
                   RPC_USER,
                   RPC_PASSWORD,
                   RPC_HOST
)

logging.basicConfig(filename='bot.log', level=logging.INFO)

MIN_CONFIRMATIONS_FOR_DEPOSIT = 2
TOP_USERS_COUNT = 10

logger = logging.getLogger("bot-wallet")
# logger_rpc = util.get_logger('BitcoinRPC')


def connect():
    return AuthServiceProxy(f"http://{RPC_USER}:{RPC_PASSWORD}@{RPC_HOST}:{RPC_PORT}")


def create_or_fetch_user(user_id, user_name):
    logger.info('attempting to fetch user %s ...', user_id)
    user = db.get_user_by_id(user_id)
    if user is None:
        logger.info('user %s does not exist. creating new user ...', user_id)
        commands = [["getnewaddress", "tippbot", "bech32"]]
        rpc_connection = connect()
        result = rpc_connection.batch_(commands)
        address = result[0]
        user = db.create_user(user_id=user_id,
                              user_name=user_name,
                              wallet_address=address)
        logger.info('user %s created.', user_id)
        return user
    else:
        logger.info('user %s fetched.', user_id)
        return user


def get_balance(user_id: int) -> float:
    logger.info('getting balance for user %s', user_id)
    user = db.get_user_by_id(user_id)
    if user is None:
        logger.info('user %s does not exist.', user_id)
        return float(0)
    else:
        logger.info('balance for %s fetched successfully.', user_id)
        return float(user.balance)


def make_transaction_to_address(user, amount, address):
    if not check_balance(user_id, amount):
        raise util.TipBotException("insufficient_funds")

    rpc_connection = connect()

    txid = rpc_connection.sendtoaddress(address, round(amount, 6), "tippbot withdraw")

    logger.info('creating withdraw transaction (user: %s, amount: %.3f, address: %s, txid: %s)', user.user_id,
                amount, address, txid)
    if db.create_withdraw_transaction(txid, amount, user):
        logger.info('withdraw successful.')
        return txid
    else:
        raise util.TipBotException("error")


def get_top_users():
    return db.get_top_users(TOP_USERS_COUNT)


def make_transaction_to_user(user_id, amount, target_user_id, target_user_name):
    if check_balance(user_id, amount):
        target_user = create_or_fetch_user(target_user_id, target_user_name)
        user = db.get_user_by_id(user_id)
        if db.move_funds(user, amount, target_user):
            logger.info('tip successful. (from: %s, to: %s, amount: %.3f)', user_id, target_user.user_id, amount)
            return
        else:
            raise util.TipBotException("error")
    else:
        raise util.TipBotException("insufficient_funds")


def check_balance(user_id, claimed_amount):
    '''Returns True if the user has a sensible balance with at least as much as
    the claimed amount. Returns False, otherwise.
    '''
    logger.info('checking %s balance for %.3f', user_id, claimed_amount)
    balance = get_balance(user_id)

    if balance < 0.0:
        logger.info('check balance failed.')
        return False

    if claimed_amount > balance:
        logger.info('check balance failed.')
        return False

    logger.info('check balance passed.')
    return True


def parse_incoming_transactions():
    # logger.info('parsing incoming transactions ...')
    commands = [["listtransactions", '*', 100, 0]]
    rpc_connection = connect()
    result = rpc_connection.batch_(commands)
    return_results = []
    if len(result[0]) > 0:
        for transaction_rpc in result[0]:
            if transaction_rpc['category'] == 'receive':
                txid = transaction_rpc['txid']
                to_user = db.get_user_by_wallet_address(transaction_rpc['address'])
                amount = transaction_rpc['amount']
                tx_time = datetime.datetime.fromtimestamp(transaction_rpc['time'])
                raw_tx_rpc = str(transaction_rpc)
                confirmations = transaction_rpc['confirmations']
                status = db.get_transaction_status_by_txid(txid)
                # logger.debug('processing transaction -> status: %s, raw_tx: %s', status, raw_tx_rpc)
                if status == 'DOESNT_EXIST' and confirmations >= MIN_CONFIRMATIONS_FOR_DEPOSIT:
                    logger.info('new confirmed transaction received: %s', transaction_rpc)
                    if db.create_deposit_transaction(txid, amount, to_user, tx_time, raw_tx_rpc, 'CONFIRMED'):
                        if to_user is not None:
                            return_results.append([to_user.user_id, 'new_deposit_confirmed', amount])
                        logger.info('transaction processed successfully %s', transaction_rpc)
                    else:
                        logger.critical('could not make deposit transaction !')
                elif status == 'DOESNT_EXIST' and confirmations < MIN_CONFIRMATIONS_FOR_DEPOSIT:
                    logger.info('new unconfirmed transaction received: %s', transaction_rpc)
                    if db.create_deposit_transaction(txid, amount, to_user, tx_time, raw_tx_rpc, 'UNCONFIRMED'):
                        if to_user is not None:
                            return_results.append([to_user.user_id, 'new_deposit_unconfirmed', amount])
                        logger.info('transaction processed successfully %s', transaction_rpc)
                    else:
                        logger.critical('could not make deposit transaction !')
                elif status == 'UNCONFIRMED' and confirmations >= MIN_CONFIRMATIONS_FOR_DEPOSIT:
                    logger.info('transaction confirmed: %s', transaction_rpc)
                    if db.confirm_transaction(txid, raw_tx_rpc):
                        if to_user is not None:
                            return_results.append([to_user.user_id, 'deposit_confirmed', amount])
                        logger.info('transaction confirmed successfully %s', transaction_rpc)
                    else:
                        logger.critical('could not confirm transaction !')
    return return_results
