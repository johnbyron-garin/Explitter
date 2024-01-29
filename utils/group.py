class Group:
    def __init__(self, cursor, user):
        self.cursor = cursor
        self.user = user

    def program(self):
        while True:
            c = self.menu()
            if c == 1:
                new_group = input("Insert group name: ")
                self.add_group(new_group)         
            elif c == 2:
                group = self.find_group()
                if group:
                    self.add_members(group)
            elif c == 3:
                group = self.find_group()
                if group:
                    self.edit_group_name(group)       
            elif c == 4:
                group = self.find_group()
                if group:
                    self.leave_group(group)
            elif c == 5:
                group = self.find_group()
                if group:
                    self.delete_group(group) 
            elif c == 6:
                self.view_all_groups()       
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
                print("\n\t\tDone checking groups!\n")
                return
            else:
                print("\n! ! ! Invalid input ! ! ! ")
    
    def menu(self):
        print("""
=====================================
█████▀███████████████████████████████
█─▄▄▄▄█▄─▄▄▀█─▄▄─█▄─██─▄█▄─▄▄─█─▄▄▄▄█
█─██▄─██─▄─▄█─██─██─██─███─▄▄▄█▄▄▄▄─█
▀▄▄▄▄▄▀▄▄▀▄▄▀▄▄▄▄▀▀▄▄▄▄▀▀▄▄▄▀▀▀▄▄▄▄▄▀
[1] Create group
[2] Add Group Members
[3] Edit Group Name
[4] Leave Group
[5] Delete Group
[6] View all groups
[0] Back
=====================================
        """)

        choice = int(input("Choice: "))
        return choice

    def add_group(self, group_name):
        # add group
        query = "INSERT INTO groups (group_name) VALUES (%s)"
        values = (group_name,)
        self.cursor.execute(query, values)

        # add user to the list of members of that group
        # Get the latest added group
        query = "SELECT max(gid) gid FROM groups"
        self.cursor.execute(query)
        new_group_id = self.cursor.fetchone()[0]
        query = f"INSERT INTO group_members(gid, username) VALUES({new_group_id}, '{self.user.username}')"
        self.cursor.execute(query)
        print("Group added successfully!")

    def add_members(self, group_id):
        # use this function for adding members to the group
        members = input("Enter username of members to add (Separate by comma): ").split(',')
        query_val = []

        # process each member
        for member in members:
            # check if user exist first
            user = self.user.findUser(member)

            if not user:
                continue

            query_val.append(f"({group_id}, '{member}')")
        
        # add new members
        query = f"INSERT INTO group_members(gid, username) VALUES{','.join(query_val)}"
        self.cursor.execute(query)
        print("Successfully added new group members")

    def edit_group_name(self, group_id):
        # function to edit a group name
        new_name = input("New group name: ")
        query = f"UPDATE groups SET group_name = '{new_name}' WHERE gid = {group_id}"

        self.cursor.execute(query)
        print("Successfully updated group name!")

    def leave_group(self, group_id):
        # function to leave a group
        query = f"DELETE FROM group_members WHERE gid = {group_id} AND username = '{self.user.username}'"
        self.cursor.execute(query)
        print("Successfully left group!")


    def delete_group(self, group_id):
        # remove all members
        query = f'DELETE FROM group_members WHERE gid = {group_id}'
        self.cursor.execute(query)
        # get all tids
        query = f"SELECT tid FROM group_transactions WHERE gid = {group_id}"
        self.cursor.execute(query)
        tids = [x[0] for x in self.cursor.fetchall()]
        # remove all user transactions
        query = f'DELETE FROM users_has_transactions WHERE tid in (SELECT tid FROM group_transactions WHERE gid = {group_id})'
        self.cursor.execute(query)
        # remove all group transactions
        query = f'DELETE FROM group_transactions WHERE tid in (SELECT tid FROM group_transactions WHERE gid = {group_id})'
        self.cursor.execute(query)
        # remove all transactions
        for tid in tids:
            query = f'DELETE FROM transactions WHERE tid = {tid}'
            self.cursor.execute(query)
        # use this function to delete a chosen group
        query = "DELETE FROM groups WHERE gid = %s"
        values = (group_id,)
        self.cursor.execute(query, values)
        print("Group deleted successfully!")

    def view_all_groups(self):
        # use this function to view all groups that user is a part of
        query = f"SELECT * FROM groups NATURAL JOIN (SELECT gid FROM group_members WHERE username = '{self.user.username}')g"

        self.cursor.execute(query)
        rows = self.cursor.fetchall()

        if len(rows) > 0:
            print("Your Groups:")
            for row in rows:
                print(f"\t[ID: {row[0]}] Group Name: {row[1]}")
        else:
            print("You are not part of any group.")

        return rows

    def find_group(self):
        groups = self.view_all_groups()

        if not len(groups):
            return None
        
        ids = [x[0] for x in groups]

        # Ask for group id
        group = int(input("Enter Group ID: "))

        # check if group is a valid id
        if not group in ids:
            print("Please enter a valid ID!")
            return None

        # return group id
        return group
    
    def get_group_members(self, gid):
        # get members of the groups
        query = f"SELECT username FROM group_members where gid = {gid}"
        self.cursor.execute(query)
        members = self.cursor.fetchall()

        return members