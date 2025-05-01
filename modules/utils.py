import mysql.connector

db = mysql.connector.connect(
  host="localhost",
  user="root",
  password="mysqlkoID@1",
)

cursor = db.cursor()

# cursor.execute("CREATE DATABASE week_2")

cursor.execute("use week_2")

# if __name__ == '__main__':
    # cursor.execute("""CREATE TABLE Tier (
    #               id int auto_increment primary key,
    #               name varchar(255),
    #               limit_amount float,
    #               );""")
    #
    # cursor.execute("""insert into tier (name, limit_amount)
    #                 values ('Basic', 10000), ('Premium', 50000), ('Merchant', 100000)""")


    # cursor.execute("""CREATE TABLE User (
    #               id int auto_increment primary key,
    #               tier_id int,
    #               username varchar(255),
    #               password varchar(255),
    #               amount float,
    #               foreign key (tier_id) references Tier(id)
    #               );""")
    #
    #
    # cursor.execute('CREATE TABLE Transaction ('
    #               'id int auto_increment primary key,'
    #               'timestamp timestamp,'
    #               'type varchar(255),'
    #               'sender int,'
    #               'receiver int,'
    #
    #               'foreign key (sender) references User(id),'
    #               'foreign key (receiver) references User(id)'
    #               ');')
    #
    # db.commit()


