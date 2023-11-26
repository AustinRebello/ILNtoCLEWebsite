# Name: Brian Haines
# Date: 11/28/15
# Purpose: Create a script that imports 32 degree data into sql
# Version/ update history:
#        1) 2/21/17- Completed!
#        2) Script imports number of 32 degree days and 32 degree day highs into sql

#######################################
#Import modules required by Acis
import urllib.request as urlL
import json
#######################################
#######################################
#Import plotting tools
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
import datetime
import numpy as np
import math
#######################################
#######################################
#MY SQL Code block
import mysql.connector
cnx = mysql.connector.connect(user='austinrebello', password='mysql',
                              host='localhost',
                              database='climate') 

sites = ["cak","cle","eri","mfd","tol","yng"]

cursor = cnx.cursor()
sql = "DELETE FROM climate.32degree_cak  WHERE Datetime != 0"
cursor.execute(sql)
cnx.commit()
sql = "DELETE FROM climate.32degree_cle  WHERE Datetime != 0"
cursor.execute(sql)
cnx.commit()
sql = "DELETE FROM climate.32degree_eri  WHERE Datetime != 0"
cursor.execute(sql)
cnx.commit()
sql = "DELETE FROM climate.32degree_mfd  WHERE Datetime != 0"
cursor.execute(sql)
cnx.commit()
sql = "DELETE FROM climate.32degree_tol  WHERE Datetime != 0"
cursor.execute(sql)
cnx.commit()
sql = "DELETE FROM climate.32degree_yng  WHERE Datetime != 0"
cursor.execute(sql)
cnx.commit()

#######################################
#######################################
#Set Acis data server
base_url = "http://data.rcc-acis.org/"
#######################################
#Acis WebServices functions
#######################################
def make_request(url,params) :
    req = urlL.Request(url,
    bytes(json.dumps(params), 'utf-8'),
    {"Content-Type":"application/json"})
    try:
        response = urlL.urlopen(req)
        return json.loads(response.read())
    except urlL.HTTPError as error:
        if error.code == 400 : print(error.msg)

def GridData(params) :
    return make_request(base_url+"StnData",params)

###################################################
#M A I N
###################################################
def sqlSite(site):
    
   #Set parameters for data request
    # Number of 32 degree days
    params = {"sid":(site.upper()+"thr"),"sdate":"por","edate":"por","elems":[{"name":"mint","interval":"mly","duration":"mly","reduce":{"reduce":"cnt_le_32"},"maxmissing":0}]}
    
    data = GridData(params)

    # Number of sub 32 degree day highs
    paramsh = {"sid":(site.upper()+"thr"),"sdate":"por","edate":"por","elems":[{"name":"mint","interval":"mly","duration":"mly","reduce":{"reduce":"cnt_le_32"},"maxmissing":0}]}
    
    datah = GridData(paramsh)
    

    # Setup variables for counts
    year = []
    month = []
    year_temp = []
    month_temp = []
    count = []
    counthigh = []
    datetime = []

    #CVG
    for d in data['data']:
        for i in range(0, len(d)):
            if (i == 0):
                year.append(str(d[0]).split('-')[0])
                year_temp = str(d[0]).split('-')[0]
                month.append(str(d[0]).split('-')[1])
                month_temp =(str(d[0]).split('-')[1])
                datetime.append(str(year_temp + month_temp))
                #print datetime
            elif (i == 1):
                count.append(str(d[1]))

    for d1 in datah['data']:
        for i in range(0, len(d1)):
            if (i == 1):
                counthigh.append(str(d1[1]))
                
    for kc in range(len(count)):
        sql_ = "INSERT INTO 32degree_"+site+"(Datetime, year_"+site+", month_"+site+", count_"+site+", counthigh_"+site+") VALUES ( '" + datetime[kc] + "', '" +  year[kc] + "', '" +  month[kc] + "', '" + count[kc] + "', '" + counthigh[kc]+ "')"  
        cursor.execute(sql_)
        cnx.commit()
    
for site in sites:
    sqlSite(site)

# Close Connection
cursor.close()
cnx.close()
