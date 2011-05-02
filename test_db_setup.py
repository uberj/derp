import sqlite3
DATABASE = "/home/uberj/derp/db/channel_logs_db"
conn = sqlite3.connect(DATABASE)
cursor = conn.cursor()
