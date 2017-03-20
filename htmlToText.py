import os
import urllib2
from urllib2 import Request, urlopen, URLError, HTTPError, HTTPRedirectHandler
from bs4 import BeautifulSoup
from bs4 import Comment
import time
import re
from time import strftime

NEWLINE = '\n'

def buildURLList(linkFile):
    urlList = []
    links = open(linkFile,"r")
    lines = links.read()
    links.close()
    for line in lines.split(NEWLINE):
        urlList.append(line)
    return urlList

print "Getting the news"

opener = urllib2.build_opener()
opener.addheaders = [('User-Agent', 'Mozilla/48.0')]

runList = []
runList.append(('training_fake/', './data/links/LinksFakeNews.txt'))
runList.append(('training_real/', './data/links/LinkRealNews.txt'))
runList.append(('LinksUnknownFake/', './data/links/LinksUnknownFake.txt'))
runList.append(('LinksUnknownReal/', './data/links/LinksUnknownReal.txt'))
runList.append(('LinkBBC/', './data/links/LinksBBC.txt'))
runList.append(('LinksFakeExtra/', './data/links/LinksFakeExtra.txt'))

for run, linkFile in runList:
    urlList = buildURLList(linkFile)
    for url in urlList:
        try:
            html = opener.open(url)
        except HTTPError as e:
            print 'The server couldn\'t fulfill the request.'
            print 'Error code: ', e.code
            print url
            print "No articles available here"
        except URLError as e:
            print 'We failed to reach a server.'
            print 'Reason: ', e.reason
            print url
            print "No articles available here"
        else:

            print "The news are here! Starting parsing"
            soup = BeautifulSoup(html, 'html.parser')

            # kill all script and style elements
            for script in soup(["script", "style"]):
                script.extract()    # rip it out

            # get rid of the annoying comment sections
            for comment in soup.findAll("div", class_=re.compile('(C|c)omment.*')):
                comment.extract()

            # get text
            text = soup.get_text()

            # break into lines and remove leading and trailing space on each
            lines = (line.strip() for line in text.splitlines())
            # break multi-headlines into a line each
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            # drop blank lines
            text = NEWLINE.join(chunk for chunk in chunks if chunk)

            print "Article parsed, reading."

            # Stuff should happen here

            print "Commiting to memory"

            path = './data/news/'+ run

            title = ""
            i = 0
            if soup.title is None :
                title = 'noTitle'
            else:
                for part in soup.title.string.split(" "):
                    temp = ""
                    for character in list(part):
                        if character.isalpha():
                            temp = temp + character
                    if len(temp) > 0 and len(title) > 0:
                        title = title + " " + temp
                    elif len(temp) > 0:
                        title = temp
                    i = i + 1
                    if i > 4:
                        break

            file_path_and_name = path+'news ' + title.encode("utf8") + '.txt'
            if not os.path.exists(os.path.dirname(file_path_and_name)):
                try:
                    os.makedirs(os.path.dirname(file_path_and_name))
                except OSError as exc: # Guard against race condition
                    if exc.errno != errno.EEXIST:
                        raise

            savedArticle = open(file_path_and_name,"w")
            for line in text.split(NEWLINE):
                tmp=len(line.split(" "))
                if(tmp>10):
                    line=line+NEWLINE
                    savedArticle.write(line.encode("utf8"))
                    savedArticle.flush()
            savedArticle.close
            print "Article saved"
print "Done"
