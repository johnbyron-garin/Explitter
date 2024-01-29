import mysql.connector
from utils.user import User
from utils.expense import Expense
from utils.friends import Friends
from utils.group import Group

cnx = mysql.connector.connect(
host='localhost',
user='project127',
password='secret123',
database='project127'
)

cursor =  cnx.cursor()

class Main:
    def __init__(self) -> None:
        self.user = User(cursor)

    def start(self):
        while True:
            # authentication
            user = self.user.menu()
   
            # if user chose exit, then stop the program
            if not user:
                return
            # commit changes
            cnx.commit()     

            # User Features
            while True:
                choice = self.menu()

                if choice == 1:
                    self.handleExpenses()
                elif choice == 2:
                    self.handleFriends()
                elif choice == 3:
                    self.handleGroups()
                elif choice == 0:
                    
                    break
                else:
                    print("Invalid choice")

    def handleExpenses(self):
        expense = Expense(cursor, self.user)
        expense.program()
        # commit changes
        cnx.commit()
    
    def handleFriends(self):
        friend = Friends(cursor, self.user)
        friend.program()
        # commit changes
        cnx.commit()       
    
    def handleGroups(self):
        group = Group(cursor, self.user)
        group.program()
        # commit changes
        cnx.commit()        

    def menu(self):
        print("""
=====================================
███╗░░░███╗███████╗███╗░░██╗██╗░░░██╗
████╗░████║██╔════╝████╗░██║██║░░░██║
██╔████╔██║█████╗░░██╔██╗██║██║░░░██║
██║╚██╔╝██║██╔══╝░░██║╚████║██║░░░██║
██║░╚═╝░██║███████╗██║░╚███║╚██████╔╝
╚═╝░░░░░╚═╝╚══════╝╚═╝░░╚══╝░╚═════╝░
Please choose what you wish to do.
[1] Expense
[2] Friend
[3] Group
[0] Log Out
=====================================
        """)

        choice = int(input("Choice > "))
        return choice



main = Main()

main.start()
cursor.close()
cnx.close()