import datetime as dt
from .user import User
from .utils import cursor, db
from tabulate import tabulate
from .transaction import Transaction

class Wallet:
    def __init__(self):
        self.user = None
        self.amount = None

    def simulate(self):
        self.user = User()
        while True:
                if not self.user.is_authenticated():
                    print('Welcome to Mero Wallet.\n'
                          '1. Register \
                           \n2. Login\n')

                    user_input = input("Choose option: ")

                    match int(user_input):
                        case 1:
                            self.user.register()
                        case 2:
                            self.user.login()
                            self.amount = self.user.amount
                else:
                    print('Action available: \
                           \n1. Money available \
                           \n2. View recent transaction statement \
                           \n3. Send money \
                           \n4. Verify KYC \
                           \n5. Load money \
                           \n6. Logout\n')

                    option = int(input('Choose option: '))

                    match option:
                        case 1:
                            self.show_amount()
                        case 2:
                            self.view_transaction()
                        case 3:
                            self.send_money()
                        case 4:
                            self.user.verify_kyc()
                        case 5:
                            self.add_money()
                        case 6:
                            self.user.logout()

    def show_amount(self):
        print(f"Amount available = Rs. {self.amount}\n")

    def view_transaction(self):
        sql = ('SELECT t.id, t.timestamp, u1.username AS sender, u2.username AS receiver, t.amount, t.type, t.amount, '
               't.remark FROM transaction t '
               'LEFT JOIN user u1 ON t.sender = u1.id '
               'LEFT JOIN user u2 ON t.receiver = u2.id '
               'WHERE u1.id = %s OR u2.id = %s')
        values = (self.user.user_id, self.user.user_id)
        cursor.execute(sql, values)

        data = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        print(tabulate(data, headers=columns, tablefmt="pretty"))
        print("")

    def send_money(self):
        sql = ("SELECT t.id, t.name, u.username FROM user u "
               "JOIN tier t ON u.tier_id = t.id")
        cursor.execute(sql)
        data = cursor.fetchall()

        usernames = [item[2] for item in data]
        tier_names = [item[1] for item in data]

        # Excluding yourself from the list
        index = usernames.index(self.user.username)
        usernames.pop(index)
        tier_names.pop(index)

        print("\nSend money to:")
        for index, (username, tier_name) in enumerate(zip(usernames, tier_names)):
            print(f"{index+1}. {username} - <{tier_name}>")
        print("")
        user_input = int(input("Choose option: ")) - 1
        amount = float(input("Enter the amount to send: "))
        remark = input("Enter remarks: ")

        if amount > self.amount:
            print("You don't have enough money.\n")
            return

        if self.user.tier_name == 'Unverified' and tier_names[user_input] != 'Unverified':
            print("\nYou can only send money to Unverified users.\n"
                  "Please verify your KYC as Agent or Enterprise first.\n")
        else:
            date = dt.datetime.now().date()
            sql = (f"SELECT SUM(t.amount) FROM "
                   f"(select timestamp, amount from transaction where DATE(timestamp) =  '{str(date)}' AND sender = "
                   f"{self.user.user_id}) AS t")
            cursor.execute(sql)

            data = cursor.fetchall()[0][0]
            today_total_amount = (data if data else 0) + amount
            if today_total_amount >= self.user.limit_amount:
                print(f"Your today's limit (Rs. {self.user.limit_amount}) exceeded.\n")
            else:
                transaction = Transaction(self.user.username, usernames[user_input], amount, remark, 'MONEY_TRANSFER')
                transaction.execute()
                transaction.record()

                self.amount -= amount

    def add_money(self):
        amount = float(input("Enter the amount: "))

        sql = ("UPDATE User SET amount = amount + %s"
               "WHERE username = %s")
        values = (amount, self.user.username)
        cursor.execute(sql, values)
        db.commit()

        transaction = Transaction(None, self.user.username, amount, None, 'MONEY_LOAD')
        transaction.execute()
        transaction.record()

        self.amount += amount

    def logout(self):
        self.user.authenticated = False