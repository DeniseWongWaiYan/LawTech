from selenium import webdriver
from selenium.webdriver.support.ui import Select
import urllib
import PyPDF2, re 
from StringIO import StringIO
import textract, requests


url ='http://www.hkexnews.hk/listedco/listconews/advancedsearch/search_active_main.aspx'

browser = webdriver.Chrome()
browser.get(url)

StockElem = browser.find_element_by_id('ctl00_txt_stock_code')
StockElem.send_keys('00174')
StockElem.click()

select = Select(browser.find_element_by_id('ctl00_sel_tier_1'))
select.select_by_value('-2')



select = Select(browser.find_element_by_id('ctl00_sel_DateOfReleaseFrom_d'))
select.select_by_value('25')

select = Select(browser.find_element_by_id('ctl00_sel_DateOfReleaseFrom_m'))
select.select_by_value('06')

select = Select(browser.find_element_by_id('ctl00_sel_DateOfReleaseFrom_y'))
select.select_by_value('2007')

#  select the search button
browser.execute_script("document.forms[0].submit()")

from bs4 import BeautifulSoup
import re
import requests

f = browser.page_source
soup = BeautifulSoup(f,'html.parser')
match = re.compile('\.(html|pdf)')

baseurls = []
for link in soup.findAll('a'):
    baseurl = 'http://www.hkexnews.hk'
    try:
        href = link['href']
        if re.search(match, href):
            file = open("newfile.txt", "a")
            file.write(baseurl+href+'\n')
            file.close
            #print ('finished write')
            #print baseurl+href
            baseurls.append(baseurl+href)
    except KeyError:
        pass
   
for baseurl in baseurls:
    print baseurl
    
    response = requests.get(baseurl)
    my_raw_data = response.content

    with open ("my_pdf.pdf", 'wb') as my_data:
        my_data.write(my_raw_data)

    open_pdf_file = open("my_pdf.pdf", 'rb')
    read_pdf = PyPDF2.PdfFileReader(open_pdf_file)


    if read_pdf.isEncrypted:
        read_pdf.decrypt("")
        extract_text = read_pdf.getPage().extractText()
        sentencelist = extract_text.split(".").remove("\n")
        for sentence in sentencelist:
            if 'Gemini' in sentencelist:
                print sentencelist 

    else:
        i = 0
        while i < read_pdf.numPages:
            extract_text = read_pdf.getPage(i).extractText()
            sentencelist = extract_text.split(".")
            for sentence in sentencelist:
                if 'Gemini' in sentence:
                    print sentencelist 
            i += 1
                    



