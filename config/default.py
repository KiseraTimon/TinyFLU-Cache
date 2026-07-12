import os
from datetime import timedelta

def env_bool(var_name: str, default: bool = False) -> bool:
    val = os.getenv(var_name)
    if val is None:
        return default
    return val.lower() in ("true", "1", "t", "yes")

class Default:
    DEBUG = False
    TESTING = False
    TEMPLATES_AUTO_RELOAD = False

    SECRET_KEY = os.getenv("SECRET_KEY")

    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    ITEMS_PER_PAGE = 20

    # Shared Base Database Engine Options
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_size": int(os.getenv("SQLALCHEMY_POOL_SIZE", 10)),
        "max_overflow": int(os.getenv("SQLALCHEMY_MAX_OVERFLOW", 20)),
        "pool_timeout": int(os.getenv("SQLALCHEMY_POOL_TIMEOUT", 20)),
        "pool_recycle": int(os.getenv("SQLALCHEMY_POOL_RECYCLE", 300)),
        "pool_pre_ping": env_bool("SQLALCHEMY_POOL_PRE_PING", True),
        "pool_use_lifo": env_bool("SQLALCHEMY_POOL_USE_LIFO", True),
        "echo_pool": env_bool("SQLALCHEMY_ECHO_POOL", False),
        "echo": env_bool("SQLALCHEMY_ECHO", False),
    }