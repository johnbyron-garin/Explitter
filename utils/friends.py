class Friends:
    def __init__(self, cursor, user):
        self.cursor = cursor
        self.user = user

    def program(self):
        while True:
            choice = self.menu()
            if choice == 1:
                username = input("Enter username of user you wish to add: ")
                self.add_friend(username)      
            elif choice == 2:
                username = input("Enter username of friend to unfriend: ")
                self.delete_friend(username)           
            elif choice == 3:
                user = input("Enter username of friend to search: ")
                self.search_friend(user)
            elif choice == 4:
                self.get_friends()   
            elif choice == 0:
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
                return
            else:
                print("\n! ! ! Invalid input ! ! ! ")


    def menu(self):
        print("""
===========================================
███████████████████████████████████████████
█▄─▄▄─█▄─▄▄▀█▄─▄█▄─▄▄─█▄─▀█▄─▄█▄─▄▄▀█─▄▄▄▄█
██─▄████─▄─▄██─███─▄█▀██─█▄▀─███─██─█▄▄▄▄─█
▀▄▄▄▀▀▀▄▄▀▄▄▀▄▄▄▀▄▄▄▄▄▀▄▄▄▀▀▄▄▀▄▄▄▄▀▀▄▄▄▄▄▀
[1] Add friend
[2] Unfriend
[3] Search friend
[4] View all friends
[0] Back
===========================================
        """)

        choice = int(input("Choice > "))
        return choice
        
    def add_friend(self, username):
        # check if username is also current user
        if username == self.user.username:
            return print("You cannot add yourself!")

        # check if user exists
        user = self.user.findUser(username)

        if not user:
            return

        query = f"SELECT * FROM friends WHERE username = '{self.user.username}' AND friend = '{username}'"

        self.cursor.execute(query)
        existing_record = self.cursor.fetchone()

        if existing_record:
            return print(f"You are already friends with {username}")

        query = f"INSERT INTO friends(username, friend) VALUES('{self.user.username}', '{username}'),('{username}', '{self.user.username}')"
        self.cursor.execute(query)
        print("Friendship added successfully.")

    def delete_friend(self, username):
        # check if user does not exists
        user = self.user.findUser(username)

        if not user:
            return
        
        # query string for deleting instance of friends
        query = f"DELETE FROM friends WHERE (username = '{self.user.username}' AND friend = '{username}') OR (username = '{username}' AND friend = '{self.user.username}')"

        self.cursor.execute(query)
    
        if self.cursor.rowcount > 0:
            print("Friendship deleted successfully.")
        else:
            print("You are not friends with that user.")

    def search_friend(self, username):
        # find a user from a user's friend list
        query = f"SELECT friend FROM users NATURAL JOIN (SELECT * FROM friends WHERE username = '{self.user.username}' AND friend = '{username}')e"

        self.cursor.execute(query)

        friend = self.cursor.fetchone()

        if not friend:
            return print(f"You are not friends with user ${username}")
        else:
            print(f"You are friends with user {friend[0]}!")

        return friend
        

    def get_friends(self):
        # get a list of friends
        query = f"SELECT * FROM users NATURAL JOIN (SELECT username FROM friends WHERE friend = '{self.user.username}')f"

        self.cursor.execute(query)
        rows = self.cursor.fetchall()

        if len(rows) > 0:
            print("All Friends:")
            for index, row in enumerate(rows):
                print(f"\t[{index + 1}] Username: {row[0]} First Name: {row[1]} Last Name: {row[2]}")
        else:
            print("No friends found.")

        return rows
    

