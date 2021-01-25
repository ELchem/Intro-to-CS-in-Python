# 6.0001/6.00 Problem Set 5 - RSS Feed Filter
# Name:
# Collaborators:
# Time:

import feedparser
import string
import time
import threading
from project_util import translate_html
from mtTkinter import *
from datetime import datetime
import pytz


#-----------------------------------------------------------------------

#======================
# Code for retrieving and parsing
# Google and Yahoo News feeds
# Do not change this code
#======================

def process(url):
    """
    Fetches news items from the rss url and parses them.
    Returns a list of NewsStory-s.
    """
    feed = feedparser.parse(url)
    entries = feed.entries
    ret = []
    for entry in entries:
        guid = entry.guid
        title = translate_html(entry.title)
        link = entry.link
        description = translate_html(entry.description)
        pubdate = translate_html(entry.published)

        try:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %Z")
            pubdate.replace(tzinfo=pytz.timezone("GMT"))
          #  pubdate = pubdate.astimezone(pytz.timezone('EST'))
          #  pubdate.replace(tzinfo=None)
        except ValueError:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %z")

        newsStory = NewsStory(guid, title, description, link, pubdate)
        ret.append(newsStory)
    return ret

#======================
# Data structure design
#======================

# Problem 1

# TODO: NewsStory
class NewsStory(object):
    def __init__(self, guid, title, description, link, pubdate):
        self.guid = guid
        self.title = title
        self.description = description
        self.link = link
        self.pubdate = pubdate
    def get_guid(self):
        return self.guid
    def get_title(self):
        return self.title
    def get_description(self):
        return self.description 
    def get_link(self):
        return self.link
    def get_pubdate(self):
        return self.pubdate
    

#======================
# Triggers
#======================

class Trigger(object):
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        # DO NOT CHANGE THIS!
        raise NotImplementedError

# PHRASE TRIGGERS

# Problem 2
# TODO: PhraseTrigger
class PhraseTrigger(Trigger):
    def __init__(self, phrase):
        self.phrase = phrase.lower()
    def is_phrase_in(self,text):
        punc = string.punctuation
        text_lower = text.lower()
        char_list = []
        for char in text_lower:
            if char in punc:
                char_list.append(' ')
            else:
                char_list.append(char)
        depuncd_str = ''.join(char_list)
        depuncd_str_lst = depuncd_str.split()
        phrase = self.phrase
        phrase_list = phrase.split()
        L = len(phrase_list)
        for x,word in enumerate(depuncd_str_lst): 
            if word == phrase_list[0]:
                if depuncd_str_lst[x:(x+L)] == phrase_list:
                    return True
        return False
    def evaluate (self, story):
        raise NotImplementedError 

# Problem 3
# TODO: TitleTrigger

class TitleTrigger(PhraseTrigger):
    def __init__(self,phrase):
        PhraseTrigger.__init__(self,phrase)
    def evaluate (self,story):
        title = story.get_title()
        return self.is_phrase_in(title)




# Problem 4
# TODO: DescriptionTrigger

class DescriptionTrigger(PhraseTrigger):
    def __init__(self,phrase):
         PhraseTrigger.__init__(self,phrase)
    def evaluate (self,story):
        description = story.get_description()
        return self.is_phrase_in(description)
        


# TIME TRIGGERS

# Problem 5
# TODO: TimeTrigger
# Constructor:
#        Input: Time has to be in EST and in the format of "%d %b %Y %H:%M:%S".
#        Convert time from string to a datetime before saving it as an attribute.

class TimeTrigger(Trigger):
    def __init__(self,time):
        month_dict = {'Jan':1,'Feb':2,'Mar':3,'Apr':4,'May':5,'Jun':6,'Jul':7,'Aug':8,'Sep':9,'Oct':10,'Nov':11,'Dec':12}
        time_list = time.split()
        if len(time_list) >3:
            HMS = time_list[3].split(':')
            date = datetime(int(time_list[2]),month_dict[time_list[1]],
                                 int(time_list[0]),int(HMS[0]),int(HMS[1]),int(HMS[2]))
            self.date = date
            self.datetz = date.replace(tzinfo=pytz.timezone("EST"))
        else:
            date = datetime(int(time_list[2]),month_dict[time_list[1]], int(time_list[0]))
            self.date = date
            self.datetz = date.replace(tzinfo=pytz.timezone("EST"))
    def evaluate(self):
        raise NotImplementedError
        
