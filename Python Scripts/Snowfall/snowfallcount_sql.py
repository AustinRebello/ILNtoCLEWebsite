### Header ###
# Name: Brian Haines
# Date: 1/24/17
# Purpose: Create a snowfall script that requests snowfall data from xmacis
#          and stores it in mysql
# Version/ update history:
#        1) 1/25/17: Completed scripts to download monthly snowfall totals
#                    and store in mysql
### --- ###

#######################################
#Import modules required by Acis
import urllib2
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
import mysql.connector # Import needed module
cnx = mysql.connector.connect(user='brian.haines', password='mysql', # Login to 198 with username brian.haines
                              host='198.206.42.11',
                              database='climate') 
cursor = cnx.cursor()
# Delete old data from table so primary key error is avioded 
sql = "DELETE FROM climate.snow_cvg  WHERE Datetime != 0"
cursor.execute(sql)
cnx.commit()
sql = "DELETE FROM climate.snow_cmh  WHERE Datetime != 0"
cursor.execute(sql)
cnx.commit()
sql = "DELETE FROM climate.snow_day  WHERE Datetime != 0"
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
    req = urllib2.Request(url,
    json.dumps(params),
    {"Content-Type":"application/json"})
    try:
        response = urllib2.urlopen(req)
        return json.loads(response.read())
    except urllib2.HTTPError as error:
        if error.code == 400 : print error.msg

def GridData(params) :
    return make_request(base_url+"StnData",params)

###################################################
#M A I N
###################################################
if __name__ == "__main__":
    
   #Set parameters for data request
    params_cvg = {"sid":"CVGthr","sdate":"por","edate":"por","elems":[{"name":"snow","interval":"mly","duration":"mly","reduce":"sum","maxmissing":1}]}
    params_day = {"sid":"DAYthr","sdate":"por","edate":"por","elems":[{"name":"snow","interval":"mly","duration":"mly","reduce":"sum","maxmissing":1}]}
    params_cmh = {"sid":"CMHthr","sdate":"por","edate":"por","elems":[{"name":"snow","interval":"mly","duration":"mly","reduce":"sum","maxmissing":1}]}
    
    data_cvg = GridData(params_cvg)
    data_cmh = GridData(params_cmh)
    data_day = GridData(params_day)

    # Setup variables for counts
    year_cvg = []
    month_cvg = []
    count_cvg = []

    year_cmh = []
    month_cmh = []
    count_cmh = []

    year_day = []
    month_day = []
    count_day = []

    #CVG
    for d in data_cvg['data']:
        for i in range(0, len(d)):
            if (i == 0):
                year_cvg = str(d[0]).split('-')[0]
                month_cvg = str(d[0]).split('-')[1]
                datetime = year_cvg + month_cvg
                #print datetime
            elif (i == 1):
                sum_cvg = str(d[1])

        sql_cvg = "INSERT INTO snow_cvg(Datetime, year_cvg, month_cvg, sum_cvg) VALUES ( '" + datetime + "', '" +  year_cvg + "', '" +  month_cvg + "', '" + sum_cvg + "')"  
        cursor.execute(sql_cvg)
        cnx.commit()

    #CMH
    for d in data_cmh['data']:
        for i in range(0, len(d)):
            if (i == 0):
                year_cmh = str(d[0]).split('-')[0]
                month_cmh = str(d[0]).split('-')[1]
                datetime = year_cmh + month_cmh             
            elif (i == 1):
                sum_cmh = str(d[1])

        sql_cmh = "INSERT INTO snow_cmh(Datetime, year_cmh, month_cmh, sum_cmh) VALUES ( '" + datetime + "', '" +  year_cmh + "', '" +  month_cmh + "', '" + sum_cmh + "')"  
        cursor.execute(sql_cmh)
        cnx.commit()

    #DAY
    for d in data_day['data']:
        for i in range(0, len(d)):
            if (i == 0):
                year_day = str(d[0]).split('-')[0]
                month_day = str(d[0]).split('-')[1]
                datetime = year_day + month_day
            elif (i == 1):
                sum_day = str(d[1])

        sql_day = "INSERT INTO snow_day(Datetime, year_day, month_day, sum_day) VALUES ( '" + datetime + "', '" +  year_day + "', '" +  month_day + "', '" + sum_day + "')"  
        cursor.execute(sql_day)
        cnx.commit()

    # Close Connection
    cursor.close()
    cnx.close()
