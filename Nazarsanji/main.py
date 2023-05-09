from sqlalchemy import create_engine, Column, Integer, String, PickleType, Boolean
from sqlalchemy.orm import sessionmaker, declarative_base
import hashlib
import re
import getpass

Base = declarative_base()


class Poll(Base):
    __tablename__ = 'Polls'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    options = Column(PickleType)
    selOptions = Column(PickleType)
    mode = Column(Boolean)
    creator = Column(String)
    isDisabled = Column(Boolean)


class User(Base):
    __tablename__ = 'Users'
    email = Column(String, primary_key=True)
    password = Column(String)
    participated = Column(PickleType)

class Cli:
    def __init__(self) -> None:
        self.engine = create_engine('sqlite:///Database.db', echo=False)
        Base.metadata.create_all(self.engine)
        self.session = sessionmaker(bind=self.engine)()
        self.quit = False
        self.loggedInUser = None
        if len(self.session.query(Poll).all()) == 0:
            self.lastId = 0
        else:
            self.lastId = self.session.query(Poll).all()[-1].id

    def login(self):
        print("Login!")
        email = input("Email: ")
        password = hashlib.blake2s(getpass.getpass('Password: ').encode()).hexdigest()
        user = self.session.query(User).filter(
            User.email == email, User.password == password).all()
        if len(user) == 1:
            self.loggedInUser = user[0]
            return
        print("Wrong email or password!")

    def signup(self):
        email = input("Enter your email: ")
        password = getpass.getpass('Enter your password: ')
        confPassword = getpass.getpass('Reenter your password: ')
        if len(self.session.query(User).filter(User.email == email).all()) != 0:
            print("A user with this email already exists!")
            return
        regex = re.compile(
            r"([-!#-'*+/-9=?A-Z^-~]+(\.[-!#-'*+/-9=?A-Z^-~]+)*|\"([]!#-[^-~ \t]|(\\[\t -~]))+\")@([-!#-'*+/-9=?A-Z^-~]+(\.[-!#-'*+/-9=?A-Z^-~]+)*|\[[\t -Z^-~]*])")
        if not re.fullmatch(regex,email):
            print("Invalid email!")
            return
        regex = re.compile(r"^(?=.*[A-Z])(?=.*[^a-zA-Z0-9]).{8,}$")
        if not re.fullmatch(regex, password):
            print("Invalid password!")
            return
        if password != confPassword:
            print("Passwords are not the same!")
            return
        self.loggedInUser = User(email=email,password=hashlib.blake2s(password.encode()).hexdigest(),participated = list())
        self.session.add(self.loggedInUser)
        self.session.commit()

    def logout(self):
        self.loggedInUser = None

    def createPoll(self) -> None:
        title = input("Title: ")
        numOpt = int(input("Number of options: "))
        self.lastId += 1
        options = []
        for i in range(numOpt):
            options.append(input(f"Options {i+1}: "))
        mode = input("Single choice or multiple choice: ")
        if mode == "single":
            mode = True
        else:
            mode = False
        self.session.add(Poll(title=title, options=options,
                         id=self.lastId, selOptions=[0]*numOpt, mode = mode, isDisabled = False))
        self.session.commit()
        print("Created!")

    def listPolls(self) -> None:
        print("#"*20)
        for poll in self.session.query(Poll).all():
            print(str(poll.id)+". "+poll.title)
        print("#"*20)

    def getIdAndPoll(self) -> Poll:
        id = int(input("Enter id: "))
        return self.session.query(Poll).filter(Poll.id == id).all()

    def participate(self) -> None:
        poll = self.getIdAndPoll()
        if len(poll) == 0:
            print("Wrong poll id!")
            return
        poll = poll[0]
        print(self.session.query(User).filter(User.email == self.loggedInUser.email).one().participated)
        if poll.id in self.session.query(User).filter(User.email == self.loggedInUser.email).one().participated:
            print("You have already participated in this poll!")
            return
        print("\n".join([str(i+1)+". "+x for i, x in enumerate(poll.options)]))
        vote = int(input("Enter your vote: "))-1
        poll.selOptions[vote] += 1
        self.session.query(User).filter(User.email == self.loggedInUser.email).one().participated.append(poll.id)
        self.session.commit()

    def deletePoll(self) -> None:
        poll = self.getIdAndPoll()
        if len(poll) == 0:
            print("Wrong poll id")
            return
        if poll[0].creator != self.loggedInUser.email:
            print("This poll is not made by you!")
        self.session.delete(poll[0])
        self.session.commit()

    def toggleActive(self) -> None:
        poll = self.getIdAndPoll()
        if len(poll) == 0:
            print("Wrong poll id")
            return
        if poll[0].creator != self.loggedInUser.email:
            print("This poll is not made by you!")
        poll[0].isDisabled = not poll[0].isDisabled
        if poll[0].isDisabled:
            print("Disabled")
        else:
            print("Enabled")
        self.session.commit()

    def showResults(self) -> None:
        poll = self.getIdAndPoll()
        print(poll[0].title+"\n"+"\n".join([str(i)+"- "+x+" --> "+str(poll[0].selOptions[i])+" votes" for i, x in enumerate(poll[0].options)]))

    def showMyPolls(self) -> None:
        print("\n".join([ str(i)+". "+x.title+" "+' Enabled' if x.isDisabled else 'Disabled' for i, x in enumerate(self.session.query(Poll).filter(Poll.creator == self.loggedInUser.email))]))

    def run(self) -> None:
        while not self.quit:
            if self.loggedInUser == None:
                print("1. Login\n2. Signup\n3. Exit")
                cmd = input("Choice: ")
                if cmd == "1":
                    self.login()
                elif cmd == "2":
                    self.signup()
                elif cmd == "3":
                    self.quit = True
                else:
                    print("Invalid choice!")
            else:
                print("1. Create a new poll\n2. List of polls\n3. Participate in a poll\n4. Delete your poll\n5. Activate or deactivate your poll\n6. Poll results\n7. List of your polls\n8. Exit")
                cmd = input("Choice: ")
                if cmd == "1":
                    self.createPoll()
                elif cmd == "2":
                    self.listPolls()
                elif cmd == "3":
                    self.participate()
                elif cmd == "4":
                    self.deletePoll()
                elif cmd == "5":
                    self.toggleActive()
                elif cmd == "6":
                    self.showResults()
                elif cmd == "7":
                    self.showMyPolls()
                elif cmd == "8":
                    self.quit = True
                else:
                    print("Invalid choice!")


cli = Cli()
cli.run()
