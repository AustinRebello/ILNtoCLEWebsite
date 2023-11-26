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
import urllib.request as urlL
import json
import datetime
#######################################
#MY SQL Code block
import mysql.connector


cnx = mysql.connector.connect(user='austinrebello', password='mysql',
                              host='localhost',
                              database='climate') 

sites = ["cak","cle","eri","mfd","tol","yng"]

cursor = cnx.cursor()
sql = "DELETE FROM climate.snow_cak  WHERE Datetime != 0"
cursor.execute(sql)
cnx.commit()
sql = "DELETE FROM climate.snow_cle  WHERE Datetime != 0"
cursor.execute(sql)
cnx.commit()
sql = "DELETE FROM climate.snow_eri  WHERE Datetime != 0"
cursor.execute(sql)
cnx.commit()
sql = "DELETE FROM climate.snow_mfd  WHERE Datetime != 0"
cursor.execute(sql)
cnx.commit()
sql = "DELETE FROM climate.snow_tol  WHERE Datetime != 0"
cursor.execute(sql)
cnx.commit()
sql = "DELETE FROM climate.snow_yng  WHERE Datetime != 0"
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
    params = {"sid":site.upper()+"thr","sdate":"por","edate":"por","elems":[{"name":"snow","interval":"mly","duration":"mly","reduce":"sum","maxmissing":1}]}
    
    data = GridData(params)

    # Setup variables for counts
    year = []
    month = []
    sum = []

    for d in data['data']:
        for i in range(0, len(d)):
            if (i == 0):
                year = str(d[0]).split('-')[0]
                month = str(d[0]).split('-')[1]
                datetime = year + month
                #print datetime
            elif (i == 1):
                sum = str(d[1])

        sql = "INSERT INTO snow_"+site+"(Datetime, year_"+site+", month_"+site+", sum_"+site+") VALUES ( '" + datetime + "', '" +  year + "', '" +  month + "', '" + sum + "')"  
        cursor.execute(sql)
        cnx.commit()

for site in sites:
    sqlSite(site)
    
# Close Connection
cursor.close()
cnx.close()