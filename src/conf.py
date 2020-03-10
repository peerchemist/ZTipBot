from os import environ

BOT_VERSION = "0.1"
DEPOSIT_CHECK_JOB = 60.0  # seconds

if environ.get('APP_ENV') == 'docker':
    RPC_PORT = environ.get('RPC_PORT', '9904')
    RPC_USER = environ.get('RPC_USER', 'user')
    RPC_PASSWORD = environ.get('RPC_PASSWORD', 'pass')

else:
    RPC_PORT = environ.get('RPC_PORT', '9904')
    RPC_USER = environ.get('RPC_USER', 'user')
    RPC_PASSWORD = environ.get('RPC_PASSWORD', 'pass')
