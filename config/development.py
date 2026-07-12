from . import DB_URL
from .default import Default, env_bool

class Development(Default):
    DEBUG = True
    TEMPLATES_AUTO_RELOAD = True

    SQLALCHEMY_DATABASE_URI = DB_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = env_bool("SQLALCHEMY_TRACK_MODIFICATIONS", False)