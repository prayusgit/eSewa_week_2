from .utils import cursor
from .utils import db
import time


class User:
    def __init__(self):
        self.user_id = None
        self.tier_id = None
        self.tier_name = None
        self.amount = None
        self.password = None
        self.username = None
        self.limit_amount = None
        self.authenticated = None

    def is_authenticated(self):
        return self.authenticated

    def register(self):
        username = input("Enter the username: ")
        password = input("Enter the password: ")

        cursor.execute('SELECT * FROM User')
        user_datas = cursor.fetchall()

        usernames = [item[-1] for item in user_datas]

        if username in usernames:
            print("User already exist try another name.\n")
        else:
            sql = "INSERT INTO User (tier_id, amount, password, username) VALUES (%s, %s, %s, %s)"
            values = (1, 0, password, username)
            cursor.execute(sql, values)
            db.commit()

            print('Successfully registered.\n')

    def login(self):
        username = input("Enter the username: ")
        password = input("Enter the password: ")

        cursor.execute('SELECT u.username, u.id, u.password, u.amount, t.name, t.id, t.limit_amount FROM User u '
                       'JOIN tier t on u.tier_id = t.id')
        user_datas = cursor.fetchall()

        usernames = [item[0] for item in user_datas]
        user_ids = [item[1] for item in user_datas]
        passwords = [item[2] for item in user_datas]
        amounts = [item[3] for item in user_datas]
        tier_names = [item[4] for item in user_datas]
        tier_ids = [item[5] for item in user_datas]
        limit_amounts = [item[6] for item in user_datas]

        index = usernames.index(username)

        if (username in usernames) and (passwords[index] == password):
            self.username = username
            self.password = password
            self.user_id = user_ids[index]
            self.tier_name = tier_names[index]
            self.tier_id = tier_ids[index]
            self.amount = amounts[index]
            self.limit_amount = limit_amounts[index]
            self.authenticated = True

            print(f'Welcome {self.username}.\n')
        else:
            print("Username or password doesn't match. Do register.\n")

    def verify_kyc(self):
        if self.tier_name == 'Unverified':
            print("Select the type of account required:\n"
                  "1. Agent\n"
                  "2. Enterprise\n")
            user_input = int(input("Choose option: "))

            match user_input:
                case 1:
                    print("Verifying citizenship....")
                    time.sleep(2)
                    print("Scanning face and fingerprint...")
                    time.sleep(2)

                    self.tier_name = 'Agent'
                    cursor.execute("SELECT id, name from tier "
                                   "WHERE name = 'Agent'")
                    agent_id = cursor.fetchall()[0][0]
                    sql = (f"UPDATE user SET tier_id = {agent_id} "
                           f"WHERE username = '{self.username}'")
                    cursor.execute(sql)
                    db.commit()

                    print("\nKYC updated to Agent.\n")

                case 2:
                    print("Verifying PAN card and VAT number....")
                    time.sleep(2)
                    print("Wait a moment...")
                    time.sleep(2)

                    self.tier_name = 'Enterprise'
                    cursor.execute("SELECT id, name from tier "
                                   "WHERE name = 'Enterprise'")
                    enterprise_id = cursor.fetchall()[0][0]
                    sql = (f"UPDATE user SET tier_id = {enterprise_id} "
                           f"WHERE username = '{self.username}'")
                    cursor.execute(sql)
                    db.commit()

                    print("\nKYC updated to Enterprise.\n")
        else:
            print("Your KYC is already verified.\n")

    def logout(self):
        self.authenticated = False