# Problem 6
# TODO: BeforeTrigger and AfterTrigger
class BeforeTrigger(TimeTrigger):
    def __init__(self,time):
            TimeTrigger.__init__(self,time)
    def evaluate(self,story):
        pubdate = story.get_pubdate()
        if pubdate.utcoffset() == None:
            return pubdate < self.date
        else:
            return pubdate < self.datetz


class AfterTrigger(TimeTrigger):
    def __init__(self,time):
        TimeTrigger.__init__(self,time)
    def evaluate(self,story):
        pubdate = story.get_pubdate()
        if pubdate.utcoffset() == None:
            return pubdate > self.date
        else:
            return pubdate > self.datetz



# COMPOSITE TRIGGERS

# Problem 7
# TODO: NotTrigger

class NotTrigger(Trigger):
    def __init__(self,T):
        self.trigger = T
    def evaluate(self,x): 
        T = self.trigger               
        return not T.evaluate(x)
    

# Problem 8
# TODO: AndTrigger

class AndTrigger(Trigger):
    def __init__(self,T1, T2):
        self.trigger1 = T1
        self.trigger2 = T2
    def evaluate(self,x):
        T1 = self.trigger1
        T2 = self.trigger2
        return T1.evaluate(x) and T2.evaluate(x)

# Problem 9
# TODO: OrTrigger

class OrTrigger(Trigger):
    def __init__(self,T1, T2):
        self.trigger1 = T1
        self.trigger2 = T2
    def evaluate(self,x):
        T1 = self.trigger1
        T2 = self.trigger2
        return T1.evaluate(x) or T2.evaluate(x)

#======================
# Filtering
#======================


#class TestTrue(object):
#    def evaluate(self,story): return True
#class TestFalse(object):
#    def evaluate(self,story): return False
    
# Problem 10
def filter_stories(stories, triggerlist):
    """
    Takes in a list of NewsStory instances.

    Returns: a list of only the stories for which a trigger in triggerlist fires.
    """
    # TODO: Problem 10
    # This is a placeholder
    # (we're just returning all the stories, with no filtering)
    
    for story in stories:
        trig_flag = False
        print(story)
        for trigger in triggerlist:
            if trigger.evaluate(story):
                trig_flag = True
        if trig_flag == False:
            stories.remove(story)            
    return stories

#a = NewsStory('', '', "asfd New York City asfdasdfasdf", '', datetime.now())
#b = NewsStory('', '', "asdfasfd new york city! asfdasdfasdf", '', datetime.now())
#noa = NewsStory('', '', "something somethingnew york city", '', datetime.now())
#nob = NewsStory('', '', "something something new york cities", '', datetime.now())
#
#tt = TestTrue
#tf = TestFalse
#news_list = [a,b,noa,nob]
#Trigger_list = [tf]
#
#filter_stories(news_list,Trigger_list)

