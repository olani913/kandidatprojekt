import xlwt
import ast
import datetime
import time
import re
import os
import bitlydatahandler
colTime=1
newsEnding = re.compile('.*news\.txt$')
run = True
path = ""

def findMostRecentFile(path):
    year = 0
    month = 0
    day = 0
    timeOfDay = 0
    for file_name in os.listdir(path):
        if(newsEnding.match(file_name)):
            if(int(file_name.split("-")[0]) >= year and int(file_name.split("-")[1]) >= month):
                year = int(file_name.split("-")[0])
                month = int(file_name.split("-")[1])
                if(int(file_name.split("-")[2].split("_")[0]) >= day):
                    day = int(file_name.split("-")[2].split("_")[0])
                    if(int(file_name.split("-")[2].split("_")[1]) > timeOfDay):
                        timeOfDay = int(file_name.split("-")[2].split("_")[1])
                        file_path = os.path.join(path, file_name)
                        if os.path.isfile(file_path):
                            return file_path
    return None
while run:
    if(colTime == 1):
        path = findMostRecentFile("./data/")
        print path
        with open(path, 'r') as file:
            data=file.read().split('\n')
        book = xlwt.Workbook(encoding="utf-8")
        sheet1 = book.add_sheet("Sheet 1")
        sheet1.write(0, 0, "URL")
        print time.asctime(time.localtime(time.time()))
        sheet1.write(0, 1, u'Antal click vid tiden: ' + str(time.asctime(time.localtime(time.time()))))
        tmp=1
        for line in data:
            if line!='':
                dataDict = ast.literal_eval(line)
                url=dataDict["long_url"]
                clicks=dataDict["global_clicks"]
                sheet1.write(tmp, 0, url)
                sheet1.write(tmp, colTime, clicks)
                tmp=tmp+1
    else:
        print path
        sheet1.write(0, colTime, u'Antal click vid tiden: ' + str(time.asctime(time.localtime(time.time()))))
        print time.asctime(time.localtime(time.time()))
        updatedData = bitlydatahandler.updateClicks(path)
        tmp=1
        for line in updatedData:
            if line!='':
                clicks=line["global_clicks"]
                sheet1.write(tmp, colTime, clicks)
                tmp=tmp+1

    book.save("ResultsBitly.xls")
    time.sleep( 10 )
    colTime=colTime+1
    if(colTime > 5):
        run = False
        print "DONE"

