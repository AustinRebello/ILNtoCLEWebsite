# Name: Brian Haines
# Modified By: Austin Rebello
# Date: 11/28/15
# Purpose: Code that gets and populates 90 degree sql database
# Version/ update history:
#        1) File completed!
#        2) 11-26-2023: Formatted to Python3 and NWS CLE, made code more dynamic

#######################################
#Import modules required by Acis
import urllib.request as urlL
import json
import mysql.connector
#######################################
#MY SQL Code block

cnx = mysql.connector.connect(user='austinrebello', password='mysql',
                              host='localhost',
                              database='climate')
sites = ["cak","cle","eri","mfd","tol","yng"]


cursor = cnx.cursor()
sql = "DELETE FROM climate.90degree_cak  WHERE Datetime != 0"
cursor.execute(sql)
cnx.commit()
sql = "DELETE FROM climate.90degree_cle  WHERE Datetime != 0"
cursor.execute(sql)
cnx.commit()
sql = "DELETE FROM climate.90degree_eri  WHERE Datetime != 0"
cursor.execute(sql)
cnx.commit()
sql = "DELETE FROM climate.90degree_mfd  WHERE Datetime != 0"
cursor.execute(sql)
cnx.commit()
sql = "DELETE FROM climate.90degree_tol  WHERE Datetime != 0"
cursor.execute(sql)
cnx.commit()
sql = "DELETE FROM climate.90degree_yng  WHERE Datetime != 0"
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
    params = {"sid":site.upper()+"thr","sdate":"por","edate":"por","elems":[{"name":"maxt","interval":"mly","duration":"mly","reduce":{"reduce":"cnt_ge_90"},"maxmissing":0}]}
    
    data = GridData(params)

    # Setup variables for counts
    year = []
    month = []
    count = []



    for d in data['data']:
        for i in range(0, len(d)):
            if (i == 0):
                year = str(d[0]).split('-')[0]
                month = str(d[0]).split('-')[1]
                datetime = year + month
                #print datetime
            elif (i == 1):
                count = str(d[1])

        sql_cvg = "INSERT INTO 90degree_"+site+"(Datetime, year_"+site+", month_"+site+", count_"+site+") VALUES ( '" + datetime + "', '" +  year + "', '" +  month + "', '" + count + "')"  
        cursor.execute(sql_cvg)
        cnx.commit()


for site in sites:
    sqlSite(site)


# Close Connection
cursor.close()
cnx.close()
