import mysql.connector
from src.app.config.settings import DB_CONFIG

def get_connection():
    return mysql.connector.connect(**DB_CONFIG)