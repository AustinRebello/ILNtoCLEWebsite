# Name: Brian Haines
# Date: 8/11/2015
# Purpose: Create a script that gets monthly data from xmacis and puts it into mysql database
# Version/ update history:
#        1) 8-14-15: Script completed!

#######################################
#Import modules required by Acis
import urllib.request as urlL
import json
#######################################
#######################################
#Import plotting tools
#import matplotlib.pyplot as plt
#import matplotlib.dates as mdates
#import matplotlib.ticker as ticker
import datetime
#import numpy as np
import math
#######################################
#######################################
#MY SQL Code block
import mysql.connector
cnx = mysql.connector.connect(user='austinrebello', password='mysql',  host='localhost', database='climate') 
cursor = cnx.cursor()
sql = "DELETE FROM climate.kcvg_monthly  WHERE Datetime != 0"
cursor.execute(sql)
cnx.commit()
sql = "DELETE FROM climate.kcmh_monthly  WHERE Datetime != 0"
cursor.execute(sql)
cnx.commit()
sql = "DELETE FROM climate.kday_monthly  WHERE Datetime != 0"
cursor.execute(sql)
cnx.commit()
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

def my_round(x):
    return int(x + math.copysign(0.5, x))
###################################################
#M A I N
###################################################
if __name__ == "__main__":
    
   #Set parameters for data request
    params_cvg = {"sid":"CVGthr","sdate":"por","edate":"por","elems":[{"name":"avgt","interval":"mly","duration":"mly","reduce":{"reduce":"mean","add":"mcnt"},"maxmissing":0},{"name":"pcpn","interval":"mly","duration":"mly","reduce":{"reduce":"sum","add":"mcnt"},"maxmissing":0},{"name":"snow","interval":"mly","duration":"mly","reduce":{"reduce":"sum","add":"mcnt"},"maxmissing":0}]}
    params_cmh ={"sid":"CMHthr","sdate":"por","edate":"por","elems":[{"name":"avgt","interval":"mly","duration":"mly","reduce":{"reduce":"mean","add":"mcnt"},"maxmissing":0},{"name":"pcpn","interval":"mly","duration":"mly","reduce":{"reduce":"sum","add":"mcnt"},"maxmissing":0},{"name":"snow","interval":"mly","duration":"mly","reduce":{"reduce":"sum","add":"mcnt"},"maxmissing":0}]}
    params_day ={"sid":"DAYthr","sdate":"por","edate":"por","elems":[{"name":"avgt","interval":"mly","duration":"mly","reduce":{"reduce":"mean","add":"mcnt"},"maxmissing":0},{"name":"pcpn","interval":"mly","duration":"mly","reduce":{"reduce":"sum","add":"mcnt"},"maxmissing":0},{"name":"snow","interval":"mly","duration":"mly","reduce":{"reduce":"sum","add":"mcnt"},"maxmissing":0}]}
    
    data_cvg = GridData(params_cvg)
    data_cmh = GridData(params_cmh)
    data_day = GridData(params_day)
    
    #CVG
    for d in data_cvg['data']:
        for i in range(0, len(d)):
            if (i == 0):
                yearmonth = str(d[0]).split('-')
                year = yearmonth[0]
                month = yearmonth[1]
                datetime = year + month
                #print month, year
            elif (i == 1):
                temp = str(d[1]).split(',')
                temp_avg = str(temp[0].strip(" [\t\n\r u ' "))
                temp_avg_miss = str(temp[1].strip(" ]\t\n\r u ' "))
                #print temp_avg
            elif (i == 2):
                precip = str(d[2]).split(',')
                precip_sum = str(precip[0].strip(" [\t\n\r u ' "))
                precip_avg_miss = str(precip[1].strip(" ]\t\n\r u ' "))
                #print precip_sum
            elif (i == 3):
                snow = str(d[3]).split(',')
                snow_sum = str(snow[0].strip(" [\t\n\r u ' "))
                snow_avg_miss = str(snow[1].strip(" ]\t\n\r u ' "))
                #print snow_sum
        sql_cvg = "INSERT INTO kcvg_monthly(Datetime, Year, Month, Monthly_Temp_Avg, Monthly_Precip_Total, Monthly_Snow_Total) VALUES ( '" + datetime + "', '" +  year + "', '" +  month +"', '" +  temp_avg +"', '" + precip_sum  +"', '" +  snow_sum + "')"  
        print(sql_cvg)
        #cursor.execute(sql_cvg)
        #cnx.commit()

    #CMH
    for d in data_cmh['data']:
        for i in range(0, len(d)):
            if (i == 0):
                yearmonth = str(d[0]).split('-')
                year = yearmonth[0]
                month = yearmonth[1]
                datetime = year + month
                #print month, year
            elif (i == 1):
                temp = str(d[1]).split(',')
                temp_avg = str(temp[0].strip(" [\t\n\r u ' "))
                temp_avg_miss = str(temp[1].strip(" ]\t\n\r u ' "))
                #print temp_avg
            elif (i == 2):
                precip = str(d[2]).split(',')
                precip_sum = str(precip[0].strip(" [\t\n\r u ' "))
                precip_avg_miss = str(precip[1].strip(" ]\t\n\r u ' "))
                #print precip_sum
            elif (i == 3):
                snow = str(d[3]).split(',')
                snow_sum = str(snow[0].strip(" [\t\n\r u ' "))
                snow_avg_miss = str(snow[1].strip(" ]\t\n\r u ' "))
                #print snow_sum
        sql_cmh = "INSERT INTO kcmh_monthly(Datetime, Year, Month, Monthly_Temp_Avg, Monthly_Precip_Total, Monthly_Snow_Total) VALUES ( '" + datetime + "', '" +  year + "', '" +  month +"', '" +  temp_avg +"', '" + precip_sum  +"', '" +  snow_sum + "')"

        #cursor.execute(sql_cmh)
        #cnx.commit()

    #DAY
    for d in data_day['data']:
        for i in range(0, len(d)):
            if (i == 0):
                yearmonth = str(d[0]).split('-')
                year = yearmonth[0]
                month = yearmonth[1]
                datetime = year + month
                #print month, year
            elif (i == 1):
                temp = str(d[1]).split(',')
                temp_avg = str(temp[0].strip(" [\t\n\r u ' "))
                temp_avg_miss = str(temp[1].strip(" ]\t\n\r u ' "))
                #print temp_avg
            elif (i == 2):
                precip = str(d[2]).split(',')
                precip_sum = str(precip[0].strip(" [\t\n\r u ' "))
                precip_avg_miss = str(precip[1].strip(" ]\t\n\r u ' "))
                #print precip_sum
            elif (i == 3):
                snow = str(d[3]).split(',')
                snow_sum = str(snow[0].strip(" [\t\n\r u ' "))
                snow_avg_miss = str(snow[1].strip(" ]\t\n\r u ' "))
                #print snow_sum
        sql_day = "INSERT INTO kday_monthly(Datetime, Year, Month, Monthly_Temp_Avg, Monthly_Precip_Total, Monthly_Snow_Total) VALUES ( '" + datetime + "', '" +  year + "', '" +  month +"', '" +  temp_avg +"', '" + precip_sum  +"', '" +  snow_sum + "')"

        #cursor.execute(sql_day)
        #cnx.commit()

    # Close Connection
    #cursor.close()
    #cnx.close()


