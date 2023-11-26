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
sites = ["cak","cle","eri","mfd","tol","yng"]
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
def sqlSite(site):
    
   #Set parameters for data request
    params_monthly = {"sid":site.upper()+"thr","sdate":"por","edate":"por","elems":[{"name":"avgt","interval":"mly","duration":"mly","reduce":{"reduce":"mean","add":"mcnt"},"maxmissing":0},{"name":"pcpn","interval":"mly","duration":"mly","reduce":{"reduce":"sum","add":"mcnt"},"maxmissing":0},{"name":"snow","interval":"mly","duration":"mly","reduce":{"reduce":"sum","add":"mcnt"},"maxmissing":0}]}
    #params_seasonally ={"sid":site.upper()+"thr","sdate":"por","edate":"por","elems":[{"name":"avgt","interval":"mly","duration":"mly","reduce":{"reduce":"mean","add":"mcnt"},"maxmissing":0},{"name":"pcpn","interval":"mly","duration":"mly","reduce":{"reduce":"sum","add":"mcnt"},"maxmissing":0},{"name":"snow","interval":"mly","duration":"mly","reduce":{"reduce":"sum","add":"mcnt"},"maxmissing":0}]}
    params_yearly ={"sid":site.upper()+"thr","sdate":"por","edate":"por","elems":[{"name":"avgt","interval":[1,0],"duration":12,"reduce":{"reduce":"mean","add":"mcnt"},"maxmissing":0},{"name":"pcpn","interval":[1,0],"duration":12,"reduce":{"reduce":"sum","add":"mcnt"},"maxmissing":0},{"name":"snow","interval":[1,0],"duration":12,"reduce":{"reduce":"sum","add":"mcnt"},"maxmissing":0}]}
    
    #"elems":[{"interval":[1,0],"duration":3,"name":"snow","reduce":{"reduce":"sum","add":"mcnt"},"maxmissing":"1","prec":3}],"sid":"BWIthr 9","sDate":"1850-02","eDate":"2023-02"}
    #https://xmacis.rcc-acis.org/
    
    
    data_monthly = GridData(params_monthly)
    #data_cmh = GridData(params_cmh)
    data_yearly = GridData(params_yearly)
    
    #CVG
    for d in data_monthly['data']:
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
        sql_cvg = "INSERT INTO "+site+"_monthly(Datetime, Year, Month, Monthly_Temp_Avg, Monthly_Precip_Total, Monthly_Snow_Total) VALUES ( '" + datetime + "', '" +  year + "', '" +  month +"', '" +  temp_avg +"', '" + precip_sum  +"', '" +  snow_sum + "')"  
        print(sql_cvg)
        cursor.execute(sql_cvg)
        cnx.commit()

    #CMH
    """for d in data_cmh['data']:
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
        sql_cmh = "INSERT INTO "+site+"_years(Datetime, Year, Season,  Seasonal_Temp_Avg, Seasonal_Precip_Total, Seasonal_Snow_Total) VALUES ( '" + datetime + "', '" +  year + "', '" +  month +"', '" +  temp_avg +"', '" + precip_sum  +"', '" +  snow_sum + "')"

        cursor.execute(sql_cmh)
        cnx.commit()"""

    #DAY
    for d in data_yearly['data']:
        for i in range(0, len(d)):
            if (i == 0):
                yearmonth = str(d[0]).split('-')
                year = yearmonth[0]
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
        sql_day = "INSERT INTO "+site+"_seasonally(Datetime, Year, Yearly_Temp_Avg, Yearly_Precip_Total, Yearly_Snow_Total) VALUES ( '" + datetime + "', '" +  year + "', '" +  temp_avg +"', '" + precip_sum  +"', '" +  snow_sum + "')"

        cursor.execute(sql_day)
        cnx.commit()

    # Close Connection
    cursor.close()
    cnx.close()
    
    
    
for site in sites:
    sqlSite(site)


