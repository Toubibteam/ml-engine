import os

MONGODB_URI = os.environ.get("MONGODB_URI", "mongodb://localhost/codes")
MONGODB_DB_NAME = os.environ.get("MONGODB_DB_NAME", "codes")
