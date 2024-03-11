class Bank:
    def __init__(self, name):
        self.name = name
        self.accounts = []
        self.total_balance = 0
        self.total_loan = 0
        self.loan_feature = False

    def create_account(self, email, password, is_admin=False):
        if is_admin:
            account = Admin(email, password)
        else:
            account = RegularUser(email, password)
        self.accounts.append(account)
        return account

    def delete_account(self, email):
        for account in self.accounts:
            if account.email == email:
                self.accounts.remove(account)
                break

    def get_all_accounts(self):
        return self.accounts

    def get_total_balance(self):
        total = sum(account.balance for account in self.accounts)
        return total

    def get_total_loan(self):
        total = sum(account.loan for account in self.accounts)
        return total

    def toggle_loan_feature(self):
        self.loan_feature = not self.loan_feature
        return self.loan_feature


class User:
    def __init__(self, email, password):
        self.email = email
        self.password = password

class Admin(User):
    def __init__(self, email, password):
        super().__init__(email, password)

    def create_account(self, email, password):
        return bank.create_account(email, password, is_admin=False)

    def delete_account(self, email):
        bank.delete_account(email)

    def see_all_accounts(self):
        return bank.get_all_accounts()

    def check_total_balance(self):
        return bank.get_total_balance()

    def check_total_loan(self):
        return bank.get_total_loan()

    def toggle_loan_feature(self):
        return bank.toggle_loan_feature()


class RegularUser(User):
    def __init__(self, email, password):
        super().__init__(email, password)
        self.balance = 0

    def deposit(self, amount):
        self.balance += amount
        return self.balance

    def withdraw(self, amount):
        if amount <= self.balance:
            self.balance -= amount
            return True
        else:
            return False

    def transfer(self, receiver, amount):
        if amount <= self.balance:
            self.balance -= amount
            receiver.balance += amount
            return True
        else:
            return False

    def check_balance(self):
        return self.balance

    def take_loan(self):
        if bank.loan_feature:
            loan_amount = self.balance * 2
            self.balance += loan_amount
            self.loan += loan_amount
            return True
        else:
            return False


def login():
    email = input("Enter your email: ")
    password = input("Enter your password: ")

    
    for admin in admins:
        if admin.email == email and admin.password == password:
            return admin

    
    for user in users:
        if user.email == email and user.password == password:
            return user

    print("Invalid email or password. Please try again.")
    return None

def register():
    email = input("Enter your email: ")
    password = input("Enter your password: ")

    is_admin = input("Are you an admin? (yes/no): ").lower()
    if is_admin == "yes":
        user = Admin(email, password)
        admins.append(user)
    else:
        user = RegularUser(email, password)
        users.append(user)

    print("Registration successful!")


bank = Bank("DAF Bank")
admins = []
users = []

while True:
    print("\nWelcome to DAF Bank")
    print("1. Login")
    print("2. Register")
    print("3. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        user = login()
        if user:
            if isinstance(user, Admin):
                while True:
                    print("\nAdmin Menu")
                    print("1. Create Account")
                    print("2. Delete User Account")
                    print("3. See All User Accounts")
                    print("4. Check Total Available Balance")
                    print("5. Check Total Loan Amount")
                    print("6. Toggle Loan Feature")
                    print("7. Logout")

                    admin_choice = input("Enter your choice: ")

                    if admin_choice == "1":
                        email = input("Enter user email: ")
                        password = input("Enter user password: ")
                        bank.create_account(email, password)
                        print("Account created successfully!")

                    elif admin_choice == "2":
                        email = input("Enter user email to delete account: ")
                        bank.delete_account(email)
                        print("Account deleted successfully!")

                    elif admin_choice == "3":
                        print("All User Accounts:")
                        for account in bank.get_all_accounts():
                            print(account.email)

                    elif admin_choice == "4":
                        print("Total Available Balance:", bank.get_total_balance())

                    elif admin_choice == "5":
                        print("Total Loan Amount:", bank.get_total_loan())

                    elif admin_choice == "6":
                        loan_feature = bank.toggle_loan_feature()
                        if loan_feature:
                            print("Loan Feature turned ON")
                        else:
                            print("Loan Feature turned OFF")

                    elif admin_choice == "7":
                        break
                    else:
                        print("Invalid choice!")

            else:
                while True:
                    print("\nUser Menu")
                    print("1. Deposit")
                    print("2. Withdraw")
                    print("3. Transfer Money")
                    print("4. Check Balance")
                    print("5. Take Loan")
                    print("6. Logout")

                    user_choice = input("Enter your choice: ")

                    if user_choice == "1":
                        amount = float(input("Enter amount to deposit: "))
                        user.deposit(amount)
                        print("Deposit successful. Current balance:", user.balance)

                    elif user_choice == "2":
                        amount = float(input("Enter amount to withdraw: "))
                        success = user.withdraw(amount)
                        if success:
                            print("Withdrawal successful. Current balance:", user.balance)
                        else:
                            print("Insufficient funds!")

                    elif user_choice == "3":
                        receiver_email = input("Enter receiver's email: ")
                        amount = float(input("Enter amount to transfer: "))
                        for receiver in users:
                            if receiver.email == receiver_email:
                                success = user.transfer(receiver, amount)
                                if success:
                                    print("Transfer successful. Current balance:", user.balance)
                                else:
                                    print("Transfer failed. Check balance or receiver email.")
                                break
                        else:
                            print("Receiver not found!")

                    elif user_choice == "4":
                        print("Current balance:", user.check_balance())

                    elif user_choice == "5":
                        success = user.take_loan()
                        if success:
                            print("Loan successfully taken. Current balance:", user.balance)
                        else:
                            print("Loan feature is not available or you are not eligible.")

                    elif user_choice == "6":
                        break
                    else:
                        print("Invalid choice!")

    elif choice == "2":
        register()
    elif choice == "3":
        print("Thank you for using DAF Bank. Goodbye!")
        break
    else:
        print("Invalid choice!")
