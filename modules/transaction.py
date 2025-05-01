import random
import datetime as dt
from .utils import cursor, db


class Transaction:
    def __init__(self, sender_name, receiver_name, amount, remark, type_string):
        self.sender_name = sender_name
        self.receiver_name = receiver_name
        self.amount = amount
        self.remark = remark
        self.type_string = type_string

        sql = "SELECT * FROM USER WHERE username = %s"
        values = (self.sender_name, )
        cursor.execute(sql, values)
        data = cursor.fetchall()
        self.sender_id = data[0][0] if len(data) > 0 else None

        sql = "SELECT * FROM USER WHERE username = %s"
        values = (self.receiver_name, )
        cursor.execute(sql, values)
        data = cursor.fetchall()
        self.receiver_id = data[0][0] if len(data) > 0 else None

    def execute(self):
        try:
            sql = "UPDATE User SET amount = amount - %s WHERE username = %s"
            values = (self.amount, self.sender_name)
            cursor.execute(sql, values)
            db.commit()

            sql = "UPDATE User SET amount = amount + %s WHERE username = %s"
            values = (self.amount, self.receiver_name)
            cursor.execute(sql, values)
            db.commit()

            print("Transaction completed successfully.\n")
        except:
            print("Transaction failed. Please try again later.\n")

    def record(self):
        sql = ("INSERT INTO transaction(timestamp, sender, receiver, remark, amount, type)"
               "VALUES (%s, %s, %s, %s, %s, %s)")
        values = (dt.datetime.now(), self.sender_id, self.receiver_id, self.remark, self.amount, self.type_string)
        cursor.execute(sql, values)
        db.commit()

