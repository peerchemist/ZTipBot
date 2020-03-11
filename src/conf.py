from os import environ

BOT_VERSION = "0.1"
DEPOSIT_CHECK_JOB = 60.0  # seconds

if environ.get("APP_ENV") == "docker":
    RPC_PORT = environ.get("RPC_PORT", "9904")
    RPC_USER = environ.get("RPC_USER", "rpc")
    RPC_PASSWORD = environ.get("RPC_PASSWORD", "pass")
    RPC_HOST = environ.get("RPC_HOST", "")
    BOT_ID = environ.get("BOT_ID", "")
    BOT_TOKEN = environ.get("BOT_TOKEN", "")
    DB_NAME = environ.get("DB_NAME", "/var/lib/tippbot/tippbot.db")

else:
    RPC_PORT = environ.get("RPC_PORT", "9904")
    RPC_USER = environ.get("RPC_USER", "rpc")
    RPC_PASSWORD = environ.get("RPC_PASSWORD", "pass")
    RPC_HOST = environ.get("RPC_HOST", "")
    BOT_ID = environ.get("BOT_ID", "")
    BOT_TOKEN = environ.get("BOT_TOKEN", "")
    DB_NAME = environ.get("DB_NAME", "tippbot.db")
