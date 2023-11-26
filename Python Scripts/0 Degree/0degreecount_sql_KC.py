# Name: Brian Haines
# Date: 11/28/15
# Purpose: 
# Version/ update history:
#        1) 

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
cursor = cnx.cursor()
sql = "DELETE FROM climate.0degree_cvg  WHERE Datetime != 0"
cursor.execute(sql)
cnx.commit()
sql = "DELETE FROM climate.0degree_cmh  WHERE Datetime != 0"
cursor.execute(sql)
cnx.commit()
sql = "DELETE FROM climate.0degree_day  WHERE Datetime != 0"
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
if __name__ == "__main__":
    
   #Set parameters for data request
    params_cvg = {"sid":"CVGthr","sdate":"por","edate":"por","elems":[{"name":"mint","interval":"mly","duration":"mly","reduce":{"reduce":"cnt_le_0"},"maxmissing":0}]}
    params_cmh = {"sid":"CMHthr","sdate":"por","edate":"por","elems":[{"name":"mint","interval":"mly","duration":"mly","reduce":{"reduce":"cnt_le_0"},"maxmissing":0}]}
    params_day = {"sid":"DAYthr","sdate":"por","edate":"por","elems":[{"name":"mint","interval":"mly","duration":"mly","reduce":{"reduce":"cnt_le_0"},"maxmissing":0}]}
    
    data_cvg = GridData(params_cvg)
    data_cmh = GridData(params_cmh)
    data_day = GridData(params_day)

    paramsh_cvg = {"sid":"CVGthr","sdate":"por","edate":"por","elems":[{"name":"maxt","interval":"mly","duration":"mly","reduce":{"reduce":"cnt_le_0"},"maxmissing":0}]}
    paramsh_cmh = {"sid":"CMHthr","sdate":"por","edate":"por","elems":[{"name":"maxt","interval":"mly","duration":"mly","reduce":{"reduce":"cnt_le_0"},"maxmissing":0}]}
    paramsh_day = {"sid":"DAYthr","sdate":"por","edate":"por","elems":[{"name":"maxt","interval":"mly","duration":"mly","reduce":{"reduce":"cnt_le_0"},"maxmissing":0}]}
    
    datah_cvg = GridData(paramsh_cvg)
    datah_cmh = GridData(paramsh_cmh)
    datah_day = GridData(paramsh_day)


    # Setup variables for counts
    year_cvg = []
    month_cvg = []
    year_cvg_temp = []
    month_cvg_temp = []
    count_cvg = []
    counthigh_cvg = []
    datetime_cvg = []

    year_cmh = []
    month_cmh = []
    year_cmh_temp = []
    month_cmh_temp = []
    count_cmh = []
    counthigh_cmh = []
    datetime_cmh = []

    year_day = []
    month_day = []
    year_day_temp = []
    month_day_temp = []
    count_day = []
    counthigh_day = []
    datetime_day = []

    #CVG
    for d in data_cvg['data']:
        for i in range(0, len(d)):
            if (i == 0):
                year_cvg.append(str(d[0]).split('-')[0])
                year_cvg_temp = str(d[0]).split('-')[0]
                month_cvg.append(str(d[0]).split('-')[1])
                month_cvg_temp =(str(d[0]).split('-')[1])
                datetime_cvg.append(str(year_cvg_temp + month_cvg_temp))
                #print datetime
            elif (i == 1):
                count_cvg.append(str(d[1]))

    for d1 in datah_cvg['data']:
        for i in range(0, len(d1)):
            if (i == 1):
                counthigh_cvg.append(str(d1[1]))
                

    for kc in range(len(count_cvg)):
        sql_cvg = "INSERT INTO 0degree_cvg(Datetime, year_cvg, month_cvg, count_cvg, counthigh_cvg) VALUES ( '" + datetime_cvg[kc] + "', '" +  year_cvg[kc] + "', '" +  month_cvg[kc] + "', '" + count_cvg[kc] + "', '" + counthigh_cvg[kc]+ "')"  
        cursor.execute(sql_cvg)
        cnx.commit()


    #CMH
    for d in data_cmh['data']:
        for i in range(0, len(d)):
            if (i == 0):
                year_cmh.append(str(d[0]).split('-')[0])
                year_cmh_temp = str(d[0]).split('-')[0]
                month_cmh.append(str(d[0]).split('-')[1])
                month_cmh_temp =(str(d[0]).split('-')[1])
                datetime_cmh.append(str(year_cmh_temp + month_cmh_temp))
                #print datetime
            elif (i == 1):
                count_cmh.append(str(d[1]))

    for d1 in datah_cmh['data']:
        for i in range(0, len(d1)):
            if (i == 1):
                counthigh_cmh.append(str(d1[1]))
                

    for kc in range(len(count_cmh)):
        sql_cmh = "INSERT INTO 0degree_cmh(Datetime, year_cmh, month_cmh, count_cmh, counthigh_cmh) VALUES ( '" + datetime_cmh[kc] + "', '" +  year_cmh[kc] + "', '" +  month_cmh[kc] + "', '" + count_cmh[kc] + "', '" + counthigh_cmh[kc]+ "')"  
        cursor.execute(sql_cmh)
        cnx.commit()

    #DAY
    for d in data_day['data']:
        for i in range(0, len(d)):
            if (i == 0):
                year_day.append(str(d[0]).split('-')[0])
                year_day_temp = str(d[0]).split('-')[0]
                month_day.append(str(d[0]).split('-')[1])
                month_day_temp =(str(d[0]).split('-')[1])
                datetime_day.append(str(year_day_temp + month_day_temp))
                #print datetime
            elif (i == 1):
                count_day.append(str(d[1]))

    for d1 in datah_day['data']:
        for i in range(0, len(d1)):
            if (i == 1):
                counthigh_day.append(str(d1[1]))
                

    for kc in range(len(count_day)):
        sql_day = "INSERT INTO 0degree_day(Datetime, year_day, month_day, count_day, counthigh_day) VALUES ( '" + datetime_day[kc] + "', '" +  year_day[kc] + "', '" +  month_day[kc] + "', '" + count_day[kc] + "', '" + counthigh_day[kc]+ "')"  
        cursor.execute(sql_day)
        cnx.commit()


    # Close Connection
    cursor.close()
    cnx.close()
