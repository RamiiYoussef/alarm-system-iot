#!/usr/bin/env python3
#Created By Rami Mohep

import datetime
import _thread
from core import config
import pymysql
    
class Database:

    def __init__(self):
        self.connection = pymysql.connect(config.server, config.username, config.password, config.database)
        self.cursor = self.connection.cursor()

    def insert(self, query):
        try:
            self.cursor.execute(query)
            self.connection.commit()
        except:
            self.connection.rollback()

    def query(self, query):
        cursor = self.connection.cursor( pymysql.cursors.DictCursor )
        cursor.execute(query)

        return cursor.fetchall()

    def __del__(self):
        self.connection.close()
   
def interactive(input,doorType):

    # Connect to database
    db = Database()

    # Door Type
    door = 1
    if doorType == 'glass':
        door = 2

    # Door Status
    status = 0
    if input == True:
        status = 1
        
    time = datetime.datetime.now()
    # Data Insert into the table
    query = """
        INSERT INTO door_log
        (`door_status`, `log_date`, `door_type_id`)
        VALUES
        ("%s","%s", "%s")
        """

    # db.query(query)
    db.insert(query % (status, time, door))
