class User:
    def __init__(self, cursor) -> None:
        self.username = None
        self.firstname = None
        self.lastname = None
        self.cursor = cursor

    def __str__(self) -> str:
        return f"================\nUsername: {self.username}\nFirst name: {self.firstname}\nLast name: {self.lastname}"
    
    def menu(self):
        choice = None 
        user = None

        while not choice or not user:
            print("""
=====================================================================
███████╗██╗░░██╗██████╗░██╗░░░░░██╗████████╗████████╗███████╗██████╗░
██╔════╝╚██╗██╔╝██╔══██╗██║░░░░░██║╚══██╔══╝╚══██╔══╝██╔════╝██╔══██╗
█████╗░░░╚███╔╝░██████╔╝██║░░░░░██║░░░██║░░░░░░██║░░░█████╗░░██████╔╝
██╔══╝░░░██╔██╗░██╔═══╝░██║░░░░░██║░░░██║░░░░░░██║░░░██╔══╝░░██╔══██╗
███████╗██╔╝╚██╗██║░░░░░███████╗██║░░░██║░░░░░░██║░░░███████╗██║░░██║
╚══════╝╚═╝░░╚═╝╚═╝░░░░░╚══════╝╚═╝░░░╚═╝░░░░░░╚═╝░░░╚══════╝╚═╝░░╚═╝
Please choose what you wish to do.
[1] Login
[2] Create Account
[0] Exit
=====================================================================
        """)
            choice = int(input("Choice > "))

            if choice == 1:
                user = self.login()
            elif choice == 2:
                user = self.signup()
            elif choice == 0:
                return False
            else:
                print("Invalid choice!")

        self.setUser(user)
        return True

    #=========================================================================A U T H E N T I C A T I O N============================
    def login(self):
        username = input("==========\nEnter your username: ")
        query = f"SELECT * FROM users WHERE username = \"{username}\";"

        self.cursor.execute(query)

        # Fetch all rows of data
        user = self.cursor.fetchone()

        if not user:
            print("User does not exist!")

        return user

    def signup(self):
        print("==========\nLet's sign you up for an account in our database!")

        # username input
        username = None
        while not username:
            username = input("Enter your username: ").strip()
            
            user = self.findUser(username, False)

            if user:
                print("Username is already taken! Please try again.")
                username = None
        
        # name inputs
        firstname = input("Enter your first name: ").strip()
        lastname = input("Enter your last name: ").strip()

        # add user to database
        query = f"INSERT INTO users(username, first_name, last_name) VALUES(\"{username}\", '{firstname}', '{lastname}')"
        self.cursor.execute(query)

        # fetch user
        query = f"SELECT * FROM users WHERE username = \"{username}\";"
        self.cursor.execute(query)

        # return user
        return self.cursor.fetchone()
    
    # set user
    def setUser(self, user):
        self.username = user[0]
        self.firstname = user[1]
        self.lastname = user[2]

    def findUser(self, username, printNotFound = True):
        # check if member exists
        query = f"SELECT * FROM users where username = '{username}'"
        self.cursor.execute(query)  

        user = self.cursor.fetchone()

        if not user:
            if printNotFound:
                print(f"User {username} does not exists.")
            return None
        
        return user

        

