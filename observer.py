class Post:
    def __init__(self, body: str, title: str, blogname: str) -> None:
        self.body=body
        self.title=title
        self.blogname = blogname

class ISubscriber:
    def showNotif(self, post: Post) -> None:
        raise NotImplementedError

class IBlog:
    def newPost(self, body: str, title: str) -> None:
        raise NotImplementedError

    def subToBlog(self, user: str) -> None:
        raise NotImplementedError

    def notifySubs(self, post: Post) -> None:
        raise NotImplementedError


class VE(ISubscriber):
    counter=0
    def __init__(self) -> None:
        VE.counter+=1
        self.counter=VE.counter
    def showNotif(self, post: Post) -> None:
        print("Salaam haji man mamoor #"+str(self.counter)+" hastam. Title: "+post.title+" az blog: "+post.blogname)

class Viewer(ISubscriber):
    def __init__(self, name: str) -> None:
        self.name = name
    
    def showNotif(self, post: Post) -> None:
        print(self.name+" received post with title: "+post.title)

class Blog(IBlog):
    def __init__(self, blogname: str) -> None:
        self.posts = []
        self.blogname = blogname
        self.subscribers = []

    def newPost(self, body: str, title: str) -> None:
        tmp = Post(body, title, self.blogname)
        self.posts.append(tmp)
        self.notifySubs(tmp)

    def subToBlog(self, user: ISubscriber) -> None:
        if user in self.subscribers:
            print("You are already subbed!")
            return
        self.subscribers.append(user)

    def unsubToBlog(self, user: ISubscriber) -> None:
        if not user in self.subscribers:
            print("You are not subbed!")
            return
        self.subscribers.remove(user)

    def notifySubs(self, post: Post) -> None:
        for sub in self.subscribers:
            sub.showNotif(post)

b1=Blog("Blog one")
b2=Blog("Blog two")
ve=VE()
ve2=VE()
v1=Viewer("First")
v2=Viewer("Second")
v3=Viewer("Third")
b1.subToBlog(v1)
b1.subToBlog(v2)
b2.subToBlog(v2)
b2.subToBlog(v3)
b1.subToBlog(ve)
b1.subToBlog(ve2)
b2.subToBlog(ve)
b2.subToBlog(ve2)
b1.newPost("Salaam","Khoobi??")
b2.newPost("Khodafez","Man raftam!")