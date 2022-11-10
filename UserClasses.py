import hashlib


class User:
    def __init__(self, username, password) -> None:
        self.username = username
        self.password = password


class Users:
    def __init__(self, filename):
        self.database = filename
        self.users = self.readFromFile()

    def createUser(self, username, password):
        for user in self.users:
            if user.username == username:
                return False
        encoder1 = password.encode()
        encoder2 = username.encode()
        hashedPassword = hashlib.md5(encoder1).hexdigest()
        hashedUsername = hashlib.md5(encoder2).hexdigest()
        self.users.append(User(hashedUsername, hashedPassword))
        self.writeToFile()
        return True

    def authenticateUser(self, username, password):
        encoder1 = password.encode()
        encoder2 = username.encode()
        hashedPassword = hashlib.md5(encoder1).hexdigest()
        hashedUsername = hashlib.md5(encoder2).hexdigest()
        for user in self.users:
            if user.username == hashedUsername and user.password == hashedPassword:
                return True
        return False

    def changePassword(self, username, newPassword):
        for i, user in enumerate(self.users):
            if user.username == username:
                user.password = newPassword
                self.users[i] = user
                return True
        return False

    def readFromFile(self):
        with open(self.database, "r") as file:
            items = []
            lines = file.readlines()
            for line in lines[1:]:
                userList = line.split(",")
                item = User(
                    userList[0].strip(),
                    userList[1].strip(),
                )
                items.append(item)
        return items

    def writeToFile(self):
        with open(self.database, "w") as file:
            file.write("Username, Password\n")
            for user in self.users:
                userString = f"{user.username}, {user.password}\n"
                file.write(userString)
