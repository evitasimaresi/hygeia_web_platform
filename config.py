import os

class Config:
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///site.db"
    SECRET_KEY = "key"
    SESSION_PERMANENT = False
    SESSION_TYPE = "filesystem"

    # Configuration settings for Bard API
    BARD_API_KEY = "####." #__Secure-1PSID
    # BARD_API_KEY = os.getenv("_BARD_API_KEY")
    BARD_HOST = "bard.google.com"
    BARD_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"
    BARD_CONTENT_TYPE = "application/x-www-form-urlencoded;charset=UTF-8"
    BARD_ORIGIN = "https://bard.google.com"
    BARD_REFERER = "https://bard.google.com/"