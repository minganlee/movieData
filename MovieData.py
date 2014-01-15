#!/usr/bin/env python
#coding=utf-8
#@Arthor:minganlee
#@Email:minganlee2010@gmail.com
#@Date:2014-01-14

import os
import sys
import csv
import json
import datetime
import urllib2
import chardet
from bs4 import BeautifulSoup

def getList(url,data):
    '''This function is to get the list data.
    '''
    req = urllib2.Request(url, data)
    req.add_header(u"User-Agent",u"Mozilla/5.0 (Windows NT 6.3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36")
    req.add_header(u"Content-Type",u"application/json; charset=utf-8")
    #Analysis json data
    html = urllib2.urlopen(req).read()
    html= json.loads(html)
    return html[u'd']

def analysisDayList():
    '''This function is to analysis the day list data.
    '''
    dayListUrl = u"http://data.entgroup.cn/BoxOffice/movieData/Movie.aspx/BindDayList"
    #Post with the data and get the day list data
    dayListData = u"{}"
    html = getList(dayListUrl, dayListData)
    html_doc = BeautifulSoup(html, u"lxml")
    #Get the dayList date
    if html_doc.find(u"p"):
        dayListDate = html_doc.find(u"p").get_text()
        dayListDate = dayListDate[:11]
    #Deal with the first of the list
    if html_doc.find(u"table").find(u"table"):
        tb = html_doc.find(u"table").find(u"table")
        tb.replace_with(tb.get_text().strip())
    tr = html_doc.find_all(u"tr")
    if tr[1].get_text().strip() =='':
        del tr[1]
    data = []
    fornum = 0
    for t in tr:
        temp = []
        if fornum == 0:
            temp.append(u"日期".encode(u"GBK"))
        if fornum >0:
            temp.append(dayListDate.encode(u"GBK"))
        fornum += 1
        for tt in t.find_all(u"td"):
            ttData = tt.get_text().strip()
            if u"￥" in ttData:
                ttData = ttData.strip(u'￥')
            temp.append(ttData.encode(u"GBK"))
        temp = tuple(temp)
        data.append(temp)
    
    file_path = os.path.split(sys.argv[0])[0]
    file_path = unicode(file_path,chardet.detect(file_path)[u'encoding'])
    csv_writer = csv.writer(open(os.path.join(file_path, dayListDate+u"MovieDayListData.csv"),u"wb"))    
    csv_writer.writerows(data)

def analysisWeekList():
    weekListUrl = u"http://data.entgroup.cn/boxoffice/movieData/Movie.aspx/BindWeekList"
    #Post with the data and get the week list data
    req = urllib2.Request(u"http://data.entgroup.cn/boxoffice/cn")
    req.add_header(u"User-Agent",u"Mozilla/5.0 (Windows NT 6.3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36")
    html = urllib2.urlopen(req).read()
    html_doc = BeautifulSoup(html)
    week_date_list = html_doc.find(id=u"SelWeek2").find_all(u"option")
    filename = html_doc.find(id=u"SelWeek2").find_all(u"option")[9].get(u"value")+"--"+html_doc.find(id=u"SelWeek2").find_all(u"option")[0].get(u"value")
    data = []
    fornum = 0
    for wd in week_date_list:
        weekdate = wd.get(u"value")
        weekarea = wd.get_text().strip()
        weekListData = u"{ 'dateStr': '" +weekdate+ u"'}"
        html= getList(weekListUrl,weekListData)
        html_doc = BeautifulSoup(html, u"lxml")
        
        if html_doc.find(u"table").find(u"table"):
            tb = html_doc.find(u"table").find(u"table")
            tb.replace_with(tb.get_text().strip())
        
        tr = html_doc.find_all(u"tr")
        if tr[1].get_text().strip() =='':
            del tr[1]
        
        if fornum>0:
            del tr[0]
        for t in tr:
            temp = []
            if fornum == 0:
                temp.append(u"日期".encode(u"GBK"))
            if fornum >0:
                temp.append(weekarea.encode(u"GBK"))
            fornum += 1
            for tt in t.find_all(u"td"):
                ttData = tt.get_text().strip()
                if u"￥" in ttData:
                    ttData = ttData.strip(u'￥')
                temp.append(ttData.encode(u"GBK"))
            temp = tuple(temp)
            data.append(temp)
    file_path = os.path.split(sys.argv[0])[0]
    file_path = unicode(file_path,chardet.detect(file_path)[u'encoding'])
    csv_writer = csv.writer(open(os.path.join(file_path, filename+u"MovieweekListData.csv"),u"wb"))
    csv_writer.writerows(data)

def analysisHistoryList():
    historyListUrl = u"http://data.entgroup.cn/boxoffice/movieData/Movie.aspx/BindHistoryList"
    #Get the page numbers
    req = urllib2.Request(u"http://data.entgroup.cn/boxoffice/cn")
    req.add_header(u"User-Agent",u"Mozilla/5.0 (Windows NT 6.3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36")
    html_pages = urllib2.urlopen(req).read()
    html_doc_pages = BeautifulSoup(html_pages)
    pagenumtemp = html_doc_pages.find(id=u"listbox3_page").find_all(u"span")
    pagenum = []
    for p in pagenumtemp:
        pp = p.get_text().strip()
        pagenum.append(pp)
    #Get the all pages data
    data = []
    fornum = 0
    for pn in pagenum:
        historyListData = u"{'pageNum': "+pn+u"}"
        html = getList(historyListUrl, historyListData)
        html_doc = BeautifulSoup(html, u"lxml")
        tr = html_doc.find_all(u"tr")
        if tr[1].get_text().strip() =='':
            del tr[1]
        if fornum>0:
            del tr[0]
        for t in tr:
            temp = []
            fornum += 1
            for tt in t.find_all(u"td"):
                ttData = tt.get_text().strip()
                if u"￥" in ttData:
                    ttData = ttData.strip(u'￥')
                temp.append(ttData.encode(u"GBK"))
            temp = tuple(temp)
            data.append(temp)
        
    file_path = os.path.split(sys.argv[0])[0]
    file_path = unicode(file_path,chardet.detect(file_path)[u'encoding'])
    csv_writer = csv.writer(open(os.path.join(file_path, str(datetime.datetime.now())[:10]+u"MovieHistoryListData.csv"),u"wb"))    
    csv_writer.writerows(data)
        


def main():
    #Get day list data
    analysisDayList()
    
    #Get week list data
    analysisWeekList()
    
    #Get history list data
    analysisHistoryList()
    

if __name__ == '__main__':
    main()