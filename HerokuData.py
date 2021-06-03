import os
from datetime import datetime

import psycopg2


class QueryTable:
    def __init__(self, table):
        self.table = table
        self.__DATABASE_URL = os.popen('heroku config:get DATABASE_URL -a gery-linebot').read()[:-1]
        self.conn = psycopg2.connect(self.__DATABASE_URL, sslmode='require')
        self.cursor = self.conn.cursor()


    def to_close(self):
        self.conn.commit()
        self.cursor.close()
        self.conn.close()

    def select(self):
        query = f'SELECT * FROM {self.table};'
        self.cursor.execute(query)
        rows = self.cursor.fetchall()

        self.conn.commit()
        return rows

    def select_board(self, board):
        query = f'SELECT * FROM {self.table} WHERE board = %s;'
        self.cursor.execute(query, (board, ))
        rows = self.cursor.fetchall()
        self.conn.commit()
        return rows 
    
    def select_push(self, board, push_number):
        query = f'SELECT * FROM {self.table} WHERE board = %s and push >= %s;'
        self.cursor.execute(query, (board, push_number))
        rows = self.cursor.fetchall()
        self.conn.commit()
        return rows 



    def select_date(self, date):
        query = f'SELECT * FROM {self.table} WHERE date = %s;'
        self.cursor.execute(query, (date, ))
        rows = self.cursor.fetchall()

        self.conn.commit()
        return rows


    def create(self):
        query = f"""CREATE TABLE {self.table}
            (board TEXT , post_aid TEXT UNIQUE, push INTEGER, date TEXT, title TEXT, website TEXT);
            """
        self.cursor.execute(query)
        self.to_close()
    

    def drop(self):
        query = f'DROP TABLE {self.table}'
        self.cursor.execute(query)
        self.to_close()
        

    def insert(self, records):
        query = f'INSERT INTO {self.table} (board, post_aid, push, date, title, website)\
            VALUES (%s, %s, %s, %s, %s, %s)'
        self.cursor.executemany(query, records)
        self.conn.commit()


    def upsert(self, records):
        query = f'INSERT INTO {self.table} (board, post_aid, push, date, title, website)\
            VALUES (%s, %s, %s, %s, %s, %s) ON CONFLICT (post_aid) \
            DO UPDATE SET push = EXCLUDED.push;'
        self.cursor.executemany(query, records)
        self.conn.commit()
    
    def delete_date(self, date):
        query = f'DELETE FROM {self.table} WHERE date = %s;'
        self.cursor.execute(query, (date, ))
        self.conn.commit()
    
    def delete_board(self, board):
        query = f'DELETE FROM {self.table} WHERE board = %s;'
        self.cursor.execute(query, (board, ))
        self.conn.commit()
    
    def add_column(self):
        query = f'ALTER TABLE {self.table} ADD COLUMN notified BOOLEAN;'
        self.cursor.execute(query)
        self.conn.commit()
    
    def delete_all(self):
        query = f'TRUNCATE TABLE {self.table};'
        self.cursor.execute(query)
        self.conn.commit()


