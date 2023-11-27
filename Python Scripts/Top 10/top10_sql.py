# Name: Brian Haines
# Modified By: Austin Rebello
# Date: 8/11/2015
# Purpose: Create a script that gets monthly, seasonally and yearly data from xmacis and puts it into mysql database
# Version/ update history:
#        1) 8-14-15: Script completed!
#        2) 11-26-2023: Converted file to Python3 and for CLE uses, and added the functionality to store the seasonally and yearly data

#######################################
#Import modules required by Acis
import urllib.request as urlL
import json
import math
import datetime as dt
import mysql.connector
#######################################
#######################################
#Set Acis data server
base_url = "http://data.rcc-acis.org/"
# Sites in the format of [site, record_start_year]
sites = [["cak", 1887],["cle", 1871],["eri", 1873],["mfd", 1899],["tol", 1871],["yng", 1896]]
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
def sqlSite(site, porYear):
    
    year = dt.date.today().year
    month = dt.date.today().month
    
   #Set parameters for data request
   
    params_monthly = {"sid":site.upper()+"thr","sdate":"por","edate":"por","elems":[{"name":"avgt","interval":"mly","duration":"mly","reduce":{"reduce":"mean","add":"mcnt"},"maxmissing":1},{"name":"pcpn","interval":"mly","duration":"mly","reduce":{"reduce":"sum","add":"mcnt"},"maxmissing":1},{"name":"snow","interval":"mly","duration":"mly","reduce":{"reduce":"sum","add":"mcnt"},"maxmissing":1}]}
    
    if(month < 3):
        params_seasonally_winter  = {"sid":site.upper()+"thr","sdate":str(porYear)+"-02","edate":str(year-1)+"-02","elems":[{"name":"avgt","interval":[1,0],"duration":3,"reduce":{"reduce":"mean","add":"mcnt"},"maxmissing":1},{"name":"pcpn","interval":[1,0],"duration":3,"reduce":{"reduce":"sum","add":"mcnt"},"maxmissing":1},{"name":"snow","interval":[1,0],"duration":3,"reduce":{"reduce":"sum","add":"mcnt"},"maxmissing":1}]}
    else:
        params_seasonally_winter  = {"sid":site.upper()+"thr","sdate":str(porYear)+"-02","edate":str(year)+"-02","elems":[{"name":"avgt","interval":[1,0],"duration":3,"reduce":{"reduce":"mean","add":"mcnt"},"maxmissing":1},{"name":"pcpn","interval":[1,0],"duration":3,"reduce":{"reduce":"sum","add":"mcnt"},"maxmissing":1},{"name":"snow","interval":[1,0],"duration":3,"reduce":{"reduce":"sum","add":"mcnt"},"maxmissing":1}]}
    
    if(month < 6):
        params_seasonally_spring  = {"sid":site.upper()+"thr","sdate":str(porYear)+"-05","edate":str(year-1)+"-05","elems":[{"name":"avgt","interval":[1,0],"duration":3,"reduce":{"reduce":"mean","add":"mcnt"},"maxmissing":1},{"name":"pcpn","interval":[1,0],"duration":3,"reduce":{"reduce":"sum","add":"mcnt"},"maxmissing":1},{"name":"snow","interval":[1,0],"duration":3,"reduce":{"reduce":"sum","add":"mcnt"},"maxmissing":1}]}
    else:
        params_seasonally_spring  = {"sid":site.upper()+"thr","sdate":str(porYear)+"-05","edate":str(year)+"-05","elems":[{"name":"avgt","interval":[1,0],"duration":3,"reduce":{"reduce":"mean","add":"mcnt"},"maxmissing":1},{"name":"pcpn","interval":[1,0],"duration":3,"reduce":{"reduce":"sum","add":"mcnt"},"maxmissing":1},{"name":"snow","interval":[1,0],"duration":3,"reduce":{"reduce":"sum","add":"mcnt"},"maxmissing":1}]}
    
    if(month < 9):
        params_seasonally_summer  = {"sid":site.upper()+"thr","sdate":str(porYear)+"-08","edate":str(year-1)+"-08","elems":[{"name":"avgt","interval":[1,0],"duration":3,"reduce":{"reduce":"mean","add":"mcnt"},"maxmissing":1},{"name":"pcpn","interval":[1,0],"duration":3,"reduce":{"reduce":"sum","add":"mcnt"},"maxmissing":1},{"name":"snow","interval":[1,0],"duration":3,"reduce":{"reduce":"sum","add":"mcnt"},"maxmissing":1}]}
    else:
        params_seasonally_summer  = {"sid":site.upper()+"thr","sdate":str(porYear)+"-08","edate":str(year)+"-08","elems":[{"name":"avgt","interval":[1,0],"duration":3,"reduce":{"reduce":"mean","add":"mcnt"},"maxmissing":1},{"name":"pcpn","interval":[1,0],"duration":3,"reduce":{"reduce":"sum","add":"mcnt"},"maxmissing":1},{"name":"snow","interval":[1,0],"duration":3,"reduce":{"reduce":"sum","add":"mcnt"},"maxmissing":1}]}
    
    if(month < 12):
        params_seasonally_fall  = {"sid":site.upper()+"thr","sdate":str(porYear)+"-11","edate":str(year-1)+"-11","elems":[{"name":"avgt","interval":[1,0],"duration":3,"reduce":{"reduce":"mean","add":"mcnt"},"maxmissing":1},{"name":"pcpn","interval":[1,0],"duration":3,"reduce":{"reduce":"sum","add":"mcnt"},"maxmissing":1},{"name":"snow","interval":[1,0],"duration":3,"reduce":{"reduce":"sum","add":"mcnt"},"maxmissing":1}]}
    else:
        params_seasonally_fall  = {"sid":site.upper()+"thr","sdate":str(porYear)+"-11","edate":str(year)+"-11","elems":[{"name":"avgt","interval":[1,0],"duration":3,"reduce":{"reduce":"mean","add":"mcnt"},"maxmissing":1},{"name":"pcpn","interval":[1,0],"duration":3,"reduce":{"reduce":"sum","add":"mcnt"},"maxmissing":1},{"name":"snow","interval":[1,0],"duration":3,"reduce":{"reduce":"sum","add":"mcnt"},"maxmissing":1}]}
    
    params_yearly = {"sid":site.upper()+"thr","sdate":"por","edate":"por","elems":[{"name":"avgt","interval":[1,0],"duration":12,"reduce":{"reduce":"mean","add":"mcnt"},"maxmissing":1},{"name":"pcpn","interval":[1,0],"duration":12,"reduce":{"reduce":"sum","add":"mcnt"},"maxmissing":1},{"name":"snow","interval":[1,0],"duration":12,"reduce":{"reduce":"sum","add":"mcnt"},"maxmissing":1}]}
    
    #https://xmacis.rcc-acis.org/
    
    
    data_monthly = GridData(params_monthly)
    data_seasonally_spring = GridData(params_seasonally_spring)
    data_seasonally_summer = GridData(params_seasonally_summer)
    data_seasonally_fall = GridData(params_seasonally_fall)
    data_seasonally_winter = GridData(params_seasonally_winter)
    
    seasons = ["SPRING", "SUMMER", "FALL", "WINTER"]
    seasonData = [data_seasonally_spring, data_seasonally_summer, data_seasonally_fall, data_seasonally_winter]
    
    data_yearly = GridData(params_yearly)
    
    #Monthly
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
        sql_cvg = "INSERT INTO monthly_"+site+"(Datetime, Year, Month, Monthly_Temp_Avg, Monthly_Precip_Total, Monthly_Snow_Total) VALUES ( '" + datetime + "', '" +  year + "', '" +  month +"', '" +  temp_avg +"', '" + precip_sum  +"', '" +  snow_sum + "')"  
        cursor.execute(sql_cvg)
        cnx.commit()

    #Seasonally
    for x in range(0, len(seasonData)):
        for d in seasonData[x]['data']:
            for i in range(0, len(d)):
                if (i == 0):
                    yearmonth = str(d[0]).split('-')
                    year = yearmonth[0]
                    datetime = year + seasons[x]
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
            
            sql_cmh = "INSERT INTO seasonally_"+site+"(Datetime, Year, Season,  Seasonal_Temp_Avg, Seasonal_Precip_Total, Seasonal_Snow_Total) VALUES ( '" + datetime + "', '" +  year + "', '"+  seasons[x] +"', '" +  temp_avg +"', '" + precip_sum  +"', '" +  snow_sum + "')"
            cursor.execute(sql_cmh)
            cnx.commit()

    #Yearly
    for d in data_yearly['data']:
        for i in range(0, len(d)):
            if (i == 0):
                yearmonth = str(d[0]).split('-')
                year = yearmonth[0]
                datetime = year
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
        sql_day = "INSERT INTO yearly_"+site+"(Datetime, Year, Yearly_Temp_Avg, Yearly_Precip_Total, Yearly_Snow_Total) VALUES ( '" + datetime + "', '" +  year + "', '" +  temp_avg +"', '" + precip_sum  +"', '" +  snow_sum + "')"

        cursor.execute(sql_day)
        cnx.commit()

#######################################
#MY SQL Code block

cnx = mysql.connector.connect(user='austinrebello', password='mysql',  host='localhost', database='climate') 
cursor = cnx.cursor()

for site in sites:
    
    sql = "DELETE FROM climate.monthly_"+site[0]+"  WHERE Datetime != 0"
    cursor.execute(sql)
    cnx.commit()
    sql = "DELETE FROM climate.seasonally_"+site[0]+"  WHERE Datetime != 0"
    cursor.execute(sql)
    cnx.commit()
    sql = "DELETE FROM climate.yearly_"+site[0]+"  WHERE Datetime != 0"
    cursor.execute(sql)
    cnx.commit()
    sqlSite(site[0], site[1])


# Close Connection
cursor.close()
cnx.close()
    