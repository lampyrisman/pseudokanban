import pathlib
import sqlite3
import time
from http.server import HTTPServer
from server import Server
import os
HOST_IP = '127.0.0.1'
PORT = 9980

if __name__ == '__main__':
    if not os.path.exists('sqlite3.db'):
        os.mknod('sqlite3.db')
        conn = sqlite3.connect('sqlite3.db')
        conn.execute('''CREATE TABLE TASKS
         (ID INTEGER PRIMARY KEY AUTOINCREMENT,
         TASK           CHAR(32)    NOT NULL,
         STATUS            INTEGER     NOT NULL,
         DESCRIPTION CHAR(254))''')

        conn.execute('''CREATE TABLE STATUSES
         (ID INTEGER PRIMARY KEY AUTOINCREMENT,
         STATUS_ID  INT NOT NULL,
         STATUS_NAME           CHAR(32)    NOT NULL,
         DESCRIPTION CHAR(254))''')

    httpd = HTTPServer((HOST_IP, PORT), Server)
    print(time.asctime(), 'Server UP - %s:%s' % (HOST_IP, PORT))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print(time.asctime(), 'Server DOWN - %s:%s' % (HOST_IP, PORT))