#======================
# User-Specified Triggers
#======================
# Problem 11
def read_trigger_config(filename):
    """
    filename: the name of a trigger configuration file

    Returns: a list of trigger objects specified by the trigger configuration
        file.
    """
    # We give you the code to read in the file and eliminate blank lines and
    # comments. You don't need to know how it works for now!
    trigger_file = open(filename, 'r')
    lines = []
    for line in trigger_file:
        line = line.rstrip()
        if not (len(line) == 0 or line.startswith('//')):
            lines.append(line)

    # TODO: Problem 11
    # line is the list of lines that you need to parse and for which you need
    # to build triggers''
    print(lines)
    trigger_dict = {}
    trigger_list = []
    for line in lines:
        line_info = line.split(',')
        if line_info[1] == 'TITLE':
            trigger_dict[line_info[0]] = TitleTrigger(line_info[2])
        elif line_info[1] == 'DESCRIPTION':
            trigger_dict[line_info[0]] = DescriptionTrigger(line_info[2])
        elif line_info[1] == 'AFTER':
            trigger_dict[line_info[0]] = AfterTrigger(line_info[2])
        elif line_info[1] == 'BEFORE':
            trigger_dict[line_info[0]] = BeforeTrigger(line_info[2])
        elif line_info[1] == 'NOT':
            trigger_dict[line_info[0]] = NotTrigger(trigger_dict[line_info[2]])
        elif line_info[1] == 'AND':
            trigger_dict[line_info[0]] = AndTrigger(trigger_dict[line_info[2]],trigger_dict[line_info[3]])
        elif line_info[1] == 'OR':
            trigger_dict[line_info[0]] = OrTrigger(trigger_dict[line_info[2]],trigger_dict[line_info[3]])
        elif line_info[0] == 'ADD':
            for key in line_info[1::]:
                try:
                    trigger_list.append(trigger_dict[key])
                except:
                    print ('ADD command used for undefined triggers')
    return trigger_list
        
     # for now, print it so you see what it contains!


SLEEPTIME = 120 #seconds -- how often we poll

def main_thread(master):
    # A sample trigger list - you might need to change the phrases to correspond
    # to what is currently in the news
    try:
        t1 = TitleTrigger("election")
        t2 = DescriptionTrigger("Trump")
        t3 = DescriptionTrigger("Clinton")
        t4 = AndTrigger(t2, t3)
        triggerlist = [t1, t4]

        # Problem 11
        # TODO: After implementing read_trigger_config, uncomment this line 
        triggerlist = read_trigger_config('triggers.txt')
        print(triggerlist)
        
        # HELPER CODE - you don't need to understand this!
        # Draws the popup window that displays the filtered stories
        # Retrieves and filters the stories from the RSS feeds
        frame = Frame(master)
        frame.pack(side=BOTTOM)
        scrollbar = Scrollbar(master)
        scrollbar.pack(side=RIGHT,fill=Y)

        t = "Google & Yahoo Top News"
        title = StringVar()
        title.set(t)
        ttl = Label(master, textvariable=title, font=("Helvetica", 18))
        ttl.pack(side=TOP)
        cont = Text(master, font=("Helvetica",14), yscrollcommand=scrollbar.set)
        cont.pack(side=BOTTOM)
        cont.tag_config("title", justify='center')
        button = Button(frame, text="Exit", command=root.destroy)
        button.pack(side=BOTTOM)
        guidShown = []
        def get_cont(newstory):
            if newstory.get_guid() not in guidShown:
                cont.insert(END, newstory.get_title()+"\n", "title")
                cont.insert(END, "\n---------------------------------------------------------------\n", "title")
                cont.insert(END, newstory.get_description())
                cont.insert(END, "\n*********************************************************************\n", "title")
                guidShown.append(newstory.get_guid())

        while True:

            print("Polling . . .", end=' ')
            # Get stories from Google's Top Stories RSS news feed
            stories = process("http://news.google.com/news?output=rss")

            # Get stories from Yahoo's Top Stories RSS news feed
            stories.extend(process("http://news.yahoo.com/rss/topstories"))

            stories = filter_stories(stories, triggerlist)

            list(map(get_cont, stories))
            scrollbar.config(command=cont.yview)


            print("Sleeping...")
            time.sleep(SLEEPTIME)

    except Exception as e:
        print(e)


if __name__ == '__main__':
    root = Tk()
    root.title("Some RSS parser")
    t = threading.Thread(target=main_thread, args=(root,))
    t.start()
    root.mainloop()

punct = string.punctuation
x = 'grift%%#boi'
list_x = x.split('#')
y = 'grift%%'
list_y = y.split('%')
print(list_y)