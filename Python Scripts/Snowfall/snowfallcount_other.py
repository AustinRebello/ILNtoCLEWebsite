### Header ###
# Name: Brian Haines
# Date: 1/25/2017
# Purpose: Create a script that requests snowfall information from my sql
# Version/ update history:
#    1) Finished 1st draft of Snowfall Monthly Script. Items that need attention:
#           - Do I need to include a missing day caveat.... If so should I do max and min differently.
#             Such as do max values with missing days matter?  Min values with missing days DO matter.
#           - How do I handle max and min values that tie? Do I include both years? What about times with
#             10 years that all are the same?
#    2) Working on yearly data and noticed issues:
#           - Smry code does not show ties. Only the latest time of occurence. E.g., CMH measurable snowfall
#    3) Finished draft of script!
#    4) 2-21-17: Updated Script-
#           - Set max missing to 1 for monthly data
#           - Set max missing to 1 for-
#                - Latest seasonal
#                - Latest first
#                - Latest seasonal 1"
#                - Latest calendar
#                - Latest seasonal
### --- ###


#######################################
# Import modules required by Acis
import urllib2
import json
#######################################
#######################################
# Import plotting tools
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
import datetime
import time
import numpy as np
import math
import mysql.connector
import pdfkit
#######################################
# Set Acis data server
base_url = "http://data.rcc-acis.org/"
#######################################
# Acis WebServices functions
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

def my_round(x):
    return int(x + math.copysign(0.5, x))
###################################################
# M A I N
###################################################
if __name__ == "__main__":
    ### Defined Constants ###
    degree_sign= u'\N{DEGREE SIGN}' # The symbol for degrees
    mydate = datetime.datetime.now()
    cm = mydate.strftime("%B") # Current month
    cy = mydate.strftime("%Y") # Current month
    current_date = (time.strftime("%Y-%m-%d")) # Current date
    star_needed_least_cvg = [] # Do I need a star besides that values to indicate multiple years with that value
    star_needed_least_day = [] # Do I need a star besides that values to indicate multiple years with that value
    star_needed_least_cmh = [] # Do I need a star besides that values to indicate multiple years with that value
    
    # mysql constants #
    cnx = mysql.connector.connect(user='brian.haines', password='mysql', # Login to 198 with username brian.haines
                              host='198.206.42.11',
                              database='climate')
    cursor = cnx.cursor(buffered=True)
    # - #
    
    ### --- ###

    
    ### Ouput files for html ###
    # Monthly Output files
    output_file_cvg_month = 'X:/Users/ILN_Common/1-BrianandKristen/ClimateWebpage/PDFTxtFiles/SnowSum/SnowSumMonth_cvg.html' # CVG output file path
    output_file_day_month = 'X:/Users/ILN_Common/1-BrianandKristen/ClimateWebpage/PDFTxtFiles/SnowSum/SnowSumMonth_day.html' # DAY output file path
    output_file_cmh_month = 'X:/Users/ILN_Common/1-BrianandKristen/ClimateWebpage/PDFTxtFiles/SnowSum/SnowSumMonth_cmh.html' # CMH output file path

    # Yearly Output files
    output_file_cvg_year = 'X:/Users/ILN_Common/1-BrianandKristen/ClimateWebpage/PDFTxtFiles/SnowSum/SnowSumYear_cvg.html' # CVG output file path
    output_file_day_year = 'X:/Users/ILN_Common/1-BrianandKristen/ClimateWebpage/PDFTxtFiles/SnowSum/SnowSumYear_day.html' # DAY output file path
    output_file_cmh_year = 'X:/Users/ILN_Common/1-BrianandKristen/ClimateWebpage/PDFTxtFiles/SnowSum/SnowSumYear_cmh.html' # CMH output file path
    ### --- ###
    
   
    ### Step 1: Obtain data from XMACIS/ mysql and format ###

    # Most snowfall in a month- CVG #
    cvg_month_totals = []
    # Get most snowfall in a month 
    month_number = ('10', '11', '12', '01', '02', '03', '04', '05')
    for monum in range(len(month_number)):
        #print str(month_number[monum])
        query_cvg = ("SELECT year_cvg, sum_cvg FROM climate.snow_cvg where month_cvg ='"+str(month_number[monum])+"' ORDER BY sum_cvg+0 DESC, year_cvg DESC;")
        #print query_cvg
        cursor.execute(query_cvg)
        row_cvg = cursor.fetchone()
        #print ( str(month_number[monum]) + str(row_cvg) )
        cvg_month_totals.append(str(month_number[monum]) + "," + str(row_cvg))
    # - #
    
    # Most snowfall in a month- DAY #
    day_month_totals = []
    for monum in range(len(month_number)):
        query_day = ("SELECT year_day, sum_day FROM climate.snow_day where month_day ='"+str(month_number[monum])+"' ORDER BY sum_day+0 DESC, year_day DESC;")
        cursor.execute(query_day)
        row_day = cursor.fetchone()
        day_month_totals.append(str(month_number[monum]) + "," + str(row_day))
    # - #
    
    # Most snowfall in a month- CMH #
    cmh_month_totals = []
    for monum in range(len(month_number)):
        query_cmh = ("SELECT year_cmh, sum_cmh FROM climate.snow_cmh where month_cmh ='"+str(month_number[monum])+"' ORDER BY sum_cmh+0 DESC, year_cmh DESC;")
        cursor.execute(query_cmh)
        row_cmh = cursor.fetchone()
        cmh_month_totals.append(str(month_number[monum]) + "," + str(row_cmh))
    # - #

    # Least snowfall in a month- CVG #
    cvg_least_month_totals = []
    # Get most snowfall in a month 
    month_number = ('10', '11', '12', '01', '02', '03', '04', '05')
    for monum in range(len(month_number)):
        #print str(month_number[monum])
        query_cvg = ("SELECT year_cvg, sum_cvg FROM climate.snow_cvg where month_cvg ='"+str(month_number[monum])+"' and sum_cvg !='M' ORDER BY sum_cvg+1, sum_cvg asc, year_cvg desc;")
        #print query_cvg
        cursor.execute(query_cvg)
        row_cvg = cursor.fetchmany(size=2)
        if row_cvg[0][1] == row_cvg[1][1]:
            star_needed_least_cvg.append(1)
        else:
            star_needed_least_cvg.append(0) 
        #print ( str(month_number[monum]) + str(row_cvg) )
        cvg_least_month_totals.append(str(month_number[monum]) + "," + str(row_cvg))
    # - #
    
    # Least snowfall in a month- DAY #
    day_least_month_totals = []
    # Get most snowfall in a month 
    month_number = ('10', '11', '12', '01', '02', '03', '04', '05')
    for monum in range(len(month_number)):
        #print str(month_number[monum])
        query_day = ("SELECT year_day, sum_day FROM climate.snow_day where month_day ='"+str(month_number[monum])+"' and sum_day !='M' ORDER BY sum_day+1, sum_day asc, year_day desc;")
        #print query_day
        cursor.execute(query_day)
        row_day = cursor.fetchmany(size=2)
        if row_day[0][1] == row_day[1][1]:
            star_needed_least_day.append(1)
        else:
            star_needed_least_day.append(0) 
        #print ( str(month_number[monum]) + str(row_day) )
        day_least_month_totals.append(str(month_number[monum]) + "," + str(row_day))
    # - #

    # Least snowfall in a month- CMH #
    cmh_least_month_totals = []
    # Get most snowfall in a month 
    month_number = ('10', '11', '12', '01', '02', '03', '04', '05')
    for monum in range(len(month_number)):
        #print str(month_number[monum])
        query_cmh = ("SELECT year_cmh, sum_cmh FROM climate.snow_cmh where month_cmh ='"+str(month_number[monum])+"' and sum_cmh !='M' ORDER BY sum_cmh+1, sum_cmh asc, year_cmh desc;")
        #print query_cmh
        cursor.execute(query_cmh)
        row_cmh = cursor.fetchmany(size=2)
        if row_cmh[0][1] == row_cmh[1][1]:
            star_needed_least_cmh.append(1)
        else:
            star_needed_least_cmh.append(0) 
        #print ( str(month_number[monum]) + str(row_cmh) )
        cmh_least_month_totals.append(str(month_number[monum]) + "," + str(row_cmh))
    # - #

    ### --- ###

    ### Parameters for data request ###
    # Earliest measurable snowfall- CVG
    earliest_snow_cvg = {"sid":"cvgthr","sdate":"1891-07-31","edate":"por","elems":[{"name":"snow","interval":[1,0,0],"duration":"std","season_start":"8-1","reduce":{"reduce":"first_ge_0.1","add":"value"},"smry":"min"}]};
    data_earliest_snow_cvg = GridData(earliest_snow_cvg) # Returned data from request
    date_earliest_snow_cvg = str(data_earliest_snow_cvg['smry'][0]) # Display year of earliest snow. Using dict key of smry. Keys are found data_earliest_snow_cvg.viewkeys() and meta, data, smry
    value1_earliest_snow_cvg = data_earliest_snow_cvg['data'][(int(str(data_earliest_snow_cvg['smry'][0])[0:4])+1)-1891] # Take the year of the earliest snow then subtract from sdate and add 1 year back
    value_earliest_snow_cvg = str(value1_earliest_snow_cvg[1][1])
    # - #
    # Earliest measurable snowfall- DAY
    earliest_snow_day = {"sid":"daythr","sdate":"1893-07-31","edate":"por","elems":[{"name":"snow","interval":[1,0,0],"duration":"std","season_start":"8-1","reduce":{"reduce":"first_ge_0.1","add":"value"},"smry":"min"}]};
    data_earliest_snow_day = GridData(earliest_snow_day) # Returned data from request
    date_earliest_snow_day = str(data_earliest_snow_day['smry'][0]) # Display year of earliest snow. Using dict key of smry. Keys are found data_earliest_snow_cvg.viewkeys() and meta, data, smry
    value1_earliest_snow_day = data_earliest_snow_day['data'][(int(str(data_earliest_snow_day['smry'][0])[0:4])+1)-1893] # Take the year of the earliest snow then subtract from sdate and add 1 year back
    value_earliest_snow_day = str(value1_earliest_snow_day[1][1])
    # - #
    # Earliest measurable snowfall- CMH
    earliest_snow_cmh = {"sid":"cmhthr","sdate":"1884-07-31","edate":"por","elems":[{"name":"snow","interval":[1,0,0],"duration":"std","season_start":"8-1","reduce":{"reduce":"first_ge_0.1","add":"value"},"smry":"min"}]};
    data_earliest_snow_cmh = GridData(earliest_snow_cmh) # Returned data from request
    date_earliest_snow_cmh = str(data_earliest_snow_cmh['smry'][0]) # Display year of earliest snow. Using dict key of smry. Keys are found data_earliest_snow_cvg.viewkeys() and meta, data, smry
    value1_earliest_snow_cmh = data_earliest_snow_cmh['data'][(int(str(data_earliest_snow_cmh['smry'][0])[0:4])+1)-1884] # Take the year of the earliest snow then subtract from sdate and add 1 year back
    value_earliest_snow_cmh = str(value1_earliest_snow_cmh[1][1])
    # - #

    # Latest First measurable snowfall- CVG
    latest_earliest_snow_cvg = {"sid":"cvgthr","sdate":"1891-07-31","edate":"por","elems":[{"name":"snow","interval":[1,0,0],"duration":"std","season_start":"8-1","reduce":{"reduce":"first_ge_0.1","add":"value"},"smry":"max","maxmissing":1}]};
    data_latest_earliest_snow_cvg = GridData(latest_earliest_snow_cvg) # Returned data from request
    date_latest_earliest_snow_cvg = str(data_latest_earliest_snow_cvg['smry'][0]) # Display year of latest_earliest snow. Using dict key of smry. Keys are found data_latest_earliest_snow_cvg.viewkeys() and meta, data, smry
    value1_latest_earliest_snow_cvg = data_latest_earliest_snow_cvg['data'][(int(str(data_latest_earliest_snow_cvg['smry'][0])[0:4]))-1891] # Take the year of the latest_earliest snow then subtract from sdate and add 1 year back
    value_latest_earliest_snow_cvg = str(value1_latest_earliest_snow_cvg[1][1])
    # - #
    # Latest First measurable snowfall- DAY
    latest_earliest_snow_day = {"sid":"daythr","sdate":"1893-07-31","edate":"por","elems":[{"name":"snow","interval":[1,0,0],"duration":"std","season_start":"8-1","reduce":{"reduce":"first_ge_0.1","add":"value"},"smry":"max","maxmissing":1}]};
    data_latest_earliest_snow_day = GridData(latest_earliest_snow_day) # Returned data from request
    date_latest_earliest_snow_day = str(data_latest_earliest_snow_day['smry'][0]) # Display year of latest_earliest snow. Using dict key of smry. Keys are found data_latest_earliest_snow_cvg.viewkeys() and meta, data, smry
    value1_latest_earliest_snow_day = data_latest_earliest_snow_day['data'][(int(str(data_latest_earliest_snow_day['smry'][0])[0:4]))-1893] # Take the year of the latest_earliest snow then subtract from sdate and add 1 year back
    value_latest_earliest_snow_day = str(value1_latest_earliest_snow_day[1][1])
    # - #
    # Latest First measurable snowfall- CMH
    latest_earliest_snow_cmh = {"sid":"cmhthr","sdate":"1884-07-31","edate":"por","elems":[{"name":"snow","interval":[1,0,0],"duration":"std","season_start":"8-1","reduce":{"reduce":"first_ge_0.1","add":"value"},"smry":"max","maxmissing":1}]};
    data_latest_earliest_snow_cmh = GridData(latest_earliest_snow_cmh) # Returned data from request
    date_latest_earliest_snow_cmh = str(data_latest_earliest_snow_cmh['smry'][0]) # Display year of latest_earliest snow. Using dict key of smry. Keys are found data_latest_earliest_snow_cvg.viewkeys() and meta, data, smry
    value1_latest_earliest_snow_cmh = data_latest_earliest_snow_cmh['data'][(int(str(data_latest_earliest_snow_cmh['smry'][0])[0:4]))-1884] # Take the year of the latest_earliest snow then subtract from sdate and add 1 year back
    value_latest_earliest_snow_cmh = str(value1_latest_earliest_snow_cmh[1][1])
    # - #

    # Normal First measurable snowfall- CVG
    normal_first_snow_cvg = {"sid":"cvgthr","sdate":"1981-07-31","edate":"2010-07-31","elems":[{"name":"snow","interval":[1,0,0],"duration":"std","season_start":"8-1","reduce":{"reduce":"first_ge_0.1","add":"value"},"smry":"mean"}]};
    data_normal_first_snow_cvg = GridData(normal_first_snow_cvg) # Returned data from request
    date_normal_first_snow_cvg = str(data_normal_first_snow_cvg['smry'][0]) # Display year of latest_earliest snow. Using dict key of smry. Keys are found data_latest_earliest_snow_cvg.viewkeys() and meta, data, smry
    # - #
    # Normal First measurable snowfall- DAY
    normal_first_snow_day = {"sid":"daythr","sdate":"1981-07-31","edate":"2010-07-31","elems":[{"name":"snow","interval":[1,0,0],"duration":"std","season_start":"8-1","reduce":{"reduce":"first_ge_0.1","add":"value"},"smry":"mean"}]};
    data_normal_first_snow_day = GridData(normal_first_snow_day) # Returned data from request
    date_normal_first_snow_day = str(data_normal_first_snow_day['smry'][0]) # Display year of latest_earliest snow. Using dict key of smry. Keys are found data_latest_earliest_snow_cvg.viewkeys() and meta, data, smry
    # - #
    # Normal First measurable snowfall- CMH
    normal_first_snow_cmh = {"sid":"cmhthr","sdate":"1981-07-31","edate":"2010-07-31","elems":[{"name":"snow","interval":[1,0,0],"duration":"std","season_start":"8-1","reduce":{"reduce":"first_ge_0.1","add":"value"},"smry":"mean"}]};
    data_normal_first_snow_cmh = GridData(normal_first_snow_cmh) # Returned data from request
    date_normal_first_snow_cmh = str(data_normal_first_snow_cmh['smry'][0]) # Display year of latest_earliest snow. Using dict key of smry. Keys are found data_latest_earliest_snow_cvg.viewkeys() and meta, data, smry
    # - #

    # Normal First 1" snowfall- CVG
    normal_firstmeasure_snow_cvg = {"sid":"cvgthr","sdate":"1981-07-31","edate":"2010-07-31","elems":[{"name":"snow","interval":[1,0,0],"duration":"std","season_start":"8-1","reduce":{"reduce":"first_ge_1.0","add":"value"},"smry":"mean"}]};
    data_normal_firstmeasure_snow_cvg = GridData(normal_firstmeasure_snow_cvg) # Returned data from request
    date_normal_firstmeasure_snow_cvg = str(data_normal_firstmeasure_snow_cvg['smry'][0]) # Display year of latest_earliest snow. Using dict key of smry. Keys are found data_latest_earliest_snow_cvg.viewkeys() and meta, data, smry
    # - #
    # Normal First 1" snowfall- DAY
    normal_firstmeasure_snow_day = {"sid":"daythr","sdate":"1981-07-31","edate":"2010-07-31","elems":[{"name":"snow","interval":[1,0,0],"duration":"std","season_start":"8-1","reduce":{"reduce":"first_ge_1.0","add":"value"},"smry":"mean"}]};
    data_normal_firstmeasure_snow_day = GridData(normal_firstmeasure_snow_day) # Returned data from request
    date_normal_firstmeasure_snow_day = str(data_normal_firstmeasure_snow_day['smry'][0]) # Display year of latest_earliest snow. Using dict key of smry. Keys are found data_latest_earliest_snow_cvg.viewkeys() and meta, data, smry
    # - #
    # Normal First 1" snowfall- CMH
    normal_firstmeasure_snow_cmh = {"sid":"cmhthr","sdate":"1981-07-31","edate":"2010-07-31","elems":[{"name":"snow","interval":[1,0,0],"duration":"std","season_start":"8-1","reduce":{"reduce":"first_ge_1.0","add":"value"},"smry":"mean"}]};
    data_normal_firstmeasure_snow_cmh = GridData(normal_firstmeasure_snow_cmh) # Returned data from request
    date_normal_firstmeasure_snow_cmh = str(data_normal_firstmeasure_snow_cmh['smry'][0]) # Display year of latest_earliest snow. Using dict key of smry. Keys are found data_latest_earliest_snow_cvg.viewkeys() and meta, data, smry
    # - #

    # Latest Seasonal Measurable Snow- CVG
    latest_snow_cvg = {"sid":"cvgthr","sdate":"1891-07-31","edate":"por","elems":[{"name":"snow","interval":[1,0,0],"duration":"std","season_start":"8-1","reduce":{"reduce":"last_ge_0.1","add":"value"},"smry":"max","maxmissing":1}]};
    data_latest_snow_cvg = GridData(latest_snow_cvg) # Returned data from request
    date_latest_snow_cvg = str(data_latest_snow_cvg['smry'][0]) # Display year of earliest snow. Using dict key of smry. Keys are found data_earliest_snow_cvg.viewkeys() and meta, data, smry
    value1_latest_snow_cvg = data_latest_snow_cvg['data'][(int(str(data_latest_snow_cvg['smry'][0])[0:4]))-1891] # Take the year of the earliest snow then subtract from sdate and add 1 year back
    value_latest_snow_cvg = str(value1_latest_snow_cvg[1][1])
    # - #
    # Latest Seasonal Measurable Snow- DAY
    latest_snow_day = {"sid":"daythr","sdate":"1893-07-31","edate":"por","elems":[{"name":"snow","interval":[1,0,0],"duration":"std","season_start":"8-1","reduce":{"reduce":"last_ge_0.1","add":"value"},"smry":"max","maxmissing":1}]};
    data_latest_snow_day = GridData(latest_snow_day) # Returned data from request
    date_latest_snow_day = str(data_latest_snow_day['smry'][0]) # Display year of earliest snow. Using dict key of smry. Keys are found data_earliest_snow_cvg.viewkeys() and meta, data, smry
    value1_latest_snow_day = data_latest_snow_day['data'][(int(str(data_latest_snow_day['smry'][0])[0:4]))-1893] # Take the year of the earliest snow then subtract from sdate and add 1 year back
    value_latest_snow_day = str(value1_latest_snow_day[1][1])
    # - #
    # Latest Seasonal Measurable Snow- CMH
    latest_snow_cmh = {"sid":"cmhthr","sdate":"1884-07-31","edate":"por","elems":[{"name":"snow","interval":[1,0,0],"duration":"std","season_start":"8-1","reduce":{"reduce":"last_ge_0.1","add":"value"},"smry":"max","maxmissing":1}]};
    data_latest_snow_cmh = GridData(latest_snow_cmh) # Returned data from request
    date_latest_snow_cmh = str(data_latest_snow_cmh['smry'][0]) # Display year of earliest snow. Using dict key of smry. Keys are found data_earliest_snow_cvg.viewkeys() and meta, data, smry
    value1_latest_snow_cmh = data_latest_snow_cmh['data'][(int(str(data_latest_snow_cmh['smry'][0])[0:4]))-1884] # Take the year of the earliest snow then subtract from sdate and add 1 year back
    value_latest_snow_cmh = str(value1_latest_snow_cmh[1][1])
    # - #

    # Latest Seasonal 1" Snow- CVG
    latestone_snow_cvg = {"sid":"cvgthr","sdate":"1891-07-31","edate":"por","elems":[{"name":"snow","interval":[1,0,0],"duration":"std","season_start":"8-1","reduce":{"reduce":"last_ge_1.0","add":"value"},"smry":"max","maxmissing":1}]};
    data_latestone_snow_cvg = GridData(latestone_snow_cvg) # Returned data from request
    date_latestone_snow_cvg = str(data_latestone_snow_cvg['smry'][0]) # Display year of earliest snow. Using dict key of smry. Keys are found data_earliest_snow_cvg.viewkeys() and meta, data, smry
    value1_latestone_snow_cvg = data_latestone_snow_cvg['data'][(int(str(data_latestone_snow_cvg['smry'][0])[0:4]))-1891] # Take the year of the earliest snow then subtract from sdate and add 1 year back
    value_latestone_snow_cvg = str(value1_latestone_snow_cvg[1][1])
    # - #
    # Latest Seasonal 1" Snow- DAY
    latestone_snow_day = {"sid":"daythr","sdate":"1893-07-31","edate":"por","elems":[{"name":"snow","interval":[1,0,0],"duration":"std","season_start":"8-1","reduce":{"reduce":"last_ge_1.0","add":"value"},"smry":"max","maxmissing":1}]};
    data_latestone_snow_day = GridData(latestone_snow_day) # Returned data from request
    date_latestone_snow_day = str(data_latestone_snow_day['smry'][0]) # Display year of earliest snow. Using dict key of smry. Keys are found data_earliest_snow_cvg.viewkeys() and meta, data, smry
    value1_latestone_snow_day = data_latestone_snow_day['data'][(int(str(data_latestone_snow_day['smry'][0])[0:4]))-1893] # Take the year of the earliest snow then subtract from sdate and add 1 year back
    value_latestone_snow_day = str(value1_latestone_snow_day[1][1])
    # - #
    # Latest Seasonal 1" Snow- CMH
    latestone_snow_cmh = {"sid":"cmhthr","sdate":"1884-07-31","edate":"por","elems":[{"name":"snow","interval":[1,0,0],"duration":"std","season_start":"8-1","reduce":{"reduce":"last_ge_1.0","add":"value"},"smry":"max","maxmissing":1}]};
    data_latestone_snow_cmh = GridData(latestone_snow_cmh) # Returned data from request
    date_latestone_snow_cmh = str(data_latestone_snow_cmh['smry'][0]) # Display year of earliest snow. Using dict key of smry. Keys are found data_earliest_snow_cvg.viewkeys() and meta, data, smry
    value1_latestone_snow_cmh = data_latestone_snow_cmh['data'][(int(str(data_latestone_snow_cmh['smry'][0])[0:4]))-1884] # Take the year of the earliest snow then subtract from sdate and add 1 year back
    value_latestone_snow_cmh = str(value1_latestone_snow_cmh[1][1])
    # - #

    # Earliest Last Seasonal Measurable Snow- CVG
    earliestlatest_snow_cvg = {"sid":"cvgthr","sdate":"1891-07-31","edate":"por","elems":[{"name":"snow","interval":[1,0,0],"duration":"std","season_start":"8-1","reduce":{"reduce":"last_ge_0.1","add":"value"},"smry":"min","maxmissing":1}]};
    data_earliestlatest_snow_cvg = GridData(earliestlatest_snow_cvg) # Returned data from request
    date_earliestlatest_snow_cvg = str(data_earliestlatest_snow_cvg['smry'][0]) # Display year of earliest snow. Using dict key of smry. Keys are found data_earliest_snow_cvg.viewkeys() and meta, data, smry
    value1_earliestlatest_snow_cvg = data_earliestlatest_snow_cvg['data'][(int(str(data_earliestlatest_snow_cvg['smry'][0])[0:4]))-1891] # Take the year of the earliest snow then subtract from sdate and add 1 year back
    value_earliestlatest_snow_cvg = str(value1_earliestlatest_snow_cvg[1][1])
    # - #
    # Earliest Last Seasonal Measurable Snow- DAY
    earliestlatest_snow_day = {"sid":"daythr","sdate":"1893-07-31","edate":"por","elems":[{"name":"snow","interval":[1,0,0],"duration":"std","season_start":"8-1","reduce":{"reduce":"last_ge_0.1","add":"value"},"smry":"min","maxmissing":1}]};
    data_earliestlatest_snow_day = GridData(earliestlatest_snow_day) # Returned data from request
    date_earliestlatest_snow_day = str(data_earliestlatest_snow_day['smry'][0]) # Display year of earliest snow. Using dict key of smry. Keys are found data_earliest_snow_cvg.viewkeys() and meta, data, smry
    value1_earliestlatest_snow_day = data_earliestlatest_snow_day['data'][(int(str(data_earliestlatest_snow_day['smry'][0])[0:4]))-1893] # Take the year of the earliest snow then subtract from sdate and add 1 year back
    value_earliestlatest_snow_day = str(value1_earliestlatest_snow_day[1][1])
    # - #
    # Earliest Last Seasonal Measurable Snow- CMH
    earliestlatest_snow_cmh = {"sid":"cmhthr","sdate":"1884-07-31","edate":"por","elems":[{"name":"snow","interval":[1,0,0],"duration":"std","season_start":"8-1","reduce":{"reduce":"last_ge_0.1","add":"value"},"smry":"min","maxmissing":1}]};
    data_earliestlatest_snow_cmh = GridData(earliestlatest_snow_cmh) # Returned data from request
    date_earliestlatest_snow_cmh = str(data_earliestlatest_snow_cmh['smry'][0]) # Display year of earliest snow. Using dict key of smry. Keys are found data_earliest_snow_cvg.viewkeys() and meta, data, smry
    value1_earliestlatest_snow_cmh = data_earliestlatest_snow_cmh['data'][(int(str(data_earliestlatest_snow_cmh['smry'][0])[0:4]))-1884] # Take the year of the earliest snow then subtract from sdate and add 1 year back
    value_earliestlatest_snow_cmh = str(value1_earliestlatest_snow_cmh[1][1])
    # - #

    # Most in a calendar year- CVG
    most_calendaryear_snow_cvg = {"sid":"cvgthr","sdate":"por","edate":"por","elems":[{"name":"snow","interval":"yly","duration":"yly","reduce":"sum","smry":{"reduce":"max","add":"date"}}]};
    data_most_calendaryear_snow_cvg = GridData(most_calendaryear_snow_cvg) # Returned data from request
    date_most_snow_cvg = str(data_most_calendaryear_snow_cvg['smry'][0][1]) # Display year of earliest snow. Using dict key of smry. Keys are found data_earliest_snow_cvg.viewkeys() and meta, data, smry
    value_most_snow_cvg = str(data_most_calendaryear_snow_cvg['smry'][0][0]) # Take the year of the earliest snow then subtract from sdate and add 1 year back
    # - #
    # Most in a calendar year- DAY
    most_calendaryear_snow_day = {"sid":"daythr","sdate":"por","edate":"por","elems":[{"name":"snow","interval":"yly","duration":"yly","reduce":"sum","smry":{"reduce":"max","add":"date"}}]};
    data_most_calendaryear_snow_day = GridData(most_calendaryear_snow_day) # Returned data from request
    date_most_snow_day = str(data_most_calendaryear_snow_day['smry'][0][1]) # Display year of earliest snow. Using dict key of smry. Keys are found data_earliest_snow_cvg.viewkeys() and meta, data, smry
    value_most_snow_day = str(data_most_calendaryear_snow_day['smry'][0][0]) # Take the year of the earliest snow then subtract from sdate and add 1 year back
    # - #
    # Most in a calendar year- CMH
    most_calendaryear_snow_cmh = {"sid":"cmhthr","sdate":"por","edate":"por","elems":[{"name":"snow","interval":"yly","duration":"yly","reduce":"sum","smry":{"reduce":"max","add":"date"}}]};
    data_most_calendaryear_snow_cmh = GridData(most_calendaryear_snow_cmh) # Returned data from request
    date_most_snow_cmh = str(data_most_calendaryear_snow_cmh['smry'][0][1]) # Display year of earliest snow. Using dict key of smry. Keys are found data_earliest_snow_cvg.viewkeys() and meta, data, smry
    value_most_snow_cmh = str(data_most_calendaryear_snow_cmh['smry'][0][0]) # Take the year of the earliest snow then subtract from sdate and add 1 year back
    # - #

    # Least in a calendar year- CVG
    least_calendaryear_snow_cvg = {"sid":"cvgthr","sdate":"por","edate":str(int(cy)-1),"elems":[{"name":"snow","interval":"yly","duration":"yly","reduce":"sum","smry":{"reduce":"min","add":"date"},"maxmissing":1}]};
    data_least_calendaryear_snow_cvg = GridData(least_calendaryear_snow_cvg) # Returned data from request
    date_least_snow_cvg = str(data_least_calendaryear_snow_cvg['smry'][0][1]) # Display year of earliest snow. Using dict key of smry. Keys are found data_earliest_snow_cvg.viewkeys() and meta, data, smry
    value_least_snow_cvg = str(data_least_calendaryear_snow_cvg['smry'][0][0]) # Take the year of the earliest snow then subtract from sdate and add 1 year back
    # - #
    # Least in a calendar year- DAY
    least_calendaryear_snow_day = {"sid":"daythr","sdate":"por","edate":str(int(cy)-1),"elems":[{"name":"snow","interval":"yly","duration":"yly","reduce":"sum","smry":{"reduce":"min","add":"date"},"maxmissing":1}]};
    data_least_calendaryear_snow_day = GridData(least_calendaryear_snow_day) # Returned data from request
    date_least_snow_day = str(data_least_calendaryear_snow_day['smry'][0][1]) # Display year of earliest snow. Using dict key of smry. Keys are found data_earliest_snow_cvg.viewkeys() and meta, data, smry
    value_least_snow_day = str(data_least_calendaryear_snow_day['smry'][0][0]) # Take the year of the earliest snow then subtract from sdate and add 1 year back
    # - #
    # Least in a calendar year- CMH
    least_calendaryear_snow_cmh = {"sid":"cmhthr","sdate":"por","edate":str(int(cy)-1),"elems":[{"name":"snow","interval":"yly","duration":"yly","reduce":"sum","smry":{"reduce":"min","add":"date"},"maxmissing":1}]};
    data_least_calendaryear_snow_cmh = GridData(least_calendaryear_snow_cmh) # Returned data from request
    date_least_snow_cmh = str(data_least_calendaryear_snow_cmh['smry'][0][1]) # Display year of earliest snow. Using dict key of smry. Keys are found data_earliest_snow_cvg.viewkeys() and meta, data, smry
    value_least_snow_cmh = str(data_least_calendaryear_snow_cmh['smry'][0][0]) # Take the year of the earliest snow then subtract from sdate and add 1 year back
    # - #

    # Most in a season- CVG
    most_seasonyear_snow_cvg = {"sid":"cvgthr","sdate":"1891-07-31","edate":"por","elems":[{"name":"snow","interval":[1,0,0],"duration":"std","season_start":"8-1","reduce":{"reduce":"sum","add":"date"},"smry":{"reduce":"max","add":"date"}}]};
    data_most_seasonyear_snow_cvg = GridData(most_seasonyear_snow_cvg) # Returned data from request
    date_most_seasonyear_snow_cvg = str(data_most_seasonyear_snow_cvg['smry'][0][1]) # Display year of earliest snow. Using dict key of smry. Keys are found data_earliest_snow_cvg.viewkeys() and meta, data, smry
    value_most_seasonyear_snow_cvg = str(data_most_seasonyear_snow_cvg['smry'][0][0]) # Take the year of the earliest snow then subtract from sdate and add 1 year back
    # - #
    # Most in a season- DAY
    most_seasonyear_snow_day = {"sid":"daythr","sdate":"1893-07-31","edate":"por","elems":[{"name":"snow","interval":[1,0,0],"duration":"std","season_start":"8-1","reduce":{"reduce":"sum","add":"date"},"smry":{"reduce":"max","add":"date"}}]};
    data_most_seasonyear_snow_day = GridData(most_seasonyear_snow_day) # Returned data from request
    date_most_seasonyear_snow_day = str(data_most_seasonyear_snow_day['smry'][0][1]) # Display year of earliest snow. Using dict key of smry. Keys are found data_earliest_snow_cvg.viewkeys() and meta, data, smry
    value_most_seasonyear_snow_day = str(data_most_seasonyear_snow_day['smry'][0][0]) # Take the year of the earliest snow then subtract from sdate and add 1 year back
    # - #
    # Most in a season- CMH
    most_seasonyear_snow_cmh = {"sid":"cmhthr","sdate":"1884-07-31","edate":"por","elems":[{"name":"snow","interval":[1,0,0],"duration":"std","season_start":"8-1","reduce":{"reduce":"sum","add":"date"},"smry":{"reduce":"max","add":"date"}}]};
    data_most_seasonyear_snow_cmh = GridData(most_seasonyear_snow_cmh) # Returned data from request
    date_most_seasonyear_snow_cmh = str(data_most_seasonyear_snow_cmh['smry'][0][1]) # Display year of earliest snow. Using dict key of smry. Keys are found data_earliest_snow_cvg.viewkeys() and meta, data, smry
    value_most_seasonyear_snow_cmh = str(data_most_seasonyear_snow_cmh['smry'][0][0]) # Take the year of the earliest snow then subtract from sdate and add 1 year back
    # - #

    # Least in a season- CVG
    least_seasonyear_snow_cvg = {"sid":"cvgthr","sdate":"1891-07-31","edate":"por","elems":[{"name":"snow","interval":[1,0,0],"duration":"std","season_start":"8-1","reduce":{"reduce":"sum","add":"date"},"smry":{"reduce":"min","add":"date"},"maxmissing":1}]};
    data_least_seasonyear_snow_cvg = GridData(least_seasonyear_snow_cvg) # Returned data from request
    date_least_seasonyear_snow_cvg = str(data_least_seasonyear_snow_cvg['smry'][0][1]) # Display year of earliest snow. Using dict key of smry. Keys are found data_earliest_snow_cvg.viewkeys() and meta, data, smry
    value_least_seasonyear_snow_cvg = str(data_least_seasonyear_snow_cvg['smry'][0][0]) # Take the year of the earliest snow then subtract from sdate and add 1 year back
    # - #
    # Least in a season- DAY
    least_seasonyear_snow_day = {"sid":"daythr","sdate":"1893-07-31","edate":"por","elems":[{"name":"snow","interval":[1,0,0],"duration":"std","season_start":"8-1","reduce":{"reduce":"sum","add":"date"},"smry":{"reduce":"min","add":"date"},"maxmissing":1}]};
    data_least_seasonyear_snow_day = GridData(least_seasonyear_snow_day) # Returned data from request
    date_least_seasonyear_snow_day = str(data_least_seasonyear_snow_day['smry'][0][1]) # Display year of earliest snow. Using dict key of smry. Keys are found data_earliest_snow_cvg.viewkeys() and meta, data, smry
    value_least_seasonyear_snow_day = str(data_least_seasonyear_snow_day['smry'][0][0]) # Take the year of the earliest snow then subtract from sdate and add 1 year back
    # - #
    # Least in a season- CMH
    least_seasonyear_snow_cmh = {"sid":"cmhthr","sdate":"1884-07-31","edate":"por","elems":[{"name":"snow","interval":[1,0,0],"duration":"std","season_start":"8-1","reduce":{"reduce":"sum","add":"date"},"smry":{"reduce":"min","add":"date"},"maxmissing":1}]};
    data_least_seasonyear_snow_cmh = GridData(least_seasonyear_snow_cmh) # Returned data from request
    date_least_seasonyear_snow_cmh = str(data_least_seasonyear_snow_cmh['smry'][0][1]) # Display year of earliest snow. Using dict key of smry. Keys are found data_earliest_snow_cvg.viewkeys() and meta, data, smry
    value_least_seasonyear_snow_cmh = str(data_least_seasonyear_snow_cmh['smry'][0][0]) # Take the year of the earliest snow then subtract from sdate and add 1 year back
    # - #

    # Most days with daily snowfall >1" in a season- CVG
    most_daysone_snow_cvg = {"sid":"cvgthr","sdate":"1891-07-31","edate":"por","elems":[{"name":"snow","interval":[1,0,0],"duration":"std","season_start":"8-1","reduce":"cnt_ge_1.0","smry":{"reduce":"max","add":"date"}}]};
    data_most_daysone_snow_cvg = GridData(most_daysone_snow_cvg)
    date_most_daysone_snow_cvg = str(data_most_daysone_snow_cvg['smry'][0][1])
    value_most_daysone_snow_cvg = str(data_most_daysone_snow_cvg['smry'][0][0])
    # - #
    # Most days with daily snowfall >1" in a season- DAY
    most_daysone_snow_day = {"sid":"daythr","sdate":"1893-07-31","edate":"por","elems":[{"name":"snow","interval":[1,0,0],"duration":"std","season_start":"8-1","reduce":"cnt_ge_1.0","smry":{"reduce":"max","add":"date"}}]};
    data_most_daysone_snow_day = GridData(most_daysone_snow_day)
    date_most_daysone_snow_day = str(data_most_daysone_snow_day['smry'][0][1])
    value_most_daysone_snow_day = str(data_most_daysone_snow_day['smry'][0][0])
    # - #
    # Most days with daily snowfall >1" in a season- CMH
    most_daysone_snow_cmh = {"sid":"cmhthr","sdate":"1884-07-31","edate":"por","elems":[{"name":"snow","interval":[1,0,0],"duration":"std","season_start":"8-1","reduce":"cnt_ge_1.0","smry":{"reduce":"max","add":"date"}}]};
    data_most_daysone_snow_cmh = GridData(most_daysone_snow_cmh)
    date_most_daysone_snow_cmh = str(data_most_daysone_snow_cmh['smry'][0][1])
    value_most_daysone_snow_cmh = str(data_most_daysone_snow_cmh['smry'][0][0])
    # - #

    # Most days with measurable snowfall in a season- CVG
    most_daystrace_snow_cvg = {"sid":"cvgthr","sdate":"1891-07-31","edate":"por","elems":[{"name":"snow","interval":[1,0,0],"duration":"std","season_start":"8-1","reduce":"cnt_gt_0","smry":{"reduce":"max","add":"date"}}]};
    data_most_daystrace_snow_cvg = GridData(most_daystrace_snow_cvg)
    date_most_daystrace_snow_cvg = str(data_most_daystrace_snow_cvg['smry'][0][1])
    value_most_daystrace_snow_cvg = str(data_most_daystrace_snow_cvg['smry'][0][0])
    # - #
    # Most days with daily snowfall >1" in a season- DAY
    most_daystrace_snow_day = {"sid":"daythr","sdate":"1893-07-31","edate":"por","elems":[{"name":"snow","interval":[1,0,0],"duration":"std","season_start":"8-1","reduce":"cnt_gt_0","smry":{"reduce":"max","add":"date"}}]};
    data_most_daystrace_snow_day = GridData(most_daystrace_snow_day)
    date_most_daystrace_snow_day = str(data_most_daystrace_snow_day['smry'][0][1])
    value_most_daystrace_snow_day = str(data_most_daystrace_snow_day['smry'][0][0])
    # - #
    # Most days with daily snowfall >1" in a season- CMH
    most_daystrace_snow_cmh = {"sid":"cmhthr","sdate":"1884-07-31","edate":"por","elems":[{"name":"snow","interval":[1,0,0],"duration":"std","season_start":"8-1","reduce":"cnt_gt_0","smry":{"reduce":"max","add":"date"}}]};
    data_most_daystrace_snow_cmh = GridData(most_daystrace_snow_cmh)
    date_most_daystrace_snow_cmh = str(data_most_daystrace_snow_cmh['smry'][0][1])
    value_most_daystrace_snow_cmh = str(data_most_daystrace_snow_cmh['smry'][0][0])
    # - #

    # Most snowfall in 1 day- CVG
    most_daily_snow_cvg = {"sid":"cvgthr","sdate":"por","edate":"por","elems":[{"name":"snow","interval":"dly","duration":"dly","smry":{"reduce":"max","add":"date"},"smry_only":1}]}
    data_most_daily_snow_cvg = GridData(most_daily_snow_cvg)
    date_most_daily_snow_cvg = str(data_most_daily_snow_cvg['smry'][0][1])
    value_most_daily_snow_cvg = str(data_most_daily_snow_cvg['smry'][0][0])
    # - #
    # Most snowfall in 1 day- DAY
    most_daily_snow_day = {"sid":"daythr","sdate":"por","edate":"por","elems":[{"name":"snow","interval":"dly","duration":"dly","smry":{"reduce":"max","add":"date"},"smry_only":1}]}
    data_most_daily_snow_day = GridData(most_daily_snow_day)
    date_most_daily_snow_day = str(data_most_daily_snow_day['smry'][0][1])
    value_most_daily_snow_day = str(data_most_daily_snow_day['smry'][0][0])
    # - #
    # Most snowfall in 1 day- CMH
    most_daily_snow_cmh = {"sid":"cmhthr","sdate":"por","edate":"por","elems":[{"name":"snow","interval":"dly","duration":"dly","smry":{"reduce":"max","add":"date"},"smry_only":1}]}
    data_most_daily_snow_cmh = GridData(most_daily_snow_cmh)
    date_most_daily_snow_cmh = str(data_most_daily_snow_cmh['smry'][0][1])
    value_most_daily_snow_cmh = str(data_most_daily_snow_cmh['smry'][0][0])
    # - #

    # Most snowfall in 2 days- CVG
    most_twodaily_snow_cvg = {"sid":"cvgthr","sdate":"por","edate":"por","elems":[{"name":"snow","interval":"dly","duration":2,"reduce":"sum","smry":{"reduce":"max","add":"date"},"smry_only":1}]}
    data_most_twodaily_snow_cvg = GridData(most_twodaily_snow_cvg)
    date_most_twodaily_snow_cvg = str(data_most_twodaily_snow_cvg['smry'][0][1])
    value_most_twodaily_snow_cvg = str(data_most_twodaily_snow_cvg['smry'][0][0])
    # Most snowfall in 2 days- DAY
    most_twodaily_snow_day = {"sid":"daythr","sdate":"por","edate":"por","elems":[{"name":"snow","interval":"dly","duration":2,"reduce":"sum","smry":{"reduce":"max","add":"date"},"smry_only":1}]}
    data_most_twodaily_snow_day = GridData(most_twodaily_snow_day)
    date_most_twodaily_snow_day = str(data_most_twodaily_snow_day['smry'][0][1])
    value_most_twodaily_snow_day = str(data_most_twodaily_snow_day['smry'][0][0])
    # Most snowfall in 2 days- CMH
    most_twodaily_snow_cmh = {"sid":"cmhthr","sdate":"por","edate":"por","elems":[{"name":"snow","interval":"dly","duration":2,"reduce":"sum","smry":{"reduce":"max","add":"date"},"smry_only":1}]}
    data_most_twodaily_snow_cmh = GridData(most_twodaily_snow_cmh)
    date_most_twodaily_snow_cmh = str(data_most_twodaily_snow_cmh['smry'][0][1])
    value_most_twodaily_snow_cmh = str(data_most_twodaily_snow_cmh['smry'][0][0])

    # Longest stretch of measurable snowfall- CVG
    longest_measure_snow_cvg = {"sid":"cvgthr","sdate":"1891-6-30","edate":"2017-6-30","elems":[{"name":"snow","interval":[1,0,0],"duration":"std","season_start":"7-1","reduce":{"reduce":"run_ge_0.1","add":"date"}}]}
    data_longest_measure_snow_cvg = GridData(longest_measure_snow_cvg)
    splitline = str(data_longest_measure_snow_cvg).split(",")
    counter = 0
    totalcount = 0
    index = 0
    dtype = [('date','S10'),('count',int)]
    values = []
    final_data_longest_measure_snow_cvg = []
    for line in splitline:
        #print line
        new = line.strip(" ' /n /t [ ] /u }")
        #print new
        if totalcount >5:
            if counter == 1:
                year = str(new)
                values.append([])
                values[index]=(year,count)
                index = index + 1
                counter = 0
            if counter == 0:
                try: 
                    count = int(new)
                    #values.append([])
                    #values[index]=(year,count)
                    counter = 1
                    #index = index + 1
                except ValueError:
                    counter = 0
        totalcount = totalcount + 1
    measure_snow_cvg = np.sort(np.array(values,dtype),order='count')[::-1]
    final_data_longest_measure_snow_cvg.append((measure_snow_cvg[0][0],measure_snow_cvg[0][1]))
    for j in range(len(measure_snow_cvg)):
        if measure_snow_cvg[j][1] == measure_snow_cvg[j+1][1]:
            final_data_longest_measure_snow_cvg.append((measure_snow_cvg[j+1][0],measure_snow_cvg[j+1][1]))
        else:
            break
    # Longest stretch of measurable snowfall- DAY
    longest_measure_snow_day = {"sid":"daythr","sdate":"1893-6-30","edate":"2017-6-30","elems":[{"name":"snow","interval":[1,0,0],"duration":"std","season_start":"7-1","reduce":{"reduce":"run_ge_0.1","add":"date"}}]}
    data_longest_measure_snow_day = GridData(longest_measure_snow_day)
    splitline = str(data_longest_measure_snow_day).split(",")
    counter = 0
    totalcount = 0
    index = 0
    dtype = [('date','S10'),('count',int)]
    values = []
    final_data_longest_measure_snow_day = []
    for line in splitline:
        #print line
        new = line.strip(" ' /n /t [ ] /u }")
        #print new
        if totalcount >5:
            if counter == 1:
                year = str(new)
                values.append([])
                values[index]=(year,count)
                index = index + 1
                counter = 0
            if counter == 0:
                try: 
                    count = int(new)
                    counter = 1
                except ValueError:
                    counter = 0
        totalcount = totalcount + 1
    measure_snow_day = np.sort(np.array(values,dtype),order='count')[::-1]
    final_data_longest_measure_snow_day.append((measure_snow_day[0][0],measure_snow_day[0][1]))
    for j in range(len(measure_snow_day)):
        if measure_snow_day[j][1] == measure_snow_day[j+1][1]:
            final_data_longest_measure_snow_day.append((measure_snow_day[j+1][0],measure_snow_day[j+1][1]))
        else:
            break
    # Longest stretch of measurable snowfall- CMH
    longest_measure_snow_cmh = {"sid":"cmhthr","sdate":"1884-6-30","edate":"2017-6-30","elems":[{"name":"snow","interval":[1,0,0],"duration":"std","season_start":"7-1","reduce":{"reduce":"run_ge_0.1","add":"date"}}]}
    data_longest_measure_snow_cmh = GridData(longest_measure_snow_cmh)
    splitline = str(data_longest_measure_snow_cmh).split(",")
    counter = 0
    totalcount = 0
    index = 0
    dtype = [('date','S10'),('count',int)]
    values = []
    final_data_longest_measure_snow_cmh = []
    for line in splitline:
        #print line
        new = line.strip(" ' /n /t [ ] /u }")
        #print new
        if totalcount >5:
            if counter == 1:
                year = str(new)
                values.append([])
                values[index]=(year,count)
                index = index + 1
                counter = 0
            if counter == 0:
                try: 
                    count = int(new)
                    counter = 1
                except ValueError:
                    counter = 0
        totalcount = totalcount + 1
    measure_snow_cmh = np.sort(np.array(values,dtype),order='count')[::-1]
    final_data_longest_measure_snow_cmh.append((measure_snow_cmh[0][0],measure_snow_cmh[0][1]))
    for j in range(len(measure_snow_cmh)):
        if measure_snow_cmh[j][1] == measure_snow_cmh[j+1][1]:
            final_data_longest_measure_snow_cmh.append((measure_snow_cmh[j+1][0],measure_snow_cmh[j+1][1]))
        else:
            break
    ### --- ###

    ### Step 2: Snowfall climate information list setup- includes needed html for formatting ###
    # List setup - Month #
    snowmonth_cvg = [] # Initialize CVG list
    snowmonth_day = [] # Initialize DAY list
    snowmonth_cmh = [] # Initialize CMH list
    # - #

    # List setup - Year #
    snowyear_cvg = [] # Initialize CVG list
    snowyear_day = [] # Initialize DAY list
    snowyear_cmh = [] # Initialize CMH list
    # - #

    # Header/ MISC Info #
    # CVG
    snowmonth_cvg.append('<table align="center" border="0" cellpadding="1" cellspacing="1" style="width: 750px;">'+ '\n' +
                        '<tbody>'+ '\n' +
                        '<tr>'+ '\n' +
			'<td style="vertical-align: middle" align="center" colspan="3"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">'+ '\n' +
                        'Last Update: ' + current_date+ '\n' +
                        '<br />'+ '\n' +
                        '<br />'+ '\n' +
			'</p></td>'+ '\n' +
                        '</tr>'+ '\n' +
                        '</tbody>'+ '\n' +
                        '</table>'+ '\n' +
                        '<table align="center" border="1" cellpadding="1" cellspacing="1" style="width: 750px;">'+ '\n' +
                        '<tbody>'+ '\n'   
                        '<tr>'+ '\n'
			'<td bgcolor="#424949" style="vertical-align: middle" align="center" colspan="1" rowspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Qualifier<br />'+ '\n'
			'</p></font></td>'+ '\n'
			'<td bgcolor="#424949" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Value/Date<br />'+ '\n'
			'</p></font></td>'+ '\n'
			'<td bgcolor="#424949" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Year<br />'+ '\n'
			'</p></td>'+ '\n'
                        '</tr>'+ '\n')
    snowyear_cvg.append('<table align="center" border="0" cellpadding="1" cellspacing="1" style="width: 750px;">'+ '\n' +
                        '<tbody>'+ '\n' +
                        '<tr>'+ '\n' +
			'<td style="vertical-align: middle" align="center" colspan="3"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">'+ '\n' +
                        'Last Update: ' + current_date+ '\n' +
                        '<br />'+ '\n' +
                        '<br />'+ '\n' +
			'</p></td>'+ '\n' +
                        '</tr>'+ '\n' +
                        '</tbody>'+ '\n' +
                        '</table>'+ '\n' +
                        '<table align="center" border="1" cellpadding="1" cellspacing="1" style="width: 750px;">'+ '\n' +
                        '<tbody>'+ '\n'   
                        '<tr>'+ '\n'
			'<td bgcolor="#424949" style="vertical-align: middle" align="center" colspan="1" rowspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Qualifier<br />'+ '\n'
			'</p></font></td>'+ '\n'
			'<td bgcolor="#424949" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Value<br />'+ '\n'
			'</p></font></td>'+ '\n'
			'<td bgcolor="#424949" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Date/Year<br />'+ '\n'
			'</p></td>'+ '\n'
                        '</tr>'+ '\n')
    # DAY
    snowmonth_day.append('<table align="center" border="0" cellpadding="1" cellspacing="1" style="width: 750px;">'+ '\n' +
                        '<tbody>'+ '\n' +
                        '<tr>'+ '\n' +
			'<td style="vertical-align: middle" align="center" colspan="3"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">'+ '\n' +
                        'Last Update: ' + current_date+ '\n' +
                        '<br />'+ '\n' +
                        '<br />'+ '\n' +
			'</p></td>'+ '\n' +
                        '</tr>'+ '\n' +
                        '</tbody>'+ '\n' +
                        '</table>'+ '\n' +
                        '<table align="center" border="1" cellpadding="1" cellspacing="1" style="width: 750px;">'+ '\n' +
                        '<tbody>'+ '\n'   
                        '<tr>'+ '\n'
			'<td bgcolor="#424949" style="vertical-align: middle" align="center" colspan="1" rowspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Qualifier<br />'+ '\n'
			'</p></font></td>'+ '\n'
			'<td bgcolor="#424949" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Value/Date<br />'+ '\n'
			'</p></font></td>'+ '\n'
			'<td bgcolor="#424949" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Year<br />'+ '\n'
			'</p></td>'+ '\n'
                        '</tr>'+ '\n')
    snowyear_day.append('<table align="center" border="0" cellpadding="1" cellspacing="1" style="width: 750px;">'+ '\n' +
                        '<tbody>'+ '\n' +
                        '<tr>'+ '\n' +
			'<td style="vertical-align: middle" align="center" colspan="3"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">'+ '\n' +
                        'Last Update: ' + current_date+ '\n' +
                        '<br />'+ '\n' +
                        '<br />'+ '\n' +
			'</p></td>'+ '\n' +
                        '</tr>'+ '\n' +
                        '</tbody>'+ '\n' +
                        '</table>'+ '\n' +
                        '<table align="center" border="1" cellpadding="1" cellspacing="1" style="width: 750px;">'+ '\n' +
                        '<tbody>'+ '\n'   
                        '<tr>'+ '\n'
			'<td bgcolor="#424949" style="vertical-align: middle" align="center" colspan="1" rowspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Qualifier<br />'+ '\n'
			'</p></font></td>'+ '\n'
			'<td bgcolor="#424949" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Value<br />'+ '\n'
			'</p></font></td>'+ '\n'
			'<td bgcolor="#424949" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Date/Year<br />'+ '\n'
			'</p></td>'+ '\n'
                        '</tr>'+ '\n')
    # CMH
    snowmonth_cmh.append('<table align="center" border="0" cellpadding="1" cellspacing="1" style="width: 750px;">'+ '\n' +
                        '<tbody>'+ '\n' +
                        '<tr>'+ '\n' +
			'<td style="vertical-align: middle" align="center" colspan="3"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">'+ '\n' +
                        'Last Update: ' + current_date+ '\n' +
                        '<br />'+ '\n' +
                        '<br />'+ '\n' +
			'</p></td>'+ '\n' +
                        '</tr>'+ '\n' +
                        '</tbody>'+ '\n' +
                        '</table>'+ '\n' +
                        '<table align="center" border="1" cellpadding="1" cellspacing="1" style="width: 750px;">'+ '\n' +
                        '<tbody>'+ '\n'   
                        '<tr>'+ '\n'
			'<td bgcolor="#424949" style="vertical-align: middle" align="center" colspan="1" rowspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Qualifier<br />'+ '\n'
			'</p></font></td>'+ '\n'
			'<td bgcolor="#424949" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Value/Date<br />'+ '\n'
			'</p></font></td>'+ '\n'
			'<td bgcolor="#424949" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Year<br />'+ '\n'
			'</p></td>'+ '\n'
                        '</tr>'+ '\n')
    snowyear_cmh.append('<table align="center" border="0" cellpadding="1" cellspacing="1" style="width: 750px;">'+ '\n' +
                        '<tbody>'+ '\n' +
                        '<tr>'+ '\n' +
			'<td style="vertical-align: middle" align="center" colspan="3"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">'+ '\n' +
                        'Last Update: ' + current_date+ '\n' +
                        '<br />'+ '\n' +
                        '<br />'+ '\n' +
			'</p></td>'+ '\n' +
                        '</tr>'+ '\n' +
                        '</tbody>'+ '\n' +
                        '</table>'+ '\n' +
                        '<table align="center" border="1" cellpadding="1" cellspacing="1" style="width: 750px;">'+ '\n' +
                        '<tbody>'+ '\n'   
                        '<tr>'+ '\n'
			'<td bgcolor="#424949" style="vertical-align: middle" align="center" colspan="1" rowspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Qualifier<br />'+ '\n'
			'</p></font></td>'+ '\n'
			'<td bgcolor="#424949" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Value<br />'+ '\n'
			'</p></font></td>'+ '\n'
			'<td bgcolor="#424949" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Date/Year<br />'+ '\n'
			'</p></td>'+ '\n'
                        '</tr>'+ '\n')
    # - #    

    # Snow Month #
    # Most in Oct
    # CVG
    cvg_month_totals_oct = str(cvg_month_totals[0])
    cvg_month_totals_octyr_final = cvg_month_totals_oct[4:11].strip(" ( u ' ")
    cvg_month_totals_octnum_final = cvg_month_totals_oct[12:21].strip(" , ( u ' ) ")
    snowmonth_cvg.append('<tr>'+ '\n' +
                        '<td bgcolor="#1F618D" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Most in October<br />'+ '\n' +
                	'</p></td>'+ '\n' +
                    	'<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowmonth_cvg.append(cvg_month_totals_octyr_final)
    snowmonth_cvg.append('<br />'+'</p></td>'+ '<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="2"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowmonth_cvg.append(cvg_month_totals_octnum_final + '"')
    snowmonth_cvg.append('<br />'+ '\n' +
                        '</p></td>'+ '\n' +
                        '</tr>'+ '\n')
    # DAY
    day_month_totals_oct = str(day_month_totals[0])
    day_month_totals_octyr_final = day_month_totals_oct[4:11].strip(" ( u ' ")
    day_month_totals_octnum_final = day_month_totals_oct[12:21].strip(" , ( u ' ) ")
    snowmonth_day.append('<tr>'+ '\n' +
                        '<td bgcolor="#1F618D" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Most in October<br />'+ '\n' +
                	'</p></td>'+ '\n' +
                    	'<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowmonth_day.append(day_month_totals_octyr_final)
    snowmonth_day.append('<br />'+'</p></td>'+ '<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="2"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowmonth_day.append(day_month_totals_octnum_final + '"')
    snowmonth_day.append('<br />'+ '\n' +
                        '</p></td>'+ '\n' +
                        '</tr>'+ '\n') 
    # CMH
    cmh_month_totals_oct = str(cmh_month_totals[0])
    cmh_month_totals_octyr_final = cmh_month_totals_oct[4:11].strip(" ( u ' ")
    cmh_month_totals_octnum_final = cmh_month_totals_oct[12:21].strip(" , ( u ' ) ")
    snowmonth_cmh.append('<tr>'+ '\n' +
                        '<td bgcolor="#1F618D" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Most in October<br />'+ '\n' +
                	'</p></td>'+ '\n' +
                    	'<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowmonth_cmh.append(cmh_month_totals_octyr_final)
    snowmonth_cmh.append('<br />'+'</p></td>'+ '<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="2"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowmonth_cmh.append(cmh_month_totals_octnum_final + '"')
    snowmonth_cmh.append('<br />'+ '\n' +
                        '</p></td>'+ '\n' +
                        '</tr>'+ '\n')
    # - #

    # Least in Oct
    # CVG
    cvg_least_month_totals_oct = str(cvg_least_month_totals[0])
    cvg_least_month_totals_octyr_final = cvg_least_month_totals_oct[4:11].strip(" ( u ' ")
    cvg_least_month_totals_octnum_final = cvg_least_month_totals_oct[12:21].strip(" , ( u ' ) ")
    snowmonth_cvg.append('<tr>'+ '\n' +
                        '<td bgcolor="#1F618D" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Least in October<br />'+ '\n' +                	'</p></td>'+ '\n' +
                    	'<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowmonth_cvg.append(cvg_least_month_totals_octyr_final)
    snowmonth_cvg.append('<br />'+'</p></td>'+ '<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="2"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowmonth_cvg.append(cvg_least_month_totals_octnum_final)
    if (cvg_least_month_totals_octnum_final != 'T'):
        snowmonth_cvg.append('"')
    if star_needed_least_cvg[0] == 1:
        snowmonth_cvg.append(' *')
    snowmonth_cvg.append('<br />'+ '\n' +
                        '</p></td>'+ '\n' +
                        '</tr>'+ '\n')
    # DAY
    day_least_month_totals_oct = str(day_least_month_totals[0])
    day_least_month_totals_octyr_final = day_least_month_totals_oct[4:11].strip(" ( u ' ")
    day_least_month_totals_octnum_final = day_least_month_totals_oct[12:21].strip(" , ( u ' ) ")
    snowmonth_day.append('<tr>'+ '\n' +
                        '<td bgcolor="#1F618D" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Least in October<br />'+ '\n' +                	'</p></td>'+ '\n' +
                    	'<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowmonth_day.append(day_least_month_totals_octyr_final)
    snowmonth_day.append('<br />'+'</p></td>'+ '<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="2"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowmonth_day.append(day_least_month_totals_octnum_final)
    if (day_least_month_totals_octnum_final != 'T'):
        snowmonth_day.append('"')
    if star_needed_least_day[0] == 1:
        snowmonth_day.append(' *')
    snowmonth_day.append('<br />'+ '\n' +
                        '</p></td>'+ '\n' +
                        '</tr>'+ '\n')

    # CMH
    cmh_least_month_totals_oct = str(cmh_least_month_totals[0])
    cmh_least_month_totals_octyr_final = cmh_least_month_totals_oct[4:11].strip(" ( u ' ")
    cmh_least_month_totals_octnum_final = cmh_least_month_totals_oct[12:21].strip(" , ( u ' ) ")
    snowmonth_cmh.append('<tr>'+ '\n' +
                        '<td bgcolor="#1F618D" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Least in October<br />'+ '\n' +                	'</p></td>'+ '\n' +
                    	'<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowmonth_cmh.append(cmh_least_month_totals_octyr_final)
    snowmonth_cmh.append('<br />'+'</p></td>'+ '<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="2"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowmonth_cmh.append(cmh_least_month_totals_octnum_final)
    if (cmh_least_month_totals_octnum_final != 'T'):
        snowmonth_cmh.append('"')
    if star_needed_least_cmh[0] == 1:
        snowmonth_cmh.append(' *')
    snowmonth_cmh.append('<br />'+ '\n' +
                        '</p></td>'+ '\n' +
                        '</tr>'+ '\n')
    
    # - #

    # Most in Nov
    # CVG
    cvg_month_totals_nov = str(cvg_month_totals[1])
    cvg_month_totals_novyr_final = cvg_month_totals_nov[4:11].strip(" ( u ' ")
    cvg_month_totals_novnum_final = cvg_month_totals_nov[12:21].strip(" , ( u ' ) ")
    snowmonth_cvg.append('<tr>'+ '\n' +
                        '<td bgcolor="#1F618D" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Most in November<br />'+ '\n' +
                	'</p></td>'+ '\n' +
                    	'<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowmonth_cvg.append(cvg_month_totals_novyr_final)
    snowmonth_cvg.append('<br />'+'</p></td>'+ '<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="2"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowmonth_cvg.append(cvg_month_totals_novnum_final + '"')
    snowmonth_cvg.append('<br />'+ '\n' +
                        '</p></td>'+ '\n' +
                        '</tr>'+ '\n')
    # DAY
    day_month_totals_nov = str(day_month_totals[1])
    day_month_totals_novyr_final = day_month_totals_nov[4:11].strip(" ( u ' ")
    day_month_totals_novnum_final = day_month_totals_nov[12:21].strip(" , ( u ' ) ")
    snowmonth_day.append('<tr>'+ '\n' +
                        '<td bgcolor="#1F618D" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Most in November<br />'+ '\n' +
                	'</p></td>'+ '\n' +
                    	'<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowmonth_day.append(day_month_totals_novyr_final)
    snowmonth_day.append('<br />'+'</p></td>'+ '<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="2"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowmonth_day.append(day_month_totals_novnum_final + '"')
    snowmonth_day.append('<br />'+ '\n' +
                        '</p></td>'+ '\n' +
                        '</tr>'+ '\n') 
    # CMH
    cmh_month_totals_nov = str(cmh_month_totals[1])
    cmh_month_totals_novyr_final = cmh_month_totals_nov[4:11].strip(" ( u ' ")
    cmh_month_totals_novnum_final = cmh_month_totals_nov[12:21].strip(" , ( u ' ) ")
    snowmonth_cmh.append('<tr>'+ '\n' +
                        '<td bgcolor="#1F618D" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Most in November<br />'+ '\n' +
                	'</p></td>'+ '\n' +
                    	'<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowmonth_cmh.append(cmh_month_totals_novyr_final)
    snowmonth_cmh.append('<br />'+'</p></td>'+ '<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="2"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowmonth_cmh.append(cmh_month_totals_novnum_final + '"')
    snowmonth_cmh.append('<br />'+ '\n' +
                        '</p></td>'+ '\n' +
                        '</tr>'+ '\n')
    # - #

    # Least in Nov
    # CVG
    cvg_least_month_totals_nov = str(cvg_least_month_totals[1])
    cvg_least_month_totals_novyr_final = cvg_least_month_totals_nov[4:11].strip(" ( u ' ")
    cvg_least_month_totals_novnum_final = cvg_least_month_totals_nov[12:21].strip(" , ( u ' ) ")
    snowmonth_cvg.append('<tr>'+ '\n' +
                        '<td bgcolor="#1F618D" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Least in November<br />'+ '\n' +                	'</p></td>'+ '\n' +
                    	'<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowmonth_cvg.append(cvg_least_month_totals_novyr_final)
    snowmonth_cvg.append('<br />'+'</p></td>'+ '<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="2"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowmonth_cvg.append(cvg_least_month_totals_novnum_final)
    if (cvg_least_month_totals_novnum_final != 'T'):
        snowmonth_cvg.append('"')
    if star_needed_least_cvg[1] == 1:
        snowmonth_cvg.append(' *')
    snowmonth_cvg.append('<br />'+ '\n' +
                        '</p></td>'+ '\n' +
                        '</tr>'+ '\n')
    # DAY
    day_least_month_totals_nov = str(day_least_month_totals[1])
    day_least_month_totals_novyr_final = day_least_month_totals_nov[4:11].strip(" ( u ' ")
    day_least_month_totals_novnum_final = day_least_month_totals_nov[12:21].strip(" , ( u ' ) ")
    snowmonth_day.append('<tr>'+ '\n' +
                        '<td bgcolor="#1F618D" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Least in November<br />'+ '\n' +                	'</p></td>'+ '\n' +
                    	'<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowmonth_day.append(day_least_month_totals_novyr_final)
    snowmonth_day.append('<br />'+'</p></td>'+ '<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="2"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowmonth_day.append(day_least_month_totals_novnum_final)
    if (day_least_month_totals_novnum_final != 'T'):
        snowmonth_day.append('"')
    if star_needed_least_day[1] == 1:
        snowmonth_day.append(' *')
    snowmonth_day.append('<br />'+ '\n' +
                        '</p></td>'+ '\n' +
                        '</tr>'+ '\n')

    # CMH
    cmh_least_month_totals_nov = str(cmh_least_month_totals[1])
    cmh_least_month_totals_novyr_final = cmh_least_month_totals_nov[4:11].strip(" ( u ' ")
    cmh_least_month_totals_novnum_final = cmh_least_month_totals_nov[12:21].strip(" , ( u ' ) ")
    snowmonth_cmh.append('<tr>'+ '\n' +
                        '<td bgcolor="#1F618D" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Least in November<br />'+ '\n' +                	'</p></td>'+ '\n' +
                    	'<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowmonth_cmh.append(cmh_least_month_totals_novyr_final)
    snowmonth_cmh.append('<br />'+'</p></td>'+ '<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="2"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowmonth_cmh.append(cmh_least_month_totals_novnum_final)
    if (cmh_least_month_totals_novnum_final != 'T'):
        snowmonth_cmh.append('"')
    if star_needed_least_cmh[1] == 1:
        snowmonth_cmh.append(' *')
    snowmonth_cmh.append('<br />'+ '\n' +
                        '</p></td>'+ '\n' +
                        '</tr>'+ '\n')
    # - #
    
    # Most in Dec
    # CVG
    cvg_month_totals_dec = str(cvg_month_totals[2])
    cvg_month_totals_decyr_final = cvg_month_totals_dec[4:11].strip(" ( u ' ")
    cvg_month_totals_decnum_final = cvg_month_totals_dec[12:21].strip(" , ( u ' ) ")
    snowmonth_cvg.append('<tr>'+ '\n' +
                        '<td bgcolor="#1F618D" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Most in December<br />'+ '\n' +
                	'</p></td>'+ '\n' +
                    	'<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowmonth_cvg.append(cvg_month_totals_decyr_final)
    snowmonth_cvg.append('<br />'+'</p></td>'+ '<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="2"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowmonth_cvg.append(cvg_month_totals_decnum_final + '"')
    snowmonth_cvg.append('<br />'+ '\n' +
                        '</p></td>'+ '\n' +
                        '</tr>'+ '\n')
    # DAY
    day_month_totals_dec = str(day_month_totals[2])
    day_month_totals_decyr_final = day_month_totals_dec[4:11].strip(" ( u ' ")
    day_month_totals_decnum_final = day_month_totals_dec[12:21].strip(" , ( u ' ) ")
    snowmonth_day.append('<tr>'+ '\n' +
                        '<td bgcolor="#1F618D" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Most in December<br />'+ '\n' +
                	'</p></td>'+ '\n' +
                    	'<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowmonth_day.append(day_month_totals_decyr_final)
    snowmonth_day.append('<br />'+'</p></td>'+ '<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="2"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowmonth_day.append(day_month_totals_decnum_final + '"')
    snowmonth_day.append('<br />'+ '\n' +
                        '</p></td>'+ '\n' +
                        '</tr>'+ '\n') 
    # CMH
    cmh_month_totals_dec = str(cmh_month_totals[2])
    cmh_month_totals_decyr_final = cmh_month_totals_dec[4:11].strip(" ( u ' ")
    cmh_month_totals_decnum_final = cmh_month_totals_dec[12:21].strip(" , ( u ' ) ")
    snowmonth_cmh.append('<tr>'+ '\n' +
                        '<td bgcolor="#1F618D" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Most in December<br />'+ '\n' +
                	'</p></td>'+ '\n' +
                    	'<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowmonth_cmh.append(cmh_month_totals_decyr_final)
    snowmonth_cmh.append('<br />'+'</p></td>'+ '<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="2"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowmonth_cmh.append(cmh_month_totals_decnum_final + '"')
    snowmonth_cmh.append('<br />'+ '\n' +
                        '</p></td>'+ '\n' +
                        '</tr>'+ '\n')
    # - #

    # Least in Dec
    # CVG
    cvg_least_month_totals_dec = str(cvg_least_month_totals[2])
    cvg_least_month_totals_decyr_final = cvg_least_month_totals_dec[4:11].strip(" ( u ' ")
    cvg_least_month_totals_decnum_final = cvg_least_month_totals_dec[12:21].strip(" , ( u ' ) ")
    snowmonth_cvg.append('<tr>'+ '\n' +
                        '<td bgcolor="#1F618D" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Least in December<br />'+ '\n' +                	'</p></td>'+ '\n' +
                    	'<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowmonth_cvg.append(cvg_least_month_totals_decyr_final)
    snowmonth_cvg.append('<br />'+'</p></td>'+ '<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="2"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowmonth_cvg.append(cvg_least_month_totals_decnum_final)
    if (cvg_least_month_totals_decnum_final != 'T'):
        snowmonth_cvg.append('"')
    if star_needed_least_cvg[2] == 1:
        snowmonth_cvg.append(' *')
    snowmonth_cvg.append('<br />'+ '\n' +
                        '</p></td>'+ '\n' +
                        '</tr>'+ '\n')
    # DAY
    day_least_month_totals_dec = str(day_least_month_totals[2])
    day_least_month_totals_decyr_final = day_least_month_totals_dec[4:11].strip(" ( u ' ")
    day_least_month_totals_decnum_final = day_least_month_totals_dec[12:21].strip(" , ( u ' ) ")
    snowmonth_day.append('<tr>'+ '\n' +
                        '<td bgcolor="#1F618D" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Least in December<br />'+ '\n' +                	'</p></td>'+ '\n' +
                    	'<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowmonth_day.append(day_least_month_totals_decyr_final)
    snowmonth_day.append('<br />'+'</p></td>'+ '<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="2"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowmonth_day.append(day_least_month_totals_decnum_final)
    if (day_least_month_totals_decnum_final != 'T'):
        snowmonth_day.append('"')
    if (star_needed_least_day[2] == 1):
        snowmonth_day.append(' *')
    snowmonth_day.append('<br />'+ '\n' +
                        '</p></td>'+ '\n' +
                        '</tr>'+ '\n')

    # CMH
    cmh_least_month_totals_dec = str(cmh_least_month_totals[2])
    cmh_least_month_totals_decyr_final = cmh_least_month_totals_dec[4:11].strip(" ( u ' ")
    cmh_least_month_totals_decnum_final = cmh_least_month_totals_dec[12:21].strip(" , ( u ' ) ")
    snowmonth_cmh.append('<tr>'+ '\n' +
                        '<td bgcolor="#1F618D" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Least in December<br />'+ '\n' +                	'</p></td>'+ '\n' +
                    	'<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowmonth_cmh.append(cmh_least_month_totals_decyr_final)
    snowmonth_cmh.append('<br />'+'</p></td>'+ '<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="2"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowmonth_cmh.append(cmh_least_month_totals_decnum_final)
    if (cmh_least_month_totals_decnum_final != 'T'):
        snowmonth_cmh.append('"')
    if star_needed_least_cmh[2] == 1:
        snowmonth_cmh.append(' *')
    snowmonth_cmh.append('<br />'+ '\n' +
                        '</p></td>'+ '\n' +
                        '</tr>'+ '\n')
    # - #

    # Most in Jan
    # CVG
    cvg_month_totals_jan = str(cvg_month_totals[3])
    cvg_month_totals_janyr_final = cvg_month_totals_jan[4:11].strip(" ( u ' ")
    cvg_month_totals_jannum_final = cvg_month_totals_jan[12:21].strip(" , ( u ' ) ")
    snowmonth_cvg.append('<tr>'+ '\n' +
                        '<td bgcolor="#1F618D" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Most in January<br />'+ '\n' +
                	'</p></td>'+ '\n' +
                    	'<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowmonth_cvg.append(cvg_month_totals_janyr_final)
    snowmonth_cvg.append('<br />'+'</p></td>'+ '<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="2"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowmonth_cvg.append(cvg_month_totals_jannum_final + '"')
    snowmonth_cvg.append('<br />'+ '\n' +
                        '</p></td>'+ '\n' +
                        '</tr>'+ '\n')
    # DAY
    day_month_totals_jan = str(day_month_totals[3])
    day_month_totals_janyr_final = day_month_totals_jan[4:11].strip(" ( u ' ")
    day_month_totals_jannum_final = day_month_totals_jan[12:21].strip(" , ( u ' ) ")
    snowmonth_day.append('<tr>'+ '\n' +
                        '<td bgcolor="#1F618D" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Most in January<br />'+ '\n' +
                	'</p></td>'+ '\n' +
                    	'<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowmonth_day.append(day_month_totals_janyr_final)
    snowmonth_day.append('<br />'+'</p></td>'+ '<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="2"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowmonth_day.append(day_month_totals_jannum_final + '"')
    snowmonth_day.append('<br />'+ '\n' +
                        '</p></td>'+ '\n' +
                        '</tr>'+ '\n') 
    # CMH
    cmh_month_totals_jan = str(cmh_month_totals[3])
    cmh_month_totals_janyr_final = cmh_month_totals_jan[4:11].strip(" ( u ' ")
    cmh_month_totals_jannum_final = cmh_month_totals_jan[12:21].strip(" , ( u ' ) ")
    snowmonth_cmh.append('<tr>'+ '\n' +
                        '<td bgcolor="#1F618D" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Most in January<br />'+ '\n' +
                	'</p></td>'+ '\n' +
                    	'<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowmonth_cmh.append(cmh_month_totals_janyr_final)
    snowmonth_cmh.append('<br />'+'</p></td>'+ '<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="2"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowmonth_cmh.append(cmh_month_totals_jannum_final + '"')
    snowmonth_cmh.append('<br />'+ '\n' +
                        '</p></td>'+ '\n' +
                        '</tr>'+ '\n')
    # - #

    # Least in Jan
    # CVG
    cvg_least_month_totals_jan = str(cvg_least_month_totals[3])
    cvg_least_month_totals_janyr_final = cvg_least_month_totals_jan[4:11].strip(" ( u ' ")
    cvg_least_month_totals_jannum_final = cvg_least_month_totals_jan[12:21].strip(" , ( u ' ) ")
    snowmonth_cvg.append('<tr>'+ '\n' +
                        '<td bgcolor="#1F618D" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Least in January<br />'+ '\n' +                	'</p></td>'+ '\n' +
                    	'<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowmonth_cvg.append(cvg_least_month_totals_janyr_final)
    snowmonth_cvg.append('<br />'+'</p></td>'+ '<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="2"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowmonth_cvg.append(cvg_least_month_totals_jannum_final)
    if (cvg_least_month_totals_jannum_final != 'T'):
        snowmonth_cvg.append('"')
    if star_needed_least_cvg[3] == 1:
        snowmonth_cvg.append(' *')
    snowmonth_cvg.append('<br />'+ '\n' +
                        '</p></td>'+ '\n' +
                        '</tr>'+ '\n')
    # DAY
    day_least_month_totals_jan = str(day_least_month_totals[3])
    day_least_month_totals_janyr_final = day_least_month_totals_jan[4:11].strip(" ( u ' ")
    day_least_month_totals_jannum_final = day_least_month_totals_jan[12:21].strip(" , ( u ' ) ")
    snowmonth_day.append('<tr>'+ '\n' +
                        '<td bgcolor="#1F618D" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Least in January<br />'+ '\n' +                	'</p></td>'+ '\n' +
                    	'<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowmonth_day.append(day_least_month_totals_janyr_final)
    snowmonth_day.append('<br />'+'</p></td>'+ '<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="2"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowmonth_day.append(day_least_month_totals_jannum_final)
    if (day_least_month_totals_jannum_final != 'T'):
        snowmonth_day.append('"')
    if (star_needed_least_day[3] == 1):
        snowmonth_day.append(' *')
    snowmonth_day.append('<br />'+ '\n' +
                        '</p></td>'+ '\n' +
                        '</tr>'+ '\n')

    # CMH
    cmh_least_month_totals_jan = str(cmh_least_month_totals[3])
    cmh_least_month_totals_janyr_final = cmh_least_month_totals_jan[4:11].strip(" ( u ' ")
    cmh_least_month_totals_jannum_final = cmh_least_month_totals_jan[12:21].strip(" , ( u ' ) ")
    snowmonth_cmh.append('<tr>'+ '\n' +
                        '<td bgcolor="#1F618D" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Least in January<br />'+ '\n' +                	'</p></td>'+ '\n' +
                    	'<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowmonth_cmh.append(cmh_least_month_totals_janyr_final)
    snowmonth_cmh.append('<br />'+'</p></td>'+ '<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="2"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowmonth_cmh.append(cmh_least_month_totals_jannum_final)
    if (cmh_least_month_totals_jannum_final != 'T'):
        snowmonth_cmh.append('"')
    if star_needed_least_cmh[3] == 1:
        snowmonth_cmh.append(' *')
    snowmonth_cmh.append('<br />'+ '\n' +
                        '</p></td>'+ '\n' +
                        '</tr>'+ '\n')
    # - #

    # Most in Feb
    # CVG
    cvg_month_totals_feb = str(cvg_month_totals[4])
    cvg_month_totals_febyr_final = cvg_month_totals_feb[4:11].strip(" ( u ' ")
    cvg_month_totals_febnum_final = cvg_month_totals_feb[12:21].strip(" , ( u ' ) ")
    snowmonth_cvg.append('<tr>'+ '\n' +
                        '<td bgcolor="#1F618D" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Most in February<br />'+ '\n' +
                	'</p></td>'+ '\n' +
                    	'<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowmonth_cvg.append(cvg_month_totals_febyr_final)
    snowmonth_cvg.append('<br />'+'</p></td>'+ '<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="2"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowmonth_cvg.append(cvg_month_totals_febnum_final + '"')
    snowmonth_cvg.append('<br />'+ '\n' +
                        '</p></td>'+ '\n' +
                        '</tr>'+ '\n')
    # DAY
    day_month_totals_feb = str(day_month_totals[4])
    day_month_totals_febyr_final = day_month_totals_feb[4:11].strip(" ( u ' ")
    day_month_totals_febnum_final = day_month_totals_feb[12:21].strip(" , ( u ' ) ")
    snowmonth_day.append('<tr>'+ '\n' +
                        '<td bgcolor="#1F618D" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Most in February<br />'+ '\n' +
                	'</p></td>'+ '\n' +
                    	'<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowmonth_day.append(day_month_totals_febyr_final)
    snowmonth_day.append('<br />'+'</p></td>'+ '<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="2"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowmonth_day.append(day_month_totals_febnum_final + '"')
    snowmonth_day.append('<br />'+ '\n' +
                        '</p></td>'+ '\n' +
                        '</tr>'+ '\n') 
    # CMH
    cmh_month_totals_feb = str(cmh_month_totals[4])
    cmh_month_totals_febyr_final = cmh_month_totals_feb[4:11].strip(" ( u ' ")
    cmh_month_totals_febnum_final = cmh_month_totals_feb[12:21].strip(" , ( u ' ) ")
    snowmonth_cmh.append('<tr>'+ '\n' +
                        '<td bgcolor="#1F618D" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Most in February<br />'+ '\n' +
                	'</p></td>'+ '\n' +
                    	'<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowmonth_cmh.append(cmh_month_totals_febyr_final)
    snowmonth_cmh.append('<br />'+'</p></td>'+ '<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="2"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowmonth_cmh.append(cmh_month_totals_febnum_final + '"')
    snowmonth_cmh.append('<br />'+ '\n' +
                        '</p></td>'+ '\n' +
                        '</tr>'+ '\n')
    # - #

    # Least in Feb
    # CVG
    cvg_least_month_totals_feb = str(cvg_least_month_totals[4])
    cvg_least_month_totals_febyr_final = cvg_least_month_totals_feb[4:11].strip(" ( u ' ")
    cvg_least_month_totals_febnum_final = cvg_least_month_totals_feb[12:21].strip(" , ( u ' ) ")
    snowmonth_cvg.append('<tr>'+ '\n' +
                        '<td bgcolor="#1F618D" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Least in February<br />'+ '\n' +                	'</p></td>'+ '\n' +
                    	'<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowmonth_cvg.append(cvg_least_month_totals_febyr_final)
    snowmonth_cvg.append('<br />'+'</p></td>'+ '<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="2"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowmonth_cvg.append(cvg_least_month_totals_febnum_final)
    if (cvg_least_month_totals_febnum_final != 'T'):
        snowmonth_cvg.append('"')
    if star_needed_least_cvg[4] == 1:
        snowmonth_cvg.append(' *')
    snowmonth_cvg.append('<br />'+ '\n' +
                        '</p></td>'+ '\n' +
                        '</tr>'+ '\n')
    # DAY
    day_least_month_totals_feb = str(day_least_month_totals[4])
    day_least_month_totals_febyr_final = day_least_month_totals_feb[4:11].strip(" ( u ' ")
    day_least_month_totals_febnum_final = day_least_month_totals_feb[12:21].strip(" , ( u ' ) ")
    snowmonth_day.append('<tr>'+ '\n' +
                        '<td bgcolor="#1F618D" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Least in February<br />'+ '\n' +                	'</p></td>'+ '\n' +
                    	'<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowmonth_day.append(day_least_month_totals_febyr_final)
    snowmonth_day.append('<br />'+'</p></td>'+ '<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="2"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowmonth_day.append(day_least_month_totals_febnum_final)
    if (day_least_month_totals_febnum_final != 'T'):
        snowmonth_day.append('"')
    if (star_needed_least_day[4] == 1):
        snowmonth_day.append(' *')
    snowmonth_day.append('<br />'+ '\n' +
                        '</p></td>'+ '\n' +
                        '</tr>'+ '\n')

    # CMH
    cmh_least_month_totals_feb = str(cmh_least_month_totals[4])
    cmh_least_month_totals_febyr_final = cmh_least_month_totals_feb[4:11].strip(" ( u ' ")
    cmh_least_month_totals_febnum_final = cmh_least_month_totals_feb[12:21].strip(" , ( u ' ) ")
    snowmonth_cmh.append('<tr>'+ '\n' +
                        '<td bgcolor="#1F618D" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Least in February<br />'+ '\n' +                	'</p></td>'+ '\n' +
                    	'<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowmonth_cmh.append(cmh_least_month_totals_febyr_final)
    snowmonth_cmh.append('<br />'+'</p></td>'+ '<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="2"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowmonth_cmh.append(cmh_least_month_totals_febnum_final)
    if (cmh_least_month_totals_febnum_final != 'T'):
        snowmonth_cmh.append('"')
    if star_needed_least_cmh[4] == 1:
        snowmonth_cmh.append(' *')
    snowmonth_cmh.append('<br />'+ '\n' +
                        '</p></td>'+ '\n' +
                        '</tr>'+ '\n')

    # Most in Mar
    # CVG
    cvg_month_totals_mar = str(cvg_month_totals[5])
    cvg_month_totals_maryr_final = cvg_month_totals_mar[4:11].strip(" ( u ' ")
    cvg_month_totals_marnum_final = cvg_month_totals_mar[12:21].strip(" , ( u ' ) ")
    snowmonth_cvg.append('<tr>'+ '\n' +
                        '<td bgcolor="#1F618D" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Most in March<br />'+ '\n' +
                	'</p></td>'+ '\n' +
                    	'<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowmonth_cvg.append(cvg_month_totals_maryr_final)
    snowmonth_cvg.append('<br />'+'</p></td>'+ '<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="2"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowmonth_cvg.append(cvg_month_totals_marnum_final + '"')
    snowmonth_cvg.append('<br />'+ '\n' +
                        '</p></td>'+ '\n' +
                        '</tr>'+ '\n')
    # DAY
    day_month_totals_mar = str(day_month_totals[5])
    day_month_totals_maryr_final = day_month_totals_mar[4:11].strip(" ( u ' ")
    day_month_totals_marnum_final = day_month_totals_mar[12:21].strip(" , ( u ' ) ")
    snowmonth_day.append('<tr>'+ '\n' +
                        '<td bgcolor="#1F618D" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Most in March<br />'+ '\n' +
                	'</p></td>'+ '\n' +
                    	'<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowmonth_day.append(day_month_totals_maryr_final)
    snowmonth_day.append('<br />'+'</p></td>'+ '<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="2"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowmonth_day.append(day_month_totals_marnum_final + '"')
    snowmonth_day.append('<br />'+ '\n' +
                        '</p></td>'+ '\n' +
                        '</tr>'+ '\n') 
    # CMH
    cmh_month_totals_mar = str(cmh_month_totals[5])
    cmh_month_totals_maryr_final = cmh_month_totals_mar[4:11].strip(" ( u ' ")
    cmh_month_totals_marnum_final = cmh_month_totals_mar[12:21].strip(" , ( u ' ) ")
    snowmonth_cmh.append('<tr>'+ '\n' +
                        '<td bgcolor="#1F618D" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Most in March<br />'+ '\n' +
                	'</p></td>'+ '\n' +
                    	'<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowmonth_cmh.append(cmh_month_totals_maryr_final)
    snowmonth_cmh.append('<br />'+'</p></td>'+ '<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="2"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowmonth_cmh.append(cmh_month_totals_marnum_final + '"')
    snowmonth_cmh.append('<br />'+ '\n' +
                        '</p></td>'+ '\n' +
                        '</tr>'+ '\n')
    # - #

    # Least in Mar
    # CVG
    cvg_least_month_totals_mar = str(cvg_least_month_totals[5])
    cvg_least_month_totals_maryr_final = cvg_least_month_totals_mar[4:11].strip(" ( u ' ")
    cvg_least_month_totals_marnum_final = cvg_least_month_totals_mar[12:21].strip(" , ( u ' ) ")
    snowmonth_cvg.append('<tr>'+ '\n' +
                        '<td bgcolor="#1F618D" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Least in March<br />'+ '\n' +                	'</p></td>'+ '\n' +
                    	'<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowmonth_cvg.append(cvg_least_month_totals_maryr_final)
    snowmonth_cvg.append('<br />'+'</p></td>'+ '<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="2"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowmonth_cvg.append(cvg_least_month_totals_marnum_final)
    if (cvg_least_month_totals_marnum_final != 'T'):
        snowmonth_cvg.append('"')
    if star_needed_least_cvg[5] == 1:
        snowmonth_cvg.append(' *')
    snowmonth_cvg.append('<br />'+ '\n' +
                        '</p></td>'+ '\n' +
                        '</tr>'+ '\n')
    # DAY
    day_least_month_totals_mar = str(day_least_month_totals[5])
    day_least_month_totals_maryr_final = day_least_month_totals_mar[4:11].strip(" ( u ' ")
    day_least_month_totals_marnum_final = day_least_month_totals_mar[12:21].strip(" , ( u ' ) ")
    snowmonth_day.append('<tr>'+ '\n' +
                        '<td bgcolor="#1F618D" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Least in March<br />'+ '\n' +                	'</p></td>'+ '\n' +
                    	'<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowmonth_day.append(day_least_month_totals_maryr_final)
    snowmonth_day.append('<br />'+'</p></td>'+ '<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="2"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowmonth_day.append(day_least_month_totals_marnum_final)
    if (day_least_month_totals_marnum_final != 'T'):
        snowmonth_day.append('"')
    if (star_needed_least_day[5] == 1):
        snowmonth_day.append(' *')
    snowmonth_day.append('<br />'+ '\n' +
                        '</p></td>'+ '\n' +
                        '</tr>'+ '\n')

    # CMH
    cmh_least_month_totals_mar = str(cmh_least_month_totals[5])
    cmh_least_month_totals_maryr_final = cmh_least_month_totals_mar[4:11].strip(" ( u ' ")
    cmh_least_month_totals_marnum_final = cmh_least_month_totals_mar[12:21].strip(" , ( u ' ) ")
    snowmonth_cmh.append('<tr>'+ '\n' +
                        '<td bgcolor="#1F618D" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Least in March<br />'+ '\n' +                	'</p></td>'+ '\n' +
                    	'<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowmonth_cmh.append(cmh_least_month_totals_maryr_final)
    snowmonth_cmh.append('<br />'+'</p></td>'+ '<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="2"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowmonth_cmh.append(cmh_least_month_totals_marnum_final)
    if (cmh_least_month_totals_marnum_final != 'T'):
        snowmonth_cmh.append('"')
    if star_needed_least_cmh[5] == 1:
        snowmonth_cmh.append(' *')
    snowmonth_cmh.append('<br />'+ '\n' +
                        '</p></td>'+ '\n' +
                        '</tr>'+ '\n')

    # Most in Apr
    # CVG
    cvg_month_totals_apr = str(cvg_month_totals[6])
    cvg_month_totals_apryr_final = cvg_month_totals_apr[4:11].strip(" ( u ' ")
    cvg_month_totals_aprnum_final = cvg_month_totals_apr[12:21].strip(" , ( u ' ) ")
    snowmonth_cvg.append('<tr>'+ '\n' +
                        '<td bgcolor="#1F618D" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Most in April<br />'+ '\n' +
                	'</p></td>'+ '\n' +
                    	'<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowmonth_cvg.append(cvg_month_totals_apryr_final)
    snowmonth_cvg.append('<br />'+'</p></td>'+ '<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="2"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowmonth_cvg.append(cvg_month_totals_aprnum_final + '"')
    snowmonth_cvg.append('<br />'+ '\n' +
                        '</p></td>'+ '\n' +
                        '</tr>'+ '\n')
    # DAY
    day_month_totals_apr = str(day_month_totals[6])
    day_month_totals_apryr_final = day_month_totals_apr[4:11].strip(" ( u ' ")
    day_month_totals_aprnum_final = day_month_totals_apr[12:21].strip(" , ( u ' ) ")
    snowmonth_day.append('<tr>'+ '\n' +
                        '<td bgcolor="#1F618D" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Most in April<br />'+ '\n' +
                	'</p></td>'+ '\n' +
                    	'<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowmonth_day.append(day_month_totals_apryr_final)
    snowmonth_day.append('<br />'+'</p></td>'+ '<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="2"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowmonth_day.append(day_month_totals_aprnum_final + '"')
    snowmonth_day.append('<br />'+ '\n' +
                        '</p></td>'+ '\n' +
                        '</tr>'+ '\n') 
    # CMH
    cmh_month_totals_apr = str(cmh_month_totals[6])
    cmh_month_totals_apryr_final = cmh_month_totals_apr[4:11].strip(" ( u ' ")
    cmh_month_totals_aprnum_final = cmh_month_totals_apr[12:21].strip(" , ( u ' ) ")
    snowmonth_cmh.append('<tr>'+ '\n' +
                        '<td bgcolor="#1F618D" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Most in April<br />'+ '\n' +
                	'</p></td>'+ '\n' +
                    	'<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowmonth_cmh.append(cmh_month_totals_apryr_final)
    snowmonth_cmh.append('<br />'+'</p></td>'+ '<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="2"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowmonth_cmh.append(cmh_month_totals_aprnum_final + '"')
    snowmonth_cmh.append('<br />'+ '\n' +
                        '</p></td>'+ '\n' +
                        '</tr>'+ '\n')
    # - #

    # Least in April
    # CVG
    cvg_least_month_totals_apr = str(cvg_least_month_totals[6])
    cvg_least_month_totals_apryr_final = cvg_least_month_totals_apr[4:11].strip(" ( u ' ")
    cvg_least_month_totals_aprnum_final = cvg_least_month_totals_apr[12:21].strip(" , ( u ' ) ")
    snowmonth_cvg.append('<tr>'+ '\n' +
                        '<td bgcolor="#1F618D" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Least in April<br />'+ '\n' +                	'</p></td>'+ '\n' +
                    	'<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowmonth_cvg.append(cvg_least_month_totals_apryr_final)
    snowmonth_cvg.append('<br />'+'</p></td>'+ '<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="2"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowmonth_cvg.append(cvg_least_month_totals_aprnum_final)
    if (cvg_least_month_totals_aprnum_final != 'T'):
        snowmonth_cvg.append('"')
    if star_needed_least_cvg[6] == 1:
        snowmonth_cvg.append(' *')
    snowmonth_cvg.append('<br />'+ '\n' +
                        '</p></td>'+ '\n' +
                        '</tr>'+ '\n')
    # DAY
    day_least_month_totals_apr = str(day_least_month_totals[6])
    day_least_month_totals_apryr_final = day_least_month_totals_apr[4:11].strip(" ( u ' ")
    day_least_month_totals_aprnum_final = day_least_month_totals_apr[12:21].strip(" , ( u ' ) ")
    snowmonth_day.append('<tr>'+ '\n' +
                        '<td bgcolor="#1F618D" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Least in April<br />'+ '\n' +                	'</p></td>'+ '\n' +
                    	'<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowmonth_day.append(day_least_month_totals_apryr_final)
    snowmonth_day.append('<br />'+'</p></td>'+ '<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="2"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowmonth_day.append(day_least_month_totals_aprnum_final)
    if (day_least_month_totals_aprnum_final != 'T'):
        snowmonth_day.append('"')
    if (star_needed_least_day[6] == 1):
        snowmonth_day.append(' *')
    snowmonth_day.append('<br />'+ '\n' +
                        '</p></td>'+ '\n' +
                        '</tr>'+ '\n')

    # CMH
    cmh_least_month_totals_apr = str(cmh_least_month_totals[6])
    cmh_least_month_totals_apryr_final = cmh_least_month_totals_apr[4:11].strip(" ( u ' ")
    cmh_least_month_totals_aprnum_final = cmh_least_month_totals_apr[12:21].strip(" , ( u ' ) ")
    snowmonth_cmh.append('<tr>'+ '\n' +
                        '<td bgcolor="#1F618D" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Least in April<br />'+ '\n' +                	'</p></td>'+ '\n' +
                    	'<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowmonth_cmh.append(cmh_least_month_totals_apryr_final)
    snowmonth_cmh.append('<br />'+'</p></td>'+ '<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="2"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowmonth_cmh.append(cmh_least_month_totals_aprnum_final)
    if (cmh_least_month_totals_aprnum_final != 'T'):
        snowmonth_cmh.append('"')
    if star_needed_least_cmh[6] == 1:
        snowmonth_cmh.append(' *')
    snowmonth_cmh.append('<br />'+ '\n' +
                        '</p></td>'+ '\n' +
                        '</tr>'+ '\n')
    # END SNOW MONTH #

    # Snow Year #
    # Earliest Seasonal Measurable Snow- CVG
    snowyear_cvg.append('<tr>' + '\n' +
                        '<td bgcolor="#1F618D" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Earliest Seasonal Measurable Snow<br />' + '\n' +
                        '</p></td>' + '\n' +
                        '<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowyear_cvg.append(value_earliest_snow_cvg)
    snowyear_cvg.append('" <br />' + '\n')
    snowyear_cvg.append('</p></td>' + '\n' +
                        '<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowyear_cvg.append(date_earliest_snow_cvg)
    snowyear_cvg.append('<br />' + '\n' +
                        '</p></td>' + '\n' +
                        '</tr>' + '\n')
    # Earliest Seasonal Measurable Snow- DAY
    snowyear_day.append('<tr>' + '\n' +
                        '<td bgcolor="#1F618D" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Earliest Seasonal Measurable Snow<br />' + '\n' +
                        '</p></font></td>' + '\n' +
                        '<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowyear_day.append(value_earliest_snow_day)
    snowyear_day.append('" <br />' + '\n')
    snowyear_day.append('</p></td>' + '\n' +
                        '<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowyear_day.append(date_earliest_snow_day)
    snowyear_day.append('<br />' + '\n' +
                        '</p></td>' + '\n' +
                        '</tr>' + '\n')
    # Earliest Seasonal Measurable Snow- CMH
    snowyear_cmh.append('<tr>' + '\n' +
                        '<td bgcolor="#1F618D" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Earliest Seasonal Measurable Snow<br />' + '\n' +
                        '</p></td>' + '\n' +
                        '<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowyear_cmh.append(value_earliest_snow_cmh)
    snowyear_cmh.append('" <br />' + '\n')
    snowyear_cmh.append('</p></td>' + '\n' +
                        '<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowyear_cmh.append(date_earliest_snow_cmh)
    snowyear_cmh.append('<br />' + '\n' +
                        '</p></td>' + '\n' +
                        '</tr>' + '\n')

    
    # Latest First Seasonal Measurable Snow- CVG
    snowyear_cvg.append('<tr>' + '\n' +
                        '<td bgcolor="#1F618D" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Latest Seasonal First Measurable Snow<br />' + '\n' +
                        '</p></td>' + '\n' +
                        '<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowyear_cvg.append(value_latest_earliest_snow_cvg)
    snowyear_cvg.append('" <br />' + '\n')
    snowyear_cvg.append('</p></td>' + '\n' +
                        '<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowyear_cvg.append(date_latest_earliest_snow_cvg)
    snowyear_cvg.append('<br />' + '\n' +
                        '</p></td>' + '\n' +
                        '</tr>' + '\n')
    # Latest First Seasonal Measurable Snow- DAY
    snowyear_day.append('<tr>' + '\n' +
                        '<td bgcolor="#1F618D" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Latest Seasonal First Measurable Snow<br />' + '\n' +
                        '</p></td>' + '\n' +
                        '<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowyear_day.append(value_latest_earliest_snow_day)
    snowyear_day.append('" <br />' + '\n')
    snowyear_day.append('</p></td>' + '\n' +
                        '<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowyear_day.append(date_latest_earliest_snow_day)
    snowyear_day.append('<br />' + '\n' +
                        '</p></td>' + '\n' +
                        '</tr>' + '\n')
    # Latest First Seasonal Measurable Snow- CMH
    snowyear_cmh.append('<tr>' + '\n' +
                        '<td bgcolor="#1F618D" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Latest Seasonal First Measurable Snow<br />' + '\n' +
                        '</p></td>' + '\n' +
                        '<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowyear_cmh.append(value_latest_earliest_snow_cmh)
    snowyear_cmh.append('" <br />' + '\n')
    snowyear_cmh.append('</p></td>' + '\n' +
                        '<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowyear_cmh.append(date_latest_earliest_snow_cmh)
    snowyear_cmh.append('<br />' + '\n' +
                        '</p></td>' + '\n' +
                        '</tr>' + '\n')

    # Normal First Seasonal Measurable Snow- CVG
    snowyear_cvg.append('<tr>' + '\n' +
                        '<td bgcolor="#1F618D" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Normal First Measurable Snow (1981-2010)<br />' + '\n' +
                        '</p></td>' + '\n' +
                        '<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="2"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowyear_cvg.append(date_normal_first_snow_cvg)
    snowyear_cvg.append('<br />' + '\n')
    snowyear_cvg.append('</p></td>' + '\n')
    snowyear_cvg.append('</tr>' + '\n')
    # Normal First Seasonal Measurable Snow- DAY
    snowyear_day.append('<tr>' + '\n' +
                        '<td bgcolor="#1F618D" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Normal First Measurable Snow (1981-2010)<br />' + '\n' +
                        '</p></td>' + '\n' +
                        '<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="2"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowyear_day.append(date_normal_first_snow_day)
    snowyear_day.append('<br />' + '\n')
    snowyear_day.append('</p></td>' + '\n')
    snowyear_day.append('</tr>' + '\n')
    # Normal First Seasonal Measurable Snow- CMH
    snowyear_cmh.append('<tr>' + '\n' +
                        '<td bgcolor="#1F618D" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Normal First Measurable Snow (1981-2010)<br />' + '\n' +
                        '</p></td>' + '\n' +
                        '<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="2"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowyear_cmh.append(date_normal_first_snow_cmh)
    snowyear_cmh.append('<br />' + '\n')
    snowyear_cmh.append('</p></td>' + '\n')
    snowyear_cmh.append('</tr>' + '\n')


    # Normal First Seasonal 1" Snow- CVG
    snowyear_cvg.append('<tr>' + '\n' +
                        '<td bgcolor="#1F618D" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Normal First Snow Of At Least 1"(1981-2010)<br />' + '\n' +
                        '</p></td>' + '\n' +
                        '<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="2"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowyear_cvg.append(date_normal_firstmeasure_snow_cvg)
    snowyear_cvg.append('<br />' + '\n')
    snowyear_cvg.append('</p></td>' + '\n')
    snowyear_cvg.append('</tr>' + '\n')
    # Normal First Seasonal 1" Snow- DAY
    snowyear_day.append('<tr>' + '\n' +
                        '<td bgcolor="#1F618D" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Normal First Snow Of At Least 1"(1981-2010)<br />' + '\n' +
                        '</p></td>' + '\n' +
                        '<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="2"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowyear_day.append(date_normal_firstmeasure_snow_day)
    snowyear_day.append('<br />' + '\n')
    snowyear_day.append('</p></td>' + '\n')
    snowyear_day.append('</tr>' + '\n')
    # Normal First Seasonal 1" Snow- CMH
    snowyear_cmh.append('<tr>' + '\n' +
                        '<td bgcolor="#1F618D" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Normal First Snow Of At Least 1"(1981-2010)<br />' + '\n' +
                        '</p></td>' + '\n' +
                        '<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="2"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowyear_cmh.append(date_normal_firstmeasure_snow_cmh)
    snowyear_cmh.append('<br />' + '\n')
    snowyear_cmh.append('</p></td>' + '\n')
    snowyear_cmh.append('</tr>' + '\n')


    # Latest Seasonal Measurable Snow- CVG
    snowyear_cvg.append('<tr>' + '\n' +
                        '<td bgcolor="#1F618D" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Latest Seasonal Measurable Snow<br />' + '\n' +
                        '</p></td>' + '\n' +
                        '<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowyear_cvg.append(value_latest_snow_cvg)
    snowyear_cvg.append('" <br />' + '\n')
    snowyear_cvg.append('</p></td>' + '\n' +
                        '<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowyear_cvg.append(date_latest_snow_cvg)
    snowyear_cvg.append('<br />' + '\n' +
                        '</p></td>' + '\n' +
                        '</tr>' + '\n')
    # Latest Seasonal Measurable Snow- DAY
    snowyear_day.append('<tr>' + '\n' +
                        '<td bgcolor="#1F618D" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Latest Seasonal Measurable Snow<br />' + '\n' +
                        '</p></td>' + '\n' +
                        '<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowyear_day.append(value_latest_snow_day)
    snowyear_day.append('" <br />' + '\n')
    snowyear_day.append('</p></td>' + '\n' +
                        '<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowyear_day.append(date_latest_snow_day)
    snowyear_day.append('<br />' + '\n' +
                        '</p></td>' + '\n' +
                        '</tr>' + '\n')
    # Latest Seasonal Measurable Snow- CMH
    snowyear_cmh.append('<tr>' + '\n' +
                        '<td bgcolor="#1F618D" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Latest Seasonal Measurable Snow<br />' + '\n' +
                        '</p></td>' + '\n' +
                        '<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowyear_cmh.append(value_latest_snow_cmh)
    snowyear_cmh.append('" <br />' + '\n')
    snowyear_cmh.append('</p></td>' + '\n' +
                        '<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowyear_cmh.append(date_latest_snow_cmh)
    snowyear_cmh.append('<br />' + '\n' +
                        '</p></td>' + '\n' +
                        '</tr>' + '\n')

    # Latest Seasonal 1" Snow- CVG
    snowyear_cvg.append('<tr>' + '\n' +
                        '<td bgcolor="#1F618D" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Latest Seasonal Snow Of At Least 1"<br />' + '\n' +
                        '</p></td>' + '\n' +
                        '<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowyear_cvg.append(value_latestone_snow_cvg)
    snowyear_cvg.append('" <br />' + '\n')
    snowyear_cvg.append('</p></td>' + '\n' +
                        '<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowyear_cvg.append(date_latestone_snow_cvg)
    snowyear_cvg.append('<br />' + '\n' +
                        '</p></td>' + '\n' +
                        '</tr>' + '\n')
    # Latest Seasonal 1" Snow- DAY
    snowyear_day.append('<tr>' + '\n' +
                        '<td bgcolor="#1F618D" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Latest Seasonal Snow Of At Least 1"<br />' + '\n' +
                        '</p></td>' + '\n' +
                        '<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowyear_day.append(value_latestone_snow_day)
    snowyear_day.append('" <br />' + '\n')
    snowyear_day.append('</p></td>' + '\n' +
                        '<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowyear_day.append(date_latestone_snow_day)
    snowyear_day.append('<br />' + '\n' +
                        '</p></td>' + '\n' +
                        '</tr>' + '\n')
    # Latest Seasonal 1" Snow- CMH
    snowyear_cmh.append('<tr>' + '\n' +
                        '<td bgcolor="#1F618D" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Latest Seasonal Snow Of At Least 1"<br />' + '\n' +
                        '</p></td>' + '\n' +
                        '<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowyear_cmh.append(value_latestone_snow_cmh)
    snowyear_cmh.append('" <br />' + '\n')
    snowyear_cmh.append('</p></td>' + '\n' +
                        '<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowyear_cmh.append(date_latestone_snow_cmh)
    snowyear_cmh.append('<br />' + '\n' +
                        '</p></td>' + '\n' +
                        '</tr>' + '\n')

    # Earliest Last Seasonal Measurable Snow- CVG
    snowyear_cvg.append('<tr>' + '\n' +
                        '<td bgcolor="#1F618D" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Earliest Last Seasonal Measurable Snow<br />' + '\n' +
                        '</p></td>' + '\n' +
                        '<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowyear_cvg.append(value_earliestlatest_snow_cvg)
    snowyear_cvg.append('" <br />' + '\n')
    snowyear_cvg.append('</p></td>' + '\n' +
                        '<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowyear_cvg.append(date_earliestlatest_snow_cvg)
    snowyear_cvg.append('<br />' + '\n' +
                        '</p></td>' + '\n' +
                        '</tr>' + '\n')
    # Earliest Last Seasonal Measurable Snow- DAY
    snowyear_day.append('<tr>' + '\n' +
                        '<td bgcolor="#1F618D" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Earliest Last Seasonal Measurable Snow<br />' + '\n' +
                        '</p></td>' + '\n' +
                        '<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowyear_day.append(value_earliestlatest_snow_day)
    snowyear_day.append('" <br />' + '\n')
    snowyear_day.append('</p></td>' + '\n' +
                        '<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowyear_day.append(date_earliestlatest_snow_day)
    snowyear_day.append('<br />' + '\n' +
                        '</p></td>' + '\n' +
                        '</tr>' + '\n')
    # Earliest Last Seasonal Measurable Snow- CMH
    snowyear_cmh.append('<tr>' + '\n' +
                        '<td bgcolor="#1F618D" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Earliest Last Seasonal Measurable Snow<br />' + '\n' +
                        '</p></td>' + '\n' +
                        '<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowyear_cmh.append(value_earliestlatest_snow_cmh)
    snowyear_cmh.append('" <br />' + '\n')
    snowyear_cmh.append('</p></td>' + '\n' +
                        '<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowyear_cmh.append(date_earliestlatest_snow_cmh)
    snowyear_cmh.append('<br />' + '\n' +
                        '</p></td>' + '\n' +
                        '</tr>' + '\n')

    # Most Snow in a Calendar Year- CVG
    snowyear_cvg.append('<tr>' + '\n' +
                        '<td bgcolor="#884EA0" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Most In A Calendar Year<br />' + '\n' +
                        '</p></td>' + '\n' +
                        '<td bgcolor="#C39BD3" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowyear_cvg.append(value_most_snow_cvg)
    snowyear_cvg.append('" <br />' + '\n')
    snowyear_cvg.append('</p></td>' + '\n' +
                        '<td bgcolor="#C39BD3" style="vertical-align: middle" align="center" colspan="2"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowyear_cvg.append(date_most_snow_cvg[0:4])
    snowyear_cvg.append('<br />' + '\n' +
                        '</p></td>' + '\n' +
                        '</tr>' + '\n')
    # Most Snow in a Calendar Year- DAY
    snowyear_day.append('<tr>' + '\n' +
                        '<td bgcolor="#884EA0" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Most In A Calendar Year<br />' + '\n' +
                        '</p></td>' + '\n' +
                        '<td bgcolor="#C39BD3" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowyear_day.append(value_most_snow_day)
    snowyear_day.append('" <br />' + '\n')
    snowyear_day.append('</p></td>' + '\n' +
                        '<td bgcolor="#C39BD3" style="vertical-align: middle" align="center" colspan="2"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowyear_day.append(date_most_snow_day[0:4])
    snowyear_day.append('<br />' + '\n' +
                        '</p></td>' + '\n' +
                        '</tr>' + '\n')
    # Most Snow in a Calendar Year- CMH
    snowyear_cmh.append('<tr>' + '\n' +
                        '<td bgcolor="#884EA0" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Most In A Calendar Year<br />' + '\n' +
                        '</p></td>' + '\n' +
                        '<td bgcolor="#C39BD3" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowyear_cmh.append(value_most_snow_cmh)
    snowyear_cmh.append('" <br />' + '\n')
    snowyear_cmh.append('</p></td>' + '\n' +
                        '<td bgcolor="#C39BD3" style="vertical-align: middle" align="center" colspan="2"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowyear_cmh.append(date_most_snow_cmh[0:4])
    snowyear_cmh.append('<br />' + '\n' +
                        '</p></td>' + '\n' +
                        '</tr>' + '\n')

    # Least Snow in a Calendar Year- CVG
    snowyear_cvg.append('<tr>' + '\n' +
                        '<td bgcolor="#884EA0" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Least In A Calendar Year<br />' + '\n' +
                        '</p></td>' + '\n' +
                        '<td bgcolor="#C39BD3" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowyear_cvg.append(value_least_snow_cvg)
    snowyear_cvg.append('" <br />' + '\n')
    snowyear_cvg.append('</p></td>' + '\n' +
                        '<td bgcolor="#C39BD3" style="vertical-align: middle" align="center" colspan="2"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowyear_cvg.append(date_least_snow_cvg[0:4])
    snowyear_cvg.append('<br />' + '\n' +
                        '</p></td>' + '\n' +
                        '</tr>' + '\n')
    # Least Snow in a Calendar Year- DAY
    snowyear_day.append('<tr>' + '\n' +
                        '<td bgcolor="#884EA0" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Least In A Calendar Year<br />' + '\n' +
                        '</p></td>' + '\n' +
                        '<td bgcolor="#C39BD3" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowyear_day.append(value_least_snow_day)
    snowyear_day.append('" <br />' + '\n')
    snowyear_day.append('</p></td>' + '\n' +
                        '<td bgcolor="#C39BD3" style="vertical-align: middle" align="center" colspan="2"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowyear_day.append(date_least_snow_day[0:4])
    snowyear_day.append('<br />' + '\n' +
                        '</p></td>' + '\n' +
                        '</tr>' + '\n')
    # Least Snow in a Calendar Year- CMH
    snowyear_cmh.append('<tr>' + '\n' +
                        '<td bgcolor="#884EA0" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Least In A Calendar Year<br />' + '\n' +
                        '</p></td>' + '\n' +
                        '<td bgcolor="#C39BD3" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowyear_cmh.append(value_least_snow_cmh)
    snowyear_cmh.append('" <br />' + '\n')
    snowyear_cmh.append('</p></td>' + '\n' +
                        '<td bgcolor="#C39BD3" style="vertical-align: middle" align="center" colspan="2"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowyear_cmh.append(date_least_snow_cmh[0:4])
    snowyear_cmh.append('<br />' + '\n' +
                        '</p></td>' + '\n' +
                        '</tr>' + '\n')

    # Most Snow in a Season Year- CVG
    snowyear_cvg.append('<tr>' + '\n' +
                        '<td bgcolor="#884EA0" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Most in a Season<br />' + '\n' +
                        '</p></td>' + '\n' +
                        '<td bgcolor="#C39BD3" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowyear_cvg.append(value_most_seasonyear_snow_cvg)
    snowyear_cvg.append('" <br />' + '\n')
    snowyear_cvg.append('</p></td>' + '\n' +
                        '<td bgcolor="#C39BD3" style="vertical-align: middle" align="center" colspan="2"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowyear_cvg.append(date_most_seasonyear_snow_cvg[0:4])
    snowyear_cvg.append('<br />' + '\n' +
                        '</p></td>' + '\n' +
                        '</tr>' + '\n')
    # Most Snow in a Season Year- DAY
    snowyear_day.append('<tr>' + '\n' +
                        '<td bgcolor="#884EA0" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Most in a Season<br />' + '\n' +
                        '</p></td>' + '\n' +
                        '<td bgcolor="#C39BD3" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowyear_day.append(value_most_seasonyear_snow_day)
    snowyear_day.append('" <br />' + '\n')
    snowyear_day.append('</p></td>' + '\n' +
                        '<td bgcolor="#C39BD3" style="vertical-align: middle" align="center" colspan="2"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowyear_day.append(date_most_seasonyear_snow_day[0:4])
    snowyear_day.append('<br />' + '\n' +
                        '</p></td>' + '\n' +
                        '</tr>' + '\n')
    # Most Snow in a Season Year- CMH
    snowyear_cmh.append('<tr>' + '\n' +
                        '<td bgcolor="#884EA0" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Most in a Season<br />' + '\n' +
                        '</p></td>' + '\n' +
                        '<td bgcolor="#C39BD3" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowyear_cmh.append(value_most_seasonyear_snow_cmh)
    snowyear_cmh.append('" <br />' + '\n')
    snowyear_cmh.append('</p></td>' + '\n' +
                        '<td bgcolor="#C39BD3" style="vertical-align: middle" align="center" colspan="2"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowyear_cmh.append(date_most_seasonyear_snow_cmh[0:4])
    snowyear_cmh.append('<br />' + '\n' +
                        '</p></td>' + '\n' +
                        '</tr>' + '\n')

    # Least Snow in a Season Year- CVG
    snowyear_cvg.append('<tr>' + '\n' +
                        '<td bgcolor="#884EA0" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Least in a Season<br />' + '\n' +
                        '</p></td>' + '\n' +
                        '<td bgcolor="#C39BD3" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowyear_cvg.append(value_least_seasonyear_snow_cvg)
    snowyear_cvg.append('" <br />' + '\n')
    snowyear_cvg.append('</p></td>' + '\n' +
                        '<td bgcolor="#C39BD3" style="vertical-align: middle" align="center" colspan="2"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowyear_cvg.append(date_least_seasonyear_snow_cvg[0:4])
    snowyear_cvg.append('<br />' + '\n' +
                        '</p></td>' + '\n' +
                        '</tr>' + '\n')
    # Least Snow in a Season Year- DAY
    snowyear_day.append('<tr>' + '\n' +
                        '<td bgcolor="#884EA0" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Least in a Season<br />' + '\n' +
                        '</p></td>' + '\n' +
                        '<td bgcolor="#C39BD3" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowyear_day.append(value_least_seasonyear_snow_day)
    snowyear_day.append('" <br />' + '\n')
    snowyear_day.append('</p></td>' + '\n' +
                        '<td bgcolor="#C39BD3" style="vertical-align: middle" align="center" colspan="2"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowyear_day.append(date_least_seasonyear_snow_day[0:4])
    snowyear_day.append('<br />' + '\n' +
                        '</p></td>' + '\n' +
                        '</tr>' + '\n')
    # Least Snow in a Season Year- CMH
    snowyear_cmh.append('<tr>' + '\n' +
                        '<td bgcolor="#884EA0" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Least in a Season<br />' + '\n' +
                        '</p></td>' + '\n' +
                        '<td bgcolor="#C39BD3" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowyear_cmh.append(value_least_seasonyear_snow_cmh)
    snowyear_cmh.append('" <br />' + '\n')
    snowyear_cmh.append('</p></td>' + '\n' +
                        '<td bgcolor="#C39BD3" style="vertical-align: middle" align="center" colspan="2"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowyear_cmh.append(date_least_seasonyear_snow_cmh[0:4])
    snowyear_cmh.append('<br />' + '\n' +
                        '</p></td>' + '\n' +
                        '</tr>' + '\n')

    # Most Days with daily snowfall >1" in a season- CVG
    snowyear_cvg.append('<tr>' + '\n' +
                        '<td bgcolor="#1F618D" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Most Days With Daily Snowfall >=1" In A Season<br />' + '\n' +
                        '</p></td>' + '\n' +
                        '<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowyear_cvg.append(value_most_daysone_snow_cvg)
    snowyear_cvg.append('<br />' + '\n')
    snowyear_cvg.append('</p></td>' + '\n' +
                        '<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowyear_cvg.append(str(int(date_most_daysone_snow_cvg[0:4])-1) + "-" + date_most_daysone_snow_cvg[0:4])
    snowyear_cvg.append('<br />' + '\n' +
                        '</p></td>' + '\n' +
                        '</tr>' + '\n')
    # Most Days with daily snowfall >1" in a season- DAY
    snowyear_day.append('<tr>' + '\n' +
                        '<td bgcolor="#1F618D" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Most Days With Daily Snowfall >=1" In A Season<br />' + '\n' +
                        '</p></td>' + '\n' +
                        '<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowyear_day.append(value_most_daysone_snow_day)
    snowyear_day.append('<br />' + '\n')
    snowyear_day.append('</p></td>' + '\n' +
                        '<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowyear_day.append(str(int(date_most_daysone_snow_day[0:4])-1) + "-" + date_most_daysone_snow_day[0:4])
    snowyear_day.append('<br />' + '\n' +
                        '</p></td>' + '\n' +
                        '</tr>' + '\n')
    # Most Days with daily snowfall >1" in a season- CMH
    snowyear_cmh.append('<tr>' + '\n' +
                        '<td bgcolor="#1F618D" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Most Days With Daily Snowfall >=1" In A Season<br />' + '\n' +
                        '</p></td>' + '\n' +
                        '<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowyear_cmh.append(value_most_daysone_snow_cmh)
    snowyear_cmh.append('<br />' + '\n')
    snowyear_cmh.append('</p></td>' + '\n' +
                        '<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowyear_cmh.append(str(int(date_most_daysone_snow_cmh[0:4])-1) + "-" + date_most_daysone_snow_cmh[0:4])
    snowyear_cmh.append('<br />' + '\n' +
                        '</p></td>' + '\n' +
                        '</tr>' + '\n')

    # Most days with measurable snowfall in a season- CVG
    snowyear_cvg.append('<tr>' + '\n' +
                        '<td bgcolor="#1F618D" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Most Days With Measurable Snowfall In A Season<br />' + '\n' +
                        '</p></td>' + '\n' +
                        '<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowyear_cvg.append(value_most_daystrace_snow_cvg)
    snowyear_cvg.append('<br />' + '\n')
    snowyear_cvg.append('</p></td>' + '\n' +
                        '<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowyear_cvg.append(str(int(date_most_daystrace_snow_cvg[0:4])-1) + "-" + date_most_daystrace_snow_cvg[0:4])
    snowyear_cvg.append('<br />' + '\n' +
                        '</p></td>' + '\n' +
                        '</tr>' + '\n')
    # Most days with measurable snowfall in a season- DAY
    snowyear_day.append('<tr>' + '\n' +
                        '<td bgcolor="#1F618D" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Most Days With Measurable Snowfall In A Season<br />' + '\n' +
                        '</p></td>' + '\n' +
                        '<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowyear_day.append(value_most_daystrace_snow_day)
    snowyear_day.append('<br />' + '\n')
    snowyear_day.append('</p></td>' + '\n' +
                        '<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowyear_day.append(str(int(date_most_daystrace_snow_day[0:4])-1) + "-" + date_most_daystrace_snow_day[0:4])
    snowyear_day.append('<br />' + '\n' +
                        '</p></td>' + '\n' +
                        '</tr>' + '\n')
    # Most days with measurable snowfall in a season- CMH
    snowyear_cmh.append('<tr>' + '\n' +
                        '<td bgcolor="#1F618D" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Most Days With Measurable Snowfall In A Season<br />' + '\n' +
                        '</p></td>' + '\n' +
                        '<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowyear_cmh.append(value_most_daystrace_snow_cmh)
    snowyear_cmh.append('<br />' + '\n')
    snowyear_cmh.append('</p></td>' + '\n' +
                        '<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowyear_cmh.append(str(int(date_most_daystrace_snow_cmh[0:4])-1) + "-" + date_most_daystrace_snow_cmh[0:4])
    snowyear_cmh.append('<br />' + '\n' +
                        '</p></td>' + '\n' +
                        '</tr>' + '\n')

    # Highest recorded daily snowfall- CVG
    snowyear_cvg.append('<tr>' + '\n' +
                        '<td bgcolor="#1F618D" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Most In 1 Day<br />' + '\n' +
                        '</p></td>' + '\n' +
                        '<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowyear_cvg.append(value_most_daily_snow_cvg)
    snowyear_cvg.append('" <br />' + '\n')
    snowyear_cvg.append('</p></td>' + '\n' +
                        '<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowyear_cvg.append(date_most_daily_snow_cvg)
    snowyear_cvg.append('<br />' + '\n' +
                        '</p></td>' + '\n' +
                        '</tr>' + '\n')
    # Highest recorded daily snowfall- DAY
    snowyear_day.append('<tr>' + '\n' +
                        '<td bgcolor="#1F618D" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Most In 1 Day<br />' + '\n' +
                        '</p></td>' + '\n' +
                        '<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowyear_day.append(value_most_daily_snow_day)
    snowyear_day.append('" <br />' + '\n')
    snowyear_day.append('</p></td>' + '\n' +
                        '<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowyear_day.append(date_most_daily_snow_day)
    snowyear_day.append('<br />' + '\n' +
                        '</p></td>' + '\n' +
                        '</tr>' + '\n')
    # Highest recorded daily snowfall- CMH
    snowyear_cmh.append('<tr>' + '\n' +
                        '<td bgcolor="#1F618D" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Most In 1 Day<br />' + '\n' +
                        '</p></td>' + '\n' +
                        '<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowyear_cmh.append(value_most_daily_snow_cmh)
    snowyear_cmh.append('" <br />' + '\n')
    snowyear_cmh.append('</p></td>' + '\n' +
                        '<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowyear_cmh.append(date_most_daily_snow_cmh)
    snowyear_cmh.append('<br />' + '\n' +
                        '</p></td>' + '\n' +
                        '</tr>' + '\n')

    # Highest two day snowfall- CVG
    snowyear_cvg.append('<tr>' + '\n' +
                        '<td bgcolor="#1F618D" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Most In 2 Consective Days (2nd Day Shown)<br />' + '\n' +
                        '</p></td>' + '\n' +
                        '<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowyear_cvg.append(value_most_twodaily_snow_cvg)
    snowyear_cvg.append('" <br />' + '\n')
    snowyear_cvg.append('</p></td>' + '\n' +
                        '<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowyear_cvg.append(date_most_twodaily_snow_cvg)
    snowyear_cvg.append('<br />' + '\n' +
                        '</p></td>' + '\n' +
                        '</tr>' + '\n')
    # Highest two day snowfall- DAY
    snowyear_day.append('<tr>' + '\n' +
                        '<td bgcolor="#1F618D" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Most In 2 Consective Days (2nd Day Shown)<br />' + '\n' +
                        '</p></td>' + '\n' +
                        '<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowyear_day.append(value_most_twodaily_snow_day)
    snowyear_day.append('" <br />' + '\n')
    snowyear_day.append('</p></td>' + '\n' +
                        '<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowyear_day.append(date_most_twodaily_snow_day)
    snowyear_day.append('<br />' + '\n' +
                        '</p></td>' + '\n' +
                        '</tr>' + '\n')
    # Highest two day snowfall- CMH
    snowyear_cmh.append('<tr>' + '\n' +
                        '<td bgcolor="#1F618D" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Most In 2 Consective Days (2nd Day Shown)<br />' + '\n' +
                        '</p></td>' + '\n' +
                        '<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowyear_cmh.append(value_most_twodaily_snow_cmh)
    snowyear_cmh.append('" <br />' + '\n')
    snowyear_cmh.append('</p></td>' + '\n' +
                        '<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowyear_cmh.append(date_most_twodaily_snow_cmh)
    snowyear_cmh.append('<br />' + '\n' +
                        '</p></td>' + '\n' +
                        '</tr>' + '\n')

    # Longest Stretch of Measurable Snowfall-CVG
    for j in range(len(final_data_longest_measure_snow_cvg)):
        snowyear_cvg.append('<tr>'+ '\n')
        if j == 0:
            if (len(final_data_longest_measure_snow_cvg)) > 1:
                snowyear_cvg.append('<td bgcolor="#1F618D" style="vertical-align: middle" align="center" rowspan="' + str(len(final_data_longest_measure_snow_cvg)) + '" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Longest Stretch of Measurable Snowfall (End Date)<br />'+ '\n' +
                                    '</p></td>'+ '\n')
            else:
                snowyear_cvg.append('<td bgcolor="#1F618D" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Longest Stretch (End Date)<br />'+ '\n' +
                                    '</p></td>'+ '\n')
            snowyear_cvg.append('<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
            snowyear_cvg.append(str(final_data_longest_measure_snow_cvg[j][0]))
            snowyear_cvg.append('<br />'+ '\n' +
                                '</p></td>'+ '\n' +
                                '<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="2"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
            snowyear_cvg.append(str(final_data_longest_measure_snow_cvg[j][1]))
            snowyear_cvg.append('<br />'+ '\n'
                                '</p></td>'+ '\n')	
        if j > 0:
            snowyear_cvg.append('<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
            snowyear_cvg.append(str(final_data_longest_measure_snow_cvg[j][0]))
            snowyear_cvg.append('<br />'+ '\n' +
                                '</p></td>'+ '\n' +
                                '<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="2"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
            snowyear_cvg.append(str(final_data_longest_measure_snow_cvg[j][1]))
            snowyear_cvg.append('<br />'+ '\n'
                                '</p></td>'+ '\n')			
    snowyear_cvg.append('</tr>'+ '\n')
    # Longest Stretch of Measurable Snowfall-DAY
    for j in range(len(final_data_longest_measure_snow_day)):
        snowyear_day.append('<tr>'+ '\n')
        if j == 0:
            if (len(final_data_longest_measure_snow_day)) > 1:
                snowyear_day.append('<td bgcolor="#1F618D" style="vertical-align: middle" align="center" rowspan="' + str(len(final_data_longest_measure_snow_day)) + '" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Longest Stretch of Measurable Snowfall (End Date)<br />'+ '\n' +
                                    '</p></td>'+ '\n')
            else:
                snowyear_day.append('<td bgcolor="#1F618D" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Longest Stretch (End Date)<br />'+ '\n' +
                                    '</p></td>'+ '\n')
            snowyear_day.append('<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
            snowyear_day.append(str(final_data_longest_measure_snow_day[j][0]))
            snowyear_day.append('<br />'+ '\n' +
                                '</p></td>'+ '\n' +
                                '<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="2"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
            snowyear_day.append(str(final_data_longest_measure_snow_day[j][1]))
            snowyear_day.append('<br />'+ '\n'
                                '</p></td>'+ '\n')	
        if j > 0:
            snowyear_day.append('<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
            snowyear_day.append(str(final_data_longest_measure_snow_day[j][0]))
            snowyear_day.append('<br />'+ '\n' +
                                '</p></td>'+ '\n' +
                                '<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="2"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
            snowyear_day.append(str(final_data_longest_measure_snow_day[j][1]))
            snowyear_day.append('<br />'+ '\n'
                                '</p></td>'+ '\n')			
    snowyear_day.append('</tr>'+ '\n')
    # Longest Stretch of Measurable Snowfall-CMH
    for j in range(len(final_data_longest_measure_snow_cmh)):
        snowyear_cmh.append('<tr>'+ '\n')
        if j == 0:
            if (len(final_data_longest_measure_snow_cmh)) > 1:
                snowyear_cmh.append('<td bgcolor="#1F618D" style="vertical-align: middle" align="center" rowspan="' + str(len(final_data_longest_measure_snow_cmh)) + '" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Longest Stretch of Measurable Snowfall (End Date)<br />'+ '\n' +
                                    '</p></td>'+ '\n')
            else:
                snowyear_cmh.append('<td bgcolor="#1F618D" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Longest Stretch (End Date)<br />'+ '\n' +
                                    '</p></td>'+ '\n')
            snowyear_cmh.append('<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
            snowyear_cmh.append(str(final_data_longest_measure_snow_cmh[j][0]))
            snowyear_cmh.append('<br />'+ '\n' +
                                '</p></td>'+ '\n' +
                                '<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="2"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
            snowyear_cmh.append(str(final_data_longest_measure_snow_cmh[j][1]))
            snowyear_cmh.append('<br />'+ '\n'
                                '</p></td>'+ '\n')	
        if j > 0:
            snowyear_cmh.append('<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
            snowyear_cmh.append(str(final_data_longest_measure_snow_cmh[j][0]))
            snowyear_cmh.append('<br />'+ '\n' +
                                '</p></td>'+ '\n' +
                                '<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="2"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
            snowyear_cmh.append(str(final_data_longest_measure_snow_cmh[j][1]))
            snowyear_cmh.append('<br />'+ '\n'
                                '</p></td>'+ '\n')			
    snowyear_cmh.append('</tr>'+ '\n')

    # END SNOW YEAR #

    # Add other static text (period of record/ normal)
    # CVG
    snowmonth_cvg.append('<tr>'+ '\n' +
			'<td bgcolor="#424949" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Period of Record<br />'+ '\n' +
			'</p></td>'+ '\n' +
			'<td bgcolor="#CCD1D1" style="vertical-align: middle" align="center" colspan="3"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">1873 - Present<br />'+ '\n' +
			'</p></td>'+ '\n' +
		        '</tr>'+ '\n' +
		        '<tr>'+ '\n' +
			'<td bgcolor="#424949" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Normal Period<br />'+ '\n' +
			'</p></td>'+ '\n' +
			'<td bgcolor="#CCD1D1" style="vertical-align: middle" align="center" colspan="3"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">1981 - 2010<br />'+ '\n' +
			'</p></td>'+ '\n' +
		        '</tr>'+ '\n' +
                        '</tbody>'+ '\n' +
                        '</table>'+ '\n' +
                        '<p style="font-size: 12px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">' + '\n' +
                        '* Multiple years tied this record. Only the latest year is shown.</p>')
    # DAY
    snowmonth_day.append('<tr>'+ '\n' +
			'<td bgcolor="#424949" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Period of Record<br />'+ '\n' +
			'</p></td>'+ '\n' +
			'<td bgcolor="#CCD1D1" style="vertical-align: middle" align="center" colspan="3"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">1894 - Present<br />'+ '\n' +
			'</p></td>'+ '\n' +
		        '</tr>'+ '\n' +
		        '<tr>'+ '\n' +
			'<td bgcolor="#424949" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Normal Period<br />'+ '\n' +
			'</p></td>'+ '\n' +
			'<td bgcolor="#CCD1D1" style="vertical-align: middle" align="center" colspan="3"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">1981 - 2010<br />'+ '\n' +
			'</p></td>'+ '\n' +
		        '</tr>'+ '\n' +
                        '</tbody>'+ '\n' +
                        '</table>'+ '\n' +
                        '<p style="font-size: 12px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">' + '\n' +
                        '* Multiple years tied this record. Only the latest year is shown.</p>')
    # CMH
    snowmonth_cmh.append('<tr>'+ '\n' +
			'<td bgcolor="#424949" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Period of Record<br />'+ '\n' +
			'</p></td>'+ '\n' +
			'<td bgcolor="#CCD1D1" style="vertical-align: middle" align="center" colspan="3"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">1879 - Present<br />'+ '\n' +
			'</p></td>'+ '\n' +
		        '</tr>'+ '\n' +
		        '<tr>'+ '\n' +
			'<td bgcolor="#424949" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Normal Period<br />'+ '\n' +
			'</p></td>'+ '\n' +
			'<td bgcolor="#CCD1D1" style="vertical-align: middle" align="center" colspan="3"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">1981 - 2010<br />'+ '\n' +
			'</p></td>'+ '\n' +
		        '</tr>'+ '\n' +
                        '</tbody>'+ '\n' +
                        '</table>'+ '\n' +
                        '<p style="font-size: 12px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">' + '\n' +
                        '* Multiple years tied this record. Only the latest year is shown.</p>')

    # CVG
    snowyear_cvg.append('<tr>'+ '\n' +
			'<td bgcolor="#424949" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Period of Record<br />'+ '\n' +
			'</p></td>'+ '\n' +
			'<td bgcolor="#CCD1D1" style="vertical-align: middle" align="center" colspan="3"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">1893 - Present<br />'+ '\n' +
			'</p></td>'+ '\n' +
		        '</tr>'+ '\n' +
		        '<tr>'+ '\n' +
			'<td bgcolor="#424949" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Normal Period<br />'+ '\n' +
			'</p></td>'+ '\n' +
			'<td bgcolor="#CCD1D1" style="vertical-align: middle" align="center" colspan="3"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">1981 - 2010<br />'+ '\n' +
			'</p></td>'+ '\n' +
		        '</tr>'+ '\n' +
                        '</tbody>'+ '\n' +
                        '</table>'+ '\n' +
                        '<p style="font-size: 12px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">' + '\n' +
                        '* Multiple years tied this record. Only the latest year is shown.</p>')
    # DAY
    snowyear_day.append('<tr>'+ '\n' +
			'<td bgcolor="#424949" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Period of Record<br />'+ '\n' +
			'</p></td>'+ '\n' +
			'<td bgcolor="#CCD1D1" style="vertical-align: middle" align="center" colspan="3"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">1893 - Present<br />'+ '\n' +
			'</p></td>'+ '\n' +
		        '</tr>'+ '\n' +
		        '<tr>'+ '\n' +
			'<td bgcolor="#424949" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Normal Period<br />'+ '\n' +
			'</p></td>'+ '\n' +
			'<td bgcolor="#CCD1D1" style="vertical-align: middle" align="center" colspan="3"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">1981 - 2010<br />'+ '\n' +
			'</p></td>'+ '\n' +
		        '</tr>'+ '\n' +
                        '</tbody>'+ '\n' +
                        '</table>'+ '\n' +
                        '<p style="font-size: 12px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">' + '\n' +
                        '* Multiple years tied this record. Only the latest year is shown.</p>')
    # CMH
    snowyear_cmh.append('<tr>'+ '\n' +
			'<td bgcolor="#424949" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Period of Record<br />'+ '\n' +
			'</p></td>'+ '\n' +
			'<td bgcolor="#CCD1D1" style="vertical-align: middle" align="center" colspan="3"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">1884 - Present<br />'+ '\n' +
			'</p></td>'+ '\n' +
		        '</tr>'+ '\n' +
		        '<tr>'+ '\n' +
			'<td bgcolor="#424949" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Normal Period<br />'+ '\n' +
			'</p></td>'+ '\n' +
			'<td bgcolor="#CCD1D1" style="vertical-align: middle" align="center" colspan="3"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">1981 - 2010<br />'+ '\n' +
			'</p></td>'+ '\n' +
		        '</tr>'+ '\n' +
                        '</tbody>'+ '\n' +
                        '</table>'+ '\n' +
                        '<p style="font-size: 12px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">' + '\n' +
                        '* Multiple years tied this record. Only the latest year is shown.</p>')

    ### --- ###
    
### Step 3: Export file as .html ###
print(' Writing data to files... ')

# Open output files for writing #
# Monthly files
final_snowmonth_cvg = open(output_file_cvg_month,"w") # Open cvg file for writing
final_snowmonth_day = open(output_file_day_month,"w") # Open day file for writing
final_snowmonth_cmh = open(output_file_cmh_month,"w") # Open cmh file for writing

# Yearly files
final_snowyear_cvg = open(output_file_cvg_year,"w") # Open cvg file for writing
final_snowyear_day = open(output_file_day_year,"w") # Open day file for writing
final_snowyear_cmh = open(output_file_cmh_year,"w") # Open cmh file for writing
# - #

# Monthly
# For loop to write out files- CVG #
for j in range(len(snowmonth_cvg)):
	#print degree90_cvg[j]
	text_cvg = snowmonth_cvg[j]
	final_snowmonth_cvg.write(text_cvg)
# - #

# For loop to write out files- DAY #
for j in range(len(snowmonth_day)):
	text_day = snowmonth_day[j]
	final_snowmonth_day.write(text_day)
# - #

# For loop to write out files- CMH #
for j in range(len(snowmonth_cmh)):
	text_cmh = snowmonth_cmh[j]
	final_snowmonth_cmh.write(text_cmh)
# - #

# Yearly
# For loop to write out files- CVG #
for j in range(len(snowyear_cvg)):
	#print degree90_cvg[j]
	text_cvg = snowyear_cvg[j]
	final_snowyear_cvg.write(text_cvg)
# - #

# For loop to write out files- DAY #
for j in range(len(snowyear_day)):
	text_day = snowyear_day[j]
	final_snowyear_day.write(text_day)
# - #

# For loop to write out files- CMH #
for j in range(len(snowyear_cmh)):
	text_cmh = snowyear_cmh[j]
	final_snowyear_cmh.write(text_cmh)
# - #

### --- ###


### Step 4: Close all the open files and generate pdf files ###
# Monthly files
final_snowmonth_cvg.close()
final_snowmonth_day.close()
final_snowmonth_cmh.close()

# Yearly files
final_snowyear_cvg.close()
final_snowyear_day.close()
final_snowyear_cmh.close()

# Create monthly pdf files #
print(' Now creating monthly pdf files')
# CVG
pdfkit.from_file('X:/Users/ILN_Common/1-BrianandKristen/ClimateWebpage/PDFTxtFiles/SnowSum/SnowSumMonth_cvg.html', 'X:/Users/ILN_Common/1-BrianandKristen/ClimateWebpage/PDFTxtFiles/SnowSum/SnowSumMonth_cvg.pdf')
pdfkit.from_file('X:/Users/ILN_Common/1-BrianandKristen/ClimateWebpage/PDFTxtFiles/SnowSum/SnowSumMonth_cvg.html', 'X:/Apps/WinSCP/ldad_upload/data_ldad_public_nwswwas/cms_media+climo_webpage+SnowSumMonth_cvg.pdf')
# DAY
pdfkit.from_file('X:/Users/ILN_Common/1-BrianandKristen/ClimateWebpage/PDFTxtFiles/SnowSum/SnowSumMonth_day.html', 'X:/Users/ILN_Common/1-BrianandKristen/ClimateWebpage/PDFTxtFiles/SnowSum/SnowSumMonth_day.pdf')
pdfkit.from_file('X:/Users/ILN_Common/1-BrianandKristen/ClimateWebpage/PDFTxtFiles/SnowSum/SnowSumMonth_day.html', 'X:/Apps/WinSCP/ldad_upload/data_ldad_public_nwswwas/cms_media+climo_webpage+SnowSumMonth_day.pdf')
# CMH
pdfkit.from_file('X:/Users/ILN_Common/1-BrianandKristen/ClimateWebpage/PDFTxtFiles/SnowSum/SnowSumMonth_cmh.html', 'X:/Users/ILN_Common/1-BrianandKristen/ClimateWebpage/PDFTxtFiles/SnowSum/SnowSumMonth_cmh.pdf')
pdfkit.from_file('X:/Users/ILN_Common/1-BrianandKristen/ClimateWebpage/PDFTxtFiles/SnowSum/SnowSumMonth_cmh.html', 'X:/Apps/WinSCP/ldad_upload/data_ldad_public_nwswwas/cms_media+climo_webpage+SnowSumMonth_cmh.pdf')
# - #

print(' Now creating yearly pdf files')
# CVG
pdfkit.from_file('X:/Users/ILN_Common/1-BrianandKristen/ClimateWebpage/PDFTxtFiles/SnowSum/SnowSumYear_cvg.html', 'X:/Users/ILN_Common/1-BrianandKristen/ClimateWebpage/PDFTxtFiles/SnowSum/SnowSumYear_cvg.pdf')
pdfkit.from_file('X:/Users/ILN_Common/1-BrianandKristen/ClimateWebpage/PDFTxtFiles/SnowSum/SnowSumYear_cvg.html', 'X:/Apps/WinSCP/ldad_upload/data_ldad_public_nwswwas/cms_media+climo_webpage+SnowSumYear_cvg.pdf')
# DAY
pdfkit.from_file('X:/Users/ILN_Common/1-BrianandKristen/ClimateWebpage/PDFTxtFiles/SnowSum/SnowSumYear_day.html', 'X:/Users/ILN_Common/1-BrianandKristen/ClimateWebpage/PDFTxtFiles/SnowSum/SnowSumYear_day.pdf')
pdfkit.from_file('X:/Users/ILN_Common/1-BrianandKristen/ClimateWebpage/PDFTxtFiles/SnowSum/SnowSumYear_day.html', 'X:/Apps/WinSCP/ldad_upload/data_ldad_public_nwswwas/cms_media+climo_webpage+SnowSumYear_day.pdf')
# CMH
pdfkit.from_file('X:/Users/ILN_Common/1-BrianandKristen/ClimateWebpage/PDFTxtFiles/SnowSum/SnowSumYear_cmh.html', 'X:/Users/ILN_Common/1-BrianandKristen/ClimateWebpage/PDFTxtFiles/SnowSum/SnowSumYear_cmh.pdf')
pdfkit.from_file('X:/Users/ILN_Common/1-BrianandKristen/ClimateWebpage/PDFTxtFiles/SnowSum/SnowSumYear_cmh.html', 'X:/Apps/WinSCP/ldad_upload/data_ldad_public_nwswwas/cms_media+climo_webpage+SnowSumYear_cmh.pdf')
# - #

print(' Script completed and files genereated... ')

### --- ###
