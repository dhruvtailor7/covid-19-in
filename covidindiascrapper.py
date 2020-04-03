# -*- coding: utf-8 -*-
"""covidIndiaScrapper.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/15mGSmPj7vWqJilzQbGL1bSQ2AVF841CB
"""

import time
import requests
from bs4 import BeautifulSoup
from datetime import date
import csv
from datetime import datetime
import json
URL_SMS = 'https://www.sms4india.com/api/v1/sendCampaign'
API_KEY = 'PMEBXICEIKK0KJ8TLZDTHQVD8Z2POC3M'
SECRET = '6S687CBOMMZ4L2UE'

# get request
def sendPostRequest(reqUrl, apiKey, secretKey, useType, phoneNo, senderId, textMessage):
  req_params = {
  'apikey':apiKey,
  'secret':secretKey,
  'usetype':useType,
  'phone': phoneNo,
  'message':textMessage,
  'senderid':senderId
  }
  return requests.post(reqUrl, req_params)

def import_csv(csvfilename):
    data = []
    with open(csvfilename, "r", errors="ignore") as scraped:
        reader = csv.reader(scraped, delimiter=',')
        next(reader);
        for row in reader:
            columns = [int(row[0]), int(row[1]), int(row[2])]
            data.append(columns)
    return data


while True:
    URL = 'https://www.worldometers.info/coronavirus/country/india/'
    ans = []
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    data = import_csv('covid-19-IN.csv')
    prev = data[-1]
    rise_flag = False
    results = soup.find_all(id='maincounter-wrap')
    for res in results:
      res.find('div', class_='maincounter-number')
      ans.append(int(res.find('span').text.replace(",","")))

    for i in range(3):
       if ans[i]!=prev[i]:
         rise_flag = True
         break


    now = datetime.now()
    dt = now.strftime("%d/%m/%Y %H:%M:%S")
    ans.append(dt)

    msg = "Total:"+str(ans[0])+"\nDeath:"+str(ans[1])+"\nRecovered:"+str(ans[2])+"\nRise from last time in Total Case:"+str(ans[0]-prev[0])+"\nRise from last time in Deaths:"+str(ans[1]-prev[1])+"\nRise from last time in Recovered Cases:"+str(ans[2]-prev[2])
    print(msg)
    response = sendPostRequest(URL_SMS, API_KEY, SECRET, 'stage', '+919925511733', '+919925511733', msg )
    print(response.text)

    if rise_flag:
        with open('covid-19-IN.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(ans)
    print(ans)
    time.sleep(3600)





