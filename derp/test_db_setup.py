import sqlite3
DATABASE = "db/channel_log"
conn = sqlite3.connect(DATABASE)
cursor = conn.cursor()
