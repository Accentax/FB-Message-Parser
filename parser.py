from bs4 import BeautifulSoup as b
from datetime import datetime as dt


def htmlToPy(fileName):
    soup = b(open(fileName))
    dtFormat = '%A, %B %d, %Y at %I:%M%p %Z'
    chatList = []
    for x in soup.find_all(class_='thread'):
        threadList = []
        for y in x.find_all(class_='message'):
            threadList.append(
                Message(
                    y.find(class_='user').string,
                    dt.strptime(y.find(class_='meta').string,dtFormat),
                    y.next_sibling.string
                )
            )
        chatList.append(
            Thread(
                set(x.next_element.split(', ')),
                threadList
            )
        )
    return FbChat(chatList)


class FbChat(object):
    """Contains a list of Threads"""

    def __init__(self, threads):
        self.threads = threads

    def __getitem__(self, key): return self.threads[key]

    def __repr__(self): return '<FbMsg len(threads)={}>'.format(len(self.threads))

    def __len__(self): return len(self.threads)

    def by(self, name):
        return [msg for thread in self if name in thread.participants for msg in thread.by(name)]

    def sentBefore(self, date):
        return [msg for thread in self for msg in thread.sentBefore(date)]

    def sentAfter(self, date):
        return [msg for thread in self for msg in thread.sentAfter(date)]

    def sentBetween(self,beg,end):
        return [msg for thread in self for msg in thread.sentBetween(beg,end)]


class Thread(object):
    """Contains a list of messages, as well as participants"""

    def __init__(self,people,messages):
        self.people = people #included in conversation
        self.messages= messages
        self.participants = {msg.sender for msg in messages} #included, and participated

    def __getitem__(self, key): return self.messages[key]

    def __repr__(self): return '<Thread people={}, len(messages)={}>'.format(self.people,len(self.messages))

    def __str__(self): return '{}\n{}\n'.format(self.people,self.messages)

    def __len__(self): return len(self.messages)

    def by (self, name):
        return [msg for msg in self if msg.sender == name]

    def sentBefore(self,date):
        return [msg for msg in self if msg.date_time < date]

    def sentAfter(self,date):
        return [msg for msg in self if msg.date_time > date]

    def sentBetween(self,beg,end):
        return [msg for msg in self.sentAfter(beg) if msg.date_time < end]


class Message(object):
    """Contains the message text, sender, and date/time"""

    def __init__(self,sender,date_time,text):
        self.sender = sender
        self.date_time = date_time
        self.text = text

    def __repr__(self): return '<Message date_time={} sender={} text={}'.format(self.date_time,self.sender,self.text)

    def __str__(self): return '{}\n{}\n{}\n'.format(self.sender,self.date_time,self.text)
