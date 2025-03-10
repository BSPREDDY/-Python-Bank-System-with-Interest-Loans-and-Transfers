import uuid
from datetime import datetime

class Account:
    INTEREST_RATE = 0.05  # 5% annual interest

    def __init__(self, name, initial_balance=0.0):
        self.account_number = str(uuid.uuid4())[:8]  # Generate a unique 8-char account number
        self.name = name
        self.balance = initial_balance
        self.loan_balance = 0.0
        self.transactions = []  # Store transaction history
        self.log_transaction("Account Created", initial_balance)

    def log_transaction(self, transaction_type, amount):
        """Logs each transaction with a timestamp."""
        self.transactions.append({
            "type": transaction_type,
            "amount": amount,
            "balance": self.balance,
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

    def deposit(self, amount):
        if amount <= 0:
            print("❌ Invalid deposit amount.")
            return
        self.balance += amount
        self.log_transaction("Deposit", amount)
        print(f"✅ {amount:.2f} deposited successfully. New balance: {self.balance:.2f}")

    def withdraw(self, amount):
        if amount <= 0:
            print("❌ Invalid withdrawal amount.")
            return
        if amount > self.balance:
            print("❌ Insufficient balance.")
            return
        self.balance -= amount
        self.log_transaction("Withdraw", amount)
        print(f"✅ {amount:.2f} withdrawn successfully. New balance: {self.balance:.2f}")

    def apply_interest(self):
        """Applies annual interest to the account."""
        interest = self.balance * Account.INTEREST_RATE
        self.balance += interest
        self.log_transaction("Interest Added", interest)
        print(f"💰 Interest of {interest:.2f} applied. New balance: {self.balance:.2f}")

    def take_loan(self, amount):
        """Allows the user to take a loan."""
        if amount <= 0:
            print("❌ Invalid loan amount.")
            return
        self.loan_balance += amount
        self.balance += amount  # Loan amount is added to balance
        self.log_transaction("Loan Taken", amount)
        print(f"🏦 Loan of {amount:.2f} approved. New balance: {self.balance:.2f}")

    def repay_loan(self, amount):
        """Allows the user to repay a loan."""
        if amount <= 0:
            print("❌ Invalid repayment amount.")
            return
        if amount > self.loan_balance:
            print(f"⚠️ Your loan balance is only {self.loan_balance:.2f}. Paying off full loan.")
            amount = self.loan_balance
        self.loan_balance -= amount
        self.balance -= amount
        self.log_transaction("Loan Repaid", -amount)
        print(f"✅ Loan repayment of {amount:.2f} successful. Remaining loan: {self.loan_balance:.2f}")

    def transfer(self, recipient, amount):
        """Transfers money to another account."""
        if amount <= 0:
            print("❌ Invalid transfer amount.")
            return
        if amount > self.balance:
            print("❌ Insufficient balance for transfer.")
            return
        self.balance -= amount
        recipient.balance += amount
        self.log_transaction("Transfer Out", -amount)
        recipient.log_transaction("Transfer In", amount)
        print(f"🔄 Transfer of {amount:.2f} to {recipient.name} successful.")

    def show_balance(self):
        print(f"💰 Current balance for {self.name}: {self.balance:.2f}")
        print(f"💳 Loan balance: {self.loan_balance:.2f}")

    def show_transactions(self):
        print(f"\n📜 Transaction History for {self.name} (Account: {self.account_number})")
        for t in self.transactions:
            print(f"{t['time']} | {t['type']} | Amount: {t['amount']:.2f} | Balance: {t['balance']:.2f}")

class BankSystem:
    def __init__(self):
        self.accounts = {}

    def create_account(self):
        name = input("Enter account holder's name: ")
        initial_balance = float(input("Enter initial deposit amount: "))
        account = Account(name, initial_balance)
        self.accounts[account.account_number] = account
        print(f"\n🎉 Account created successfully! Your account number is {account.account_number}")

    def access_account(self):
        acc_number = input("Enter your account number: ")
        account = self.accounts.get(acc_number)
        if not account:
            print("❌ Account not found.")
            return

        while True:
            print("\n🏦 Account Menu")
            print("1️⃣ Deposit")
            print("2️⃣ Withdraw")
            print("3️⃣ Check Balance")
            print("4️⃣ Transaction History")
            print("5️⃣ Apply Interest")
            print("6️⃣ Take Loan")
            print("7️⃣ Repay Loan")
            print("8️⃣ Transfer Money")
            print("9️⃣ Exit")

            choice = input("Choose an option: ")
            if choice == '1':
                amount = float(input("Enter deposit amount: "))
                account.deposit(amount)
            elif choice == '2':
                amount = float(input("Enter withdrawal amount: "))
                account.withdraw(amount)
            elif choice == '3':
                account.show_balance()
            elif choice == '4':
                account.show_transactions()
            elif choice == '5':
                account.apply_interest()
            elif choice == '6':
                amount = float(input("Enter loan amount: "))
                account.take_loan(amount)
            elif choice == '7':
                amount = float(input("Enter repayment amount: "))
                account.repay_loan(amount)
            elif choice == '8':
                recipient_number = input("Enter recipient's account number: ")
                recipient = self.accounts.get(recipient_number)
                if not recipient:
                    print("❌ Recipient account not found.")
                else:
                    amount = float(input("Enter transfer amount: "))
                    account.transfer(recipient, amount)
            elif choice == '9':
                print("👋 Exiting account menu...")
                break
            else:
                print("❌ Invalid choice. Try again.")

    def admin_dashboard(self):
        """Admin can view all user accounts."""
        print("\n🔑 Admin Dashboard - All Accounts")
        if not self.accounts:
            print("No accounts found.")
            return

        for acc_number, account in self.accounts.items():
            print(f"📌 Account: {acc_number} | Name: {account.name} | Balance: {account.balance:.2f} | Loan: {account.loan_balance:.2f}")

    def run(self):
        """Main menu to interact with the banking system."""
        while True:
            print("\n🏦 Welcome to the Bank System")
            print("1️⃣ Create Account")
            print("2️⃣ Access Account")
            print("3️⃣ Admin Dashboard")
            print("4️⃣ Exit")

            choice = input("Choose an option: ")
            if choice == '1':
                self.create_account()
            elif choice == '2':
                self.access_account()
            elif choice == '3':
                self.admin_dashboard()
            elif choice == '4':
                print("👋 Exiting the bank system. Have a great day!")
                break
            else:
                print("❌ Invalid choice. Try again.")

if __name__ == "__main__":
    bank_system = BankSystem()
    bank_system.run()
