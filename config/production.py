import os
from . import DB_URL
from .default import Default

class Production(Default):
    SQLALCHEMY_DATABASE_URI = DB_URL
    PRESERVE_CONTEXT_ON_EXCEPTION = False

    def __init__(self):
        if not self.SECRET_KEY:
            raise ValueError("CRITICAL: Cannot boot production without a strong SECRET_KEY set in the environment.")