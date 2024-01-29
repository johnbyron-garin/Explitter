import datetime
from utils.group import Group
from utils.friends import Friends

class Expense:
    def __init__(self, cursor, user):
        self.cursor = cursor
        self.user = user

    def program(self):
        while True:
            c = self.menu()
            if c == 1:
                self.createExpense()
            elif c == 2:
                self.removeExpense()
            elif c == 3:
                self.pay_unpaid_expenses()
            elif c == 4:
                self.view_expense_month()
            elif c == 5:
                self.view_expenses_with_friend()
            elif c == 6:
                self.view_expenses_with_group()
            elif c == 7:
                self.view_current_balance()
            elif c == 8:
                self.view_outstanding_friend()
            elif c == 9:
                self.view_outstanding_group()
            elif c == 0:
                print("""
                                                        .''.       
                    .''.      .        *''*    :_\/_:     . 
                    :_\/_:   _\(/_  .:.*_\/_*   : /\ :  .'.:.'.
                .''.: /\ :   ./)\   ':'* /\ * :  '..'.  -=:o:=-
                :_\/_:'.:::.    ' *''*    * '.\'/.' _\(/_'.':'.'
                : /\ : :::::     *_\/_*     -= o =-  /)\    '  *
                '..'  ':::'     * /\ *     .'/.\'.   '
                    *            *..*         :
                    *
                        *
                """)
                print("\n\t\tThank you for using this program!\n")
                break  
            else:
                print("\n! ! ! Invalid input ! ! ! ")

    def menu(self):
        print("""
===========================================
▒█▀▀▀ ▀▄▒▄▀ ▒█▀▀█ ▒█▀▀▀ ▒█▄░▒█ ▒█▀▀▀█ ▒█▀▀▀ 
▒█▀▀▀ ░▒█░░ ▒█▄▄█ ▒█▀▀▀ ▒█▒█▒█ ░▀▀▀▄▄ ▒█▀▀▀ 
▒█▄▄▄ ▄▀▒▀▄ ▒█░░░ ▒█▄▄▄ ▒█░░▀█ ▒█▄▄▄█ ▒█▄▄▄
[1] Create expense
[2] Remove expense
[3] Pay unpaid expenses
[4] View all expenses made this month
[5] View all expenses made with a friend
[6] View all expenses made with a group
[7] View current balance from all expenses
[8] View friends with outstanding balances
[9] View groups with oustanding balances
[0] Back
        """)

        choice = int(input("Choice: "))
        return choice
    def pay_unpaid_expenses(self):
        query = f"SELECT * FROM transactions where tid IN (SELECT tid FROM users_has_transactions WHERE username = '{self.user.username}' AND NOT paid)"
        self.cursor.execute(query)

        expenses = self.cursor.fetchall()

        self.printExpenses(expenses)

        expenseID = int(input("Enter expense ID to mark as paid: "))

        ids = [x[0] for x in expenses]

        if not expenseID in ids:
           return print("Invalid expense ID!")
        
        query = f"UPDATE users_has_transactions SET paid = 1 WHERE tid = {expenseID} AND username = '{self.user.username}'"

        self.cursor.execute(query)

        # check if we should update is_settled
        query = f"SELECT * FROM users_has_transactions WHERE tid = {expenseID} AND NOT paid"

        self.cursor.execute(query)

        user = self.cursor.fetchone()

        if not user:
            query = f"UPDATE transactions SET is_settled = 1 WHERE tid = {expenseID}"
            self.cursor.execute(query)

        print("Successfully marked as paid!")

    def view_expense_month(self):
        date = datetime.date.today()
        current_month = date.month
        current_year = date.year

        query = f"SELECT * FROM transactions WHERE tid IN (SELECT tid FROM users_has_transactions WHERE username = '{self.user.username}') OR payer_username = '{self.user.username}' AND MONTH(date_created) = {current_month} AND YEAR(date_created) = {current_year}"

        self.cursor.execute(query)

        expenses = self.cursor.fetchall()

        self.printExpenses(expenses)

    def view_expenses_with_friend(self):
        FriendAPI = Friends(self.cursor, self.user)

        FriendAPI.get_friends()

        friend = input("Enter friend username: ")

        query = f"SELECT * FROM transactions WHERE (tid IN (SELECT tid FROM users_has_transactions WHERE username = '{friend}') AND payer_username = '{self.user.username}') OR (tid IN (SELECT tid FROM users_has_transactions WHERE username = '{self.user.username}') AND payer_username = '{friend}')"

        self.cursor.execute(query)

        expenses = self.cursor.fetchall()

        self.printExpenses(expenses)

    def view_expenses_with_group(self):
        # fetch expenses of a group
        GroupAPI = Group(self.cursor, self.user)

        group = GroupAPI.find_group()
        
        if not group:
            return
        
        query = f"SELECT * FROM transactions t JOIN group_transactions gt ON t.tid = gt.tid JOIN groups g ON gt.gid = g.gid JOIN group_members gm ON g.gid = gm.gid WHERE gm.username = '{self.user.username}' AND g.gid = {group} ORDER BY g.gid;"
        self.cursor.execute(query)
        expenses = self.cursor.fetchall()
        self.printExpenses(expenses)
    
    def view_outstanding_friend(self):
        # fetch oustanding balance of friends
        query = f"SELECT username, SUM(contribution)debt FROM users_has_transactions NATURAL JOIN (SELECT * FROM transactions WHERE payer_username = '{self.user.username}')a WHERE NOT tid in (SELECT tid FROM group_transactions) AND NOT paid GROUP BY username;"

        self.cursor.execute(query)
        outstandings = self.cursor.fetchall()
        
        if len(outstandings):
            print("==== OUTSTANDINGS ====")
            for outstanding in outstandings:
                print(f"Username: {outstanding[0]}, Outstanding Balance: {outstanding[1]}")
        else:
            print("No friends with outstanding balance")

    def view_outstanding_group(self):
        # fetch outstanding balance of groups
        query = f"SELECT gid, username, SUM(contribution)debt FROM users_has_transactions NATURAL JOIN (SELECT * FROM transactions NATURAL JOIN group_transactions WHERE payer_username = '{self.user.username}')a WHERE NOT paid GROUP BY gid, username"

        self.cursor.execute(query)
        outstandings = self.cursor.fetchall()
        
        if len(outstandings):
            print("==== OUTSTANDINGS ====")
            for outstanding in outstandings:
                print(f"Group: {outstanding[0]}, Username: {outstanding[1]}, Outstanding Balance: {outstanding[2]}")
        else:
            print("No groups with outstanding balance")

    def view_current_balance(self):
        # fetch current balance
        query = f"SELECT sum(contribution) 'Total Debt' FROM users_has_transactions NATURAL JOIN (SELECT * FROM transactions WHERE payer_username = '{self.user.username}')a WHERE not paid"

        self.cursor.execute(query)

        totalOutstanding = self.cursor.fetchone()[0]

        query = f"SELECT sum(contribution) 'Total Unpaid' FROM users_has_transactions NATURAL JOIN (SELECT * FROM transactions)a WHERE NOT paid AND username = '{self.user.username}'"

        self.cursor.execute(query)

        totalUnpaid = self.cursor.fetchone()[0]

        print(f"===== CURRENT BALANCE =====\n>(PHP) {totalOutstanding - totalUnpaid}")
        print('You need to fix your finance!' if totalOutstanding - totalUnpaid < 0 else 'Remind people that they still owe you money!')  
        print()

    def createExpense(self):
        print("==== Creating an expense ====")
        category = None
        
        while not category:
            category = int(input("Category:\n[1] Expense\n[2] Settlement\n> "))

            if category != 1 and category != 2:
                print("Please put a valid category")
                category = None

        if category == 1:
            category = 'expenses'
            amount = float(input("Amount: "))
            transaction_description = input("Description: ")
            date_created = datetime.date.today()
            query = f"INSERT INTO transactions(amount, category, date_created, payer_username, transaction_description) VALUES({amount}, '{category}', '{date_created}', '{self.user.username}', '{transaction_description}')"
            self.cursor.execute(query)

            query = "SELECT max(tid) tid FROM transactions"
            self.cursor.execute(query)
            new_id = self.cursor.fetchone()[0]

            while True:
                print("Do you wish to add people to this expense?\n[1] Friends\n[2] Groups\n[0] No")

                choice = int(input("Choice: "))

                if choice == 0:
                    break
                elif choice == 1:
                    self.friendExpense(new_id, amount)
                    break
                elif choice == 2:
                    self.groupExpense(new_id, amount)
                    break
                else: 
                    print("Invalid input!")
        else:
           category = 'settlement'
           username = input("Enter username of user to settle payment with: ")
         
           query = f"SELECT * FROM transactions NATURAL JOIN (SELECT tid FROM users_has_transactions WHERE username = '{self.user.username}' AND NOT paid)a WHERE payer_username = '{username}'"
           self.cursor.execute(query)

           debts = self.cursor.fetchall()

           if len(debts):
                description = input("Enter description of settlement: ")
                date_created = datetime.date.today()
                amount = sum([x[2] for x in debts])
                tids = [x[0] for x in debts]

                query = f"INSERT INTO transactions(amount, category, date_created, payer_username, transaction_description) VALUES({amount}, '{category}', '{date_created}', '{self.user.username}', '{description}')"
                self.cursor.execute(query)
           else:
               return print("No need to create a settlement")

        print("Successfully created an expense!")


    
    def friendExpense(self, tid, amount):
        # function to add friends to expense
        FriendAPI = Friends(self.cursor, self.user)

        FriendAPI.get_friends()

        friends = input("Enter username of friends to add to this expense (Separate by comma): ").split(',')

        query_val = []
        for friend in friends:
            query_val.append(f"({tid}, '{friend}')")

        query = f"INSERT INTO users_has_transactions(tid, username) VALUES{','.join(query_val)}"
        self.cursor.execute(query)

        contribution = amount / ((len(friends)) + 1)

        query = f"UPDATE transactions SET contribution = {contribution} where tid = {tid}"
        self.cursor.execute(query) 

    def groupExpense(self, tid, amount):
        # function to add group members to expense
        GroupAPI = Group(self.cursor, self.user)

        group = None

        while not group:
            group = GroupAPI.find_group()

        members = GroupAPI.get_group_members(group) 
       

        if len(members) == 1:
            return print("There are no other members in this group aside from you")
        
        contribution = amount / len(members)

        # filter members where user is not included
        filtered_members = []

        for member in members:
            if member[0] != self.user.username:
                filtered_members.append(member[0])

        # add members to transaction
        query_val = []
        for member in filtered_members:
            query_val.append(f"({tid}, '{member}')")
        
        query = f"INSERT INTO users_has_transactions(tid, username) VALUES{','.join(query_val)}"
        self.cursor.execute(query)

        query = f"INSERT INTO group_transactions(tid, gid) VALUES({tid}, {group})"
        self.cursor.execute(query)

        query = f"UPDATE transactions SET contribution = {contribution} where tid = {tid}"
        self.cursor.execute(query) 


    def showCreatedOpenExpenses(self):
        query = f"SELECT * FROM transactions WHERE category = 'expenses' AND payer_username = '{self.user.username}' AND NOT is_settled"
        self.cursor.execute(query)
        rows = self.cursor.fetchall()

        self.printExpenses(rows)

        return rows
        

    def get_id(self, expenses):
        choice = int(input("\n\nEnter expense to delete: "))

        ids = [x[0] for x in expenses]

        if not choice in ids:
            print("Invalid expense ID!")
            return None 
        
        return id

    def removeExpense(self):
        expenses = self.showCreatedOpenExpenses()

        if not len(expenses):
            return

        expense_id = self.get_id(expenses)

        if not expense_id:
            return

        # delete expense from group
        query = f"DELETE FROM group_transactions WHERE tid = {expense_id}"
        self.cursor.execute(query)

        # delete expense from user transactions
        query = f"DELETE FROM users_has_transactions WHERE tid = {expense_id}"
        self.cursor.execute(query)

        # delete expense from transactions
        query = f"DELETE FROM transactions WHERE tid = {expense_id}"
        self.cursor.execute(query)

        print("Successfully deleted an expense!")
        
    def printExpenses(self, expenses):
        if len(expenses):
            for expense in expenses:
                self.formatExpense(expense)
        else:
            print("No expenses to show.")
        

    def formatExpense(self, expense):
        print(f'=== EXPENSE {expense[0]} ===')
        print(f"Amount: {expense[1]}\nContribution: {expense[2]}\nExpense Type:{expense[3]}\nDate Created: {expense[4]}\nPayer Username: {expense[5]}\nDescription: {expense[7]}\nIs settled: {'Not yet' if expense[6] == 0 else 'Completed'}\n")


