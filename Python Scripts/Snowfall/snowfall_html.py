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
import urllib.request as urlL
import json
#######################################
#######################################
import datetime
import time
import numpy as np
import math
import mysql.connector
import pdfkit
#######################################
# Set Acis data server
base_url = "http://data.rcc-acis.org/"
sites = ["cak","cle","eri","mfd","tol","yng"]
#######################################
# Acis WebServices functions
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
# M A I N
###################################################
def htmlSite(site):
    ### Defined Constants ###
    degree_sign= u'\N{DEGREE SIGN}' # The symbol for degrees
    mydate = datetime.datetime.now()
    cm = mydate.strftime("%B") # Current month
    cy = mydate.strftime("%Y") # Current month
    current_date = (time.strftime("%Y-%m-%d")) # Current date
    star_needed_least = [] # Do I need a star besides that values to indicate multiple years with that value
    
    # mysql constants #
    cnx = mysql.connector.connect(user='austinrebello', password='mysql',
                                host='localhost',
                                database='climate') 
    cursor = cnx.cursor(buffered=True)
    # - #
    # - #
    
    ### --- ###

    
    ### Ouput files for html ###
    # Monthly Output files
    output_file_month = '../../PDFTxtFiles/Snowfall/SnowSumMonth_'+site+'.html' # Output file path

    # Yearly Output files
    output_file_year = '../../PDFTxtFiles/Snowfall/SnowSumYear_'+site+'.html' # Output file path
    ### --- ###
    
   
    ### Step 1: Obtain data from XMACIS/ mysql and format ###

    # Most snowfall in a month- #
    month_totals = []
    # Get most snowfall in a month 
    month_number = ('10', '11', '12', '01', '02', '03', '04', '05')
    for monum in range(len(month_number)):
        #print str(month_number[monum])
        query = ("SELECT year_"+site+", sum_"+site+" FROM climate.snow_"+site+" where month_"+site+" ='"+str(month_number[monum])+"' ORDER BY sum_"+site+"+0 DESC, year_"+site+" DESC;")
        #print query
        cursor.execute(query)
        row = cursor.fetchone()
        #print ( str(month_number[monum]) + str(row) )
        month_totals.append(str(month_number[monum]) + "," + str(row))
    # - #
    
    # Least snowfall in a month- #
    least_month_totals = []
    # Get most snowfall in a month 
    month_number = ('10', '11', '12', '01', '02', '03', '04', '05')
    for monum in range(len(month_number)):
        #print str(month_number[monum])
        query = ("SELECT year_"+site+", sum_"+site+" FROM climate.snow_"+site+" where month_"+site+" ='"+str(month_number[monum])+"' and sum_"+site+" !='M' ORDER BY sum_"+site+"+1, sum_"+site+" asc, year_"+site+" desc;")
        #print query
        cursor.execute(query)
        row = cursor.fetchmany(size=2)
        if row[0][1] == row[1][1]:
            star_needed_least.append(1)
        else:
            star_needed_least.append(0) 
        #print ( str(month_number[monum]) + str(row) )
        least_month_totals.append(str(month_number[monum]) + "," + str(row))
    # - #
    ### --- ###

    ### Parameters for data request ###
    # Earliest measurable snowfall-
    earliest_snow = {"sid":site+"thr","sdate":"1891-07-31","edate":"por","elems":[{"name":"snow","interval":[1,0,0],"duration":"std","season_start":"8-1","reduce":{"reduce":"first_ge_0.1","add":"value"},"smry":"min"}]};
    data_earliest_snow = GridData(earliest_snow) # Returned data from request
    date_earliest_snow = str(data_earliest_snow['smry'][0]) # Display year of earliest snow. Using dict key of smry. Keys are found data_earliest_snow.viewkeys() and meta, data, smry
    value1_earliest_snow = data_earliest_snow['data'][(int(str(data_earliest_snow['smry'][0])[0:4])+1)-1891] # Take the year of the earliest snow then subtract from sdate and add 1 year back
    value_earliest_snow = str(value1_earliest_snow[1][1])
    # - #

    # Latest First measurable snowfall-
    latest_earliest_snow = {"sid":site+"thr","sdate":"1891-07-31","edate":"por","elems":[{"name":"snow","interval":[1,0,0],"duration":"std","season_start":"8-1","reduce":{"reduce":"first_ge_0.1","add":"value"},"smry":"max","maxmissing":1}]};
    data_latest_earliest_snow = GridData(latest_earliest_snow) # Returned data from request
    date_latest_earliest_snow = str(data_latest_earliest_snow['smry'][0]) # Display year of latest_earliest snow. Using dict key of smry. Keys are found data_latest_earliest_snow.viewkeys() and meta, data, smry
    value1_latest_earliest_snow = data_latest_earliest_snow['data'][(int(str(data_latest_earliest_snow['smry'][0])[0:4]))-1891] # Take the year of the latest_earliest snow then subtract from sdate and add 1 year back
    value_latest_earliest_snow = str(value1_latest_earliest_snow[1][1])
    # - #

    # Normal First measurable snowfall-
    normal_first_snow = {"sid":site+"thr","sdate":"1981-07-31","edate":"2010-07-31","elems":[{"name":"snow","interval":[1,0,0],"duration":"std","season_start":"8-1","reduce":{"reduce":"first_ge_0.1","add":"value"},"smry":"mean"}]};
    data_normal_first_snow = GridData(normal_first_snow) # Returned data from request
    date_normal_first_snow = str(data_normal_first_snow['smry'][0]) # Display year of latest_earliest snow. Using dict key of smry. Keys are found data_latest_earliest_snow.viewkeys() and meta, data, smry
    # - #

    # Normal First 1" snowfall-
    normal_firstmeasure_snow = {"sid":site+"thr","sdate":"1981-07-31","edate":"2010-07-31","elems":[{"name":"snow","interval":[1,0,0],"duration":"std","season_start":"8-1","reduce":{"reduce":"first_ge_1.0","add":"value"},"smry":"mean"}]};
    data_normal_firstmeasure_snow = GridData(normal_firstmeasure_snow) # Returned data from request
    date_normal_firstmeasure_snow = str(data_normal_firstmeasure_snow['smry'][0]) # Display year of latest_earliest snow. Using dict key of smry. Keys are found data_latest_earliest_snow.viewkeys() and meta, data, smry
    # - #

    # Latest Seasonal Measurable Snow-
    latest_snow = {"sid":site+"thr","sdate":"1891-07-31","edate":"por","elems":[{"name":"snow","interval":[1,0,0],"duration":"std","season_start":"8-1","reduce":{"reduce":"last_ge_0.1","add":"value"},"smry":"max","maxmissing":1}]};
    data_latest_snow = GridData(latest_snow) # Returned data from request
    date_latest_snow = str(data_latest_snow['smry'][0]) # Display year of earliest snow. Using dict key of smry. Keys are found data_earliest_snow.viewkeys() and meta, data, smry
    value1_latest_snow = data_latest_snow['data'][(int(str(data_latest_snow['smry'][0])[0:4]))-1891] # Take the year of the earliest snow then subtract from sdate and add 1 year back
    value_latest_snow = str(value1_latest_snow[1][1])
    # - #

    # Latest Seasonal 1" Snow-
    latestone_snow = {"sid":site+"thr","sdate":"1891-07-31","edate":"por","elems":[{"name":"snow","interval":[1,0,0],"duration":"std","season_start":"8-1","reduce":{"reduce":"last_ge_1.0","add":"value"},"smry":"max","maxmissing":1}]};
    data_latestone_snow = GridData(latestone_snow) # Returned data from request
    date_latestone_snow = str(data_latestone_snow['smry'][0]) # Display year of earliest snow. Using dict key of smry. Keys are found data_earliest_snow.viewkeys() and meta, data, smry
    value1_latestone_snow = data_latestone_snow['data'][(int(str(data_latestone_snow['smry'][0])[0:4]))-1891] # Take the year of the earliest snow then subtract from sdate and add 1 year back
    value_latestone_snow = str(value1_latestone_snow[1][1])
    # - #

    # Earliest Last Seasonal Measurable Snow-
    earliestlatest_snow = {"sid":site+"thr","sdate":"1891-07-31","edate":"por","elems":[{"name":"snow","interval":[1,0,0],"duration":"std","season_start":"8-1","reduce":{"reduce":"last_ge_0.1","add":"value"},"smry":"min","maxmissing":1}]};
    data_earliestlatest_snow = GridData(earliestlatest_snow) # Returned data from request
    date_earliestlatest_snow = str(data_earliestlatest_snow['smry'][0]) # Display year of earliest snow. Using dict key of smry. Keys are found data_earliest_snow.viewkeys() and meta, data, smry
    value1_earliestlatest_snow = data_earliestlatest_snow['data'][(int(str(data_earliestlatest_snow['smry'][0])[0:4]))-1891] # Take the year of the earliest snow then subtract from sdate and add 1 year back
    value_earliestlatest_snow = str(value1_earliestlatest_snow[1][1])
    # - #
    
    # Most in a calendar year-
    most_calendaryear_snow = {"sid":site+"thr","sdate":"por","edate":"por","elems":[{"name":"snow","interval":"yly","duration":"yly","reduce":"sum","smry":{"reduce":"max","add":"date"}}]};
    data_most_calendaryear_snow = GridData(most_calendaryear_snow) # Returned data from request
    date_most_snow = str(data_most_calendaryear_snow['smry'][0][1]) # Display year of earliest snow. Using dict key of smry. Keys are found data_earliest_snow.viewkeys() and meta, data, smry
    value_most_snow = str(data_most_calendaryear_snow['smry'][0][0]) # Take the year of the earliest snow then subtract from sdate and add 1 year back
    # - #
    
    # Least in a calendar year-
    least_calendaryear_snow = {"sid":site+"thr","sdate":"por","edate":str(int(cy)-1),"elems":[{"name":"snow","interval":"yly","duration":"yly","reduce":"sum","smry":{"reduce":"min","add":"date"},"maxmissing":1}]};
    data_least_calendaryear_snow = GridData(least_calendaryear_snow) # Returned data from request
    date_least_snow = str(data_least_calendaryear_snow['smry'][0][1]) # Display year of earliest snow. Using dict key of smry. Keys are found data_earliest_snow.viewkeys() and meta, data, smry
    value_least_snow = str(data_least_calendaryear_snow['smry'][0][0]) # Take the year of the earliest snow then subtract from sdate and add 1 year back
    # - #

    # Most in a season-
    most_seasonyear_snow = {"sid":site+"thr","sdate":"1891-07-31","edate":"por","elems":[{"name":"snow","interval":[1,0,0],"duration":"std","season_start":"8-1","reduce":{"reduce":"sum","add":"date"},"smry":{"reduce":"max","add":"date"}}]};
    data_most_seasonyear_snow = GridData(most_seasonyear_snow) # Returned data from request
    date_most_seasonyear_snow = str(data_most_seasonyear_snow['smry'][0][1]) # Display year of earliest snow. Using dict key of smry. Keys are found data_earliest_snow.viewkeys() and meta, data, smry
    value_most_seasonyear_snow = str(data_most_seasonyear_snow['smry'][0][0]) # Take the year of the earliest snow then subtract from sdate and add 1 year back
    # - #

    # Least in a season-
    least_seasonyear_snow = {"sid":site+"thr","sdate":"1891-07-31","edate":"por","elems":[{"name":"snow","interval":[1,0,0],"duration":"std","season_start":"8-1","reduce":{"reduce":"sum","add":"date"},"smry":{"reduce":"min","add":"date"},"maxmissing":1}]};
    data_least_seasonyear_snow = GridData(least_seasonyear_snow) # Returned data from request
    date_least_seasonyear_snow = str(data_least_seasonyear_snow['smry'][0][1]) # Display year of earliest snow. Using dict key of smry. Keys are found data_earliest_snow.viewkeys() and meta, data, smry
    value_least_seasonyear_snow = str(data_least_seasonyear_snow['smry'][0][0]) # Take the year of the earliest snow then subtract from sdate and add 1 year back
    # - #

    # Most days with daily snowfall >1" in a season-
    most_daysone_snow = {"sid":site+"thr","sdate":"1891-07-31","edate":"por","elems":[{"name":"snow","interval":[1,0,0],"duration":"std","season_start":"8-1","reduce":"cnt_ge_1.0","smry":{"reduce":"max","add":"date"}}]};
    data_most_daysone_snow = GridData(most_daysone_snow)
    date_most_daysone_snow = str(data_most_daysone_snow['smry'][0][1])
    value_most_daysone_snow = str(data_most_daysone_snow['smry'][0][0])
    # - #

    # Most days with measurable snowfall in a season-
    most_daystrace_snow = {"sid":site+"thr","sdate":"1891-07-31","edate":"por","elems":[{"name":"snow","interval":[1,0,0],"duration":"std","season_start":"8-1","reduce":"cnt_gt_0","smry":{"reduce":"max","add":"date"}}]};
    data_most_daystrace_snow = GridData(most_daystrace_snow)
    date_most_daystrace_snow = str(data_most_daystrace_snow['smry'][0][1])
    value_most_daystrace_snow = str(data_most_daystrace_snow['smry'][0][0])
    # - #

    # Most snowfall in 1 day-
    most_daily_snow = {"sid":site+"thr","sdate":"por","edate":"por","elems":[{"name":"snow","interval":"dly","duration":"dly","smry":{"reduce":"max","add":"date"},"smry_only":1}]}
    data_most_daily_snow = GridData(most_daily_snow)
    date_most_daily_snow = str(data_most_daily_snow['smry'][0][1])
    value_most_daily_snow = str(data_most_daily_snow['smry'][0][0])
    # - #

    # Most snowfall in 2 days-
    most_twodaily_snow = {"sid":site+"thr","sdate":"por","edate":"por","elems":[{"name":"snow","interval":"dly","duration":2,"reduce":"sum","smry":{"reduce":"max","add":"date"},"smry_only":1}]}
    data_most_twodaily_snow = GridData(most_twodaily_snow)
    date_most_twodaily_snow = str(data_most_twodaily_snow['smry'][0][1])
    value_most_twodaily_snow = str(data_most_twodaily_snow['smry'][0][0])

    # Longest stretch of measurable snowfall-
    longest_measure_snow = {"sid":site+"thr","sdate":"1891-6-30","edate":"2017-6-30","elems":[{"name":"snow","interval":[1,0,0],"duration":"std","season_start":"7-1","reduce":{"reduce":"run_ge_0.1","add":"date"}}]}
    data_longest_measure_snow = GridData(longest_measure_snow)
    splitline = str(data_longest_measure_snow).split(",")
    counter = 0
    totalcount = 0
    index = 0
    dtype = [('date','S10'),('count',int)]
    values = []
    final_data_longest_measure_snow = []
    for line in splitline:
        new = line.strip(" ' /n /t [ ] /u }")
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
    measure_snow = np.sort(np.array(values,dtype),order='count')[::-1]
    final_data_longest_measure_snow.append((measure_snow[0][0],measure_snow[0][1]))
    for j in range(len(measure_snow)):
        if measure_snow[j][1] == measure_snow[j+1][1]:
            final_data_longest_measure_snow.append((measure_snow[j+1][0],measure_snow[j+1][1]))
        else:
            break
    ### --- ###

    ### Step 2: Snowfall climate information list setup- includes needed html for formatting ###
    # List setup - Month #
    snowmonth = [] # Initialize list
    # - #

    # List setup - Year #
    snowyear = [] # Initialize list
    # - #

    # Header/ MISC Info #
    snowmonth.append('<table align="center" border="0" cellpadding="1" cellspacing="1" style="width: 750px;">'+ '\n' +
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
    snowyear.append('<table align="center" border="0" cellpadding="1" cellspacing="1" style="width: 750px;">'+ '\n' +
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
    month_totals_oct = str(month_totals[0])
    month_totals_octyr_final = month_totals_oct[4:11].strip(" ( , ' ")
    month_totals_octnum_final = month_totals_oct[12:21].strip(" , ( u ' ) ")
    snowmonth.append('<tr>'+ '\n' +
                        '<td bgcolor="#1F618D" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Most in October<br />'+ '\n' +
                	'</p></td>'+ '\n' +
                    	'<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowmonth.append(month_totals_octyr_final)
    snowmonth.append('<br />'+'</p></td>'+ '<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="2"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowmonth.append(month_totals_octnum_final + '"')
    snowmonth.append('<br />'+ '\n' +
                        '</p></td>'+ '\n' +
                        '</tr>'+ '\n')
    # - #

    # Least in Oct
    least_month_totals_oct = str(least_month_totals[0])
    least_month_totals_octyr_final = least_month_totals_oct[4:11].strip(" ( , ' ")
    least_month_totals_octnum_final = least_month_totals_oct[12:21].strip(" , ( u ' ) ")
    snowmonth.append('<tr>'+ '\n' +
                        '<td bgcolor="#1F618D" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Least in October<br />'+ '\n' +                	'</p></td>'+ '\n' +
                    	'<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowmonth.append(least_month_totals_octyr_final)
    snowmonth.append('<br />'+'</p></td>'+ '<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="2"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowmonth.append(least_month_totals_octnum_final)
    if (least_month_totals_octnum_final != 'T'):
        snowmonth.append('"')
    if star_needed_least[0] == 1:
        snowmonth.append(' *')
    snowmonth.append('<br />'+ '\n' +
                        '</p></td>'+ '\n' +
                        '</tr>'+ '\n')
    # - #

    # Most in Nov
    month_totals_nov = str(month_totals[1])
    month_totals_novyr_final = month_totals_nov[4:11].strip(" ( , ' ")
    month_totals_novnum_final = month_totals_nov[12:21].strip(" , ( u ' ) ")
    snowmonth.append('<tr>'+ '\n' +
                        '<td bgcolor="#1F618D" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Most in November<br />'+ '\n' +
                	'</p></td>'+ '\n' +
                    	'<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowmonth.append(month_totals_novyr_final)
    snowmonth.append('<br />'+'</p></td>'+ '<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="2"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowmonth.append(month_totals_novnum_final + '"')
    snowmonth.append('<br />'+ '\n' +
                        '</p></td>'+ '\n' +
                        '</tr>'+ '\n')
    # - #

    # Least in Nov
    least_month_totals_nov = str(least_month_totals[1])
    least_month_totals_novyr_final = least_month_totals_nov[4:11].strip(" ( , ' ")
    least_month_totals_novnum_final = least_month_totals_nov[12:21].strip(" , ( u ' ) ")
    snowmonth.append('<tr>'+ '\n' +
                        '<td bgcolor="#1F618D" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Least in November<br />'+ '\n' +                	'</p></td>'+ '\n' +
                    	'<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowmonth.append(least_month_totals_novyr_final)
    snowmonth.append('<br />'+'</p></td>'+ '<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="2"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowmonth.append(least_month_totals_novnum_final)
    if (least_month_totals_novnum_final != 'T'):
        snowmonth.append('"')
    if star_needed_least[1] == 1:
        snowmonth.append(' *')
    snowmonth.append('<br />'+ '\n' +
                        '</p></td>'+ '\n' +
                        '</tr>'+ '\n')
    # - #
    
    # Most in Dec
    month_totals_dec = str(month_totals[2])
    month_totals_decyr_final = month_totals_dec[4:11].strip(" ( , ' ")
    month_totals_decnum_final = month_totals_dec[12:21].strip(" , ( u ' ) ")
    snowmonth.append('<tr>'+ '\n' +
                        '<td bgcolor="#1F618D" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Most in December<br />'+ '\n' +
                	'</p></td>'+ '\n' +
                    	'<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowmonth.append(month_totals_decyr_final)
    snowmonth.append('<br />'+'</p></td>'+ '<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="2"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowmonth.append(month_totals_decnum_final + '"')
    snowmonth.append('<br />'+ '\n' +
                        '</p></td>'+ '\n' +
                        '</tr>'+ '\n')
    # - #

    # Least in Dec
    least_month_totals_dec = str(least_month_totals[2])
    least_month_totals_decyr_final = least_month_totals_dec[4:11].strip(" ( , ' ")
    least_month_totals_decnum_final = least_month_totals_dec[12:21].strip(" , ( u ' ) ")
    snowmonth.append('<tr>'+ '\n' +
                        '<td bgcolor="#1F618D" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Least in December<br />'+ '\n' +                	'</p></td>'+ '\n' +
                    	'<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowmonth.append(least_month_totals_decyr_final)
    snowmonth.append('<br />'+'</p></td>'+ '<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="2"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowmonth.append(least_month_totals_decnum_final)
    if (least_month_totals_decnum_final != 'T'):
        snowmonth.append('"')
    if star_needed_least[2] == 1:
        snowmonth.append(' *')
    snowmonth.append('<br />'+ '\n' +
                        '</p></td>'+ '\n' +
                        '</tr>'+ '\n')
    # - #

    # Most in Jan
    month_totals_jan = str(month_totals[3])
    month_totals_janyr_final = month_totals_jan[4:11].strip(" ( , ' ")
    month_totals_jannum_final = month_totals_jan[12:21].strip(" , ( u ' ) ")
    snowmonth.append('<tr>'+ '\n' +
                        '<td bgcolor="#1F618D" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Most in January<br />'+ '\n' +
                	'</p></td>'+ '\n' +
                    	'<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowmonth.append(month_totals_janyr_final)
    snowmonth.append('<br />'+'</p></td>'+ '<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="2"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowmonth.append(month_totals_jannum_final + '"')
    snowmonth.append('<br />'+ '\n' +
                        '</p></td>'+ '\n' +
                        '</tr>'+ '\n')
    # - #

    # Least in Jan
    least_month_totals_jan = str(least_month_totals[3])
    least_month_totals_janyr_final = least_month_totals_jan[4:11].strip(" ( , ' ")
    least_month_totals_jannum_final = least_month_totals_jan[12:21].strip(" , ( u ' ) ")
    snowmonth.append('<tr>'+ '\n' +
                        '<td bgcolor="#1F618D" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Least in January<br />'+ '\n' +                	'</p></td>'+ '\n' +
                    	'<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowmonth.append(least_month_totals_janyr_final)
    snowmonth.append('<br />'+'</p></td>'+ '<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="2"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowmonth.append(least_month_totals_jannum_final)
    if (least_month_totals_jannum_final != 'T'):
        snowmonth.append('"')
    if star_needed_least[3] == 1:
        snowmonth.append(' *')
    snowmonth.append('<br />'+ '\n' +
                        '</p></td>'+ '\n' +
                        '</tr>'+ '\n')
    # - #

    # Most in Feb
    month_totals_feb = str(month_totals[4])
    month_totals_febyr_final = month_totals_feb[4:11].strip(" ( , ' ")
    month_totals_febnum_final = month_totals_feb[12:21].strip(" , ( u ' ) ")
    snowmonth.append('<tr>'+ '\n' +
                        '<td bgcolor="#1F618D" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Most in February<br />'+ '\n' +
                	'</p></td>'+ '\n' +
                    	'<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowmonth.append(month_totals_febyr_final)
    snowmonth.append('<br />'+'</p></td>'+ '<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="2"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowmonth.append(month_totals_febnum_final + '"')
    snowmonth.append('<br />'+ '\n' +
                        '</p></td>'+ '\n' +
                        '</tr>'+ '\n')
    # - #

    # Least in Feb
    least_month_totals_feb = str(least_month_totals[4])
    least_month_totals_febyr_final = least_month_totals_feb[4:11].strip(" ( , ' ")
    least_month_totals_febnum_final = least_month_totals_feb[12:21].strip(" , ( u ' ) ")
    snowmonth.append('<tr>'+ '\n' +
                        '<td bgcolor="#1F618D" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Least in February<br />'+ '\n' +                	'</p></td>'+ '\n' +
                    	'<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowmonth.append(least_month_totals_febyr_final)
    snowmonth.append('<br />'+'</p></td>'+ '<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="2"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowmonth.append(least_month_totals_febnum_final)
    if (least_month_totals_febnum_final != 'T'):
        snowmonth.append('"')
    if star_needed_least[4] == 1:
        snowmonth.append(' *')
    snowmonth.append('<br />'+ '\n' +
                        '</p></td>'+ '\n' +
                        '</tr>'+ '\n')
    # - #

    # Most in Mar
    month_totals_mar = str(month_totals[5])
    month_totals_maryr_final = month_totals_mar[4:11].strip(" ( , ' ")
    month_totals_marnum_final = month_totals_mar[12:21].strip(" , ( u ' ) ")
    snowmonth.append('<tr>'+ '\n' +
                        '<td bgcolor="#1F618D" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Most in March<br />'+ '\n' +
                	'</p></td>'+ '\n' +
                    	'<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowmonth.append(month_totals_maryr_final)
    snowmonth.append('<br />'+'</p></td>'+ '<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="2"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowmonth.append(month_totals_marnum_final + '"')
    snowmonth.append('<br />'+ '\n' +
                        '</p></td>'+ '\n' +
                        '</tr>'+ '\n')
    # - #

    # Least in Mar
    least_month_totals_mar = str(least_month_totals[5])
    least_month_totals_maryr_final = least_month_totals_mar[4:11].strip(" ( , ' ")
    least_month_totals_marnum_final = least_month_totals_mar[12:21].strip(" , ( u ' ) ")
    snowmonth.append('<tr>'+ '\n' +
                        '<td bgcolor="#1F618D" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Least in March<br />'+ '\n' +                	'</p></td>'+ '\n' +
                    	'<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowmonth.append(least_month_totals_maryr_final)
    snowmonth.append('<br />'+'</p></td>'+ '<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="2"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowmonth.append(least_month_totals_marnum_final)
    if (least_month_totals_marnum_final != 'T'):
        snowmonth.append('"')
    if star_needed_least[5] == 1:
        snowmonth.append(' *')
    snowmonth.append('<br />'+ '\n' +
                        '</p></td>'+ '\n' +
                        '</tr>'+ '\n')
    # - #

    # Most in Apr
    month_totals_apr = str(month_totals[6])
    month_totals_apryr_final = month_totals_apr[4:11].strip(" ( , ' ")
    month_totals_aprnum_final = month_totals_apr[12:21].strip(" , ( u ' ) ")
    snowmonth.append('<tr>'+ '\n' +
                        '<td bgcolor="#1F618D" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Most in April<br />'+ '\n' +
                	'</p></td>'+ '\n' +
                    	'<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowmonth.append(month_totals_apryr_final)
    snowmonth.append('<br />'+'</p></td>'+ '<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="2"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowmonth.append(month_totals_aprnum_final + '"')
    snowmonth.append('<br />'+ '\n' +
                        '</p></td>'+ '\n' +
                        '</tr>'+ '\n')
    # - #

    # Least in April
    least_month_totals_apr = str(least_month_totals[6])
    least_month_totals_apryr_final = least_month_totals_apr[4:11].strip(" ( , ' ")
    least_month_totals_aprnum_final = least_month_totals_apr[12:21].strip(" , ( u ' ) ")
    snowmonth.append('<tr>'+ '\n' +
                        '<td bgcolor="#1F618D" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Least in April<br />'+ '\n' +                	'</p></td>'+ '\n' +
                    	'<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowmonth.append(least_month_totals_apryr_final)
    snowmonth.append('<br />'+'</p></td>'+ '<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="2"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowmonth.append(least_month_totals_aprnum_final)
    if (least_month_totals_aprnum_final != 'T'):
        snowmonth.append('"')
    if star_needed_least[6] == 1:
        snowmonth.append(' *')
    snowmonth.append('<br />'+ '\n' +
                        '</p></td>'+ '\n' +
                        '</tr>'+ '\n')
    # END SNOW MONTH #

    # Snow Year #
    # Earliest Seasonal Measurable Snow-
    snowyear.append('<tr>' + '\n' +
                        '<td bgcolor="#1F618D" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Earliest Seasonal Measurable Snow<br />' + '\n' +
                        '</p></td>' + '\n' +
                        '<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowyear.append(value_earliest_snow)
    snowyear.append('" <br />' + '\n')
    snowyear.append('</p></td>' + '\n' +
                        '<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowyear.append(date_earliest_snow)
    snowyear.append('<br />' + '\n' +
                        '</p></td>' + '\n' +
                        '</tr>' + '\n')
    
    # Latest First Seasonal Measurable Snow-
    snowyear.append('<tr>' + '\n' +
                        '<td bgcolor="#1F618D" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Latest Seasonal First Measurable Snow<br />' + '\n' +
                        '</p></td>' + '\n' +
                        '<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowyear.append(value_latest_earliest_snow)
    snowyear.append('" <br />' + '\n')
    snowyear.append('</p></td>' + '\n' +
                        '<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowyear.append(date_latest_earliest_snow)
    snowyear.append('<br />' + '\n' +
                        '</p></td>' + '\n' +
                        '</tr>' + '\n')

    # Normal First Seasonal Measurable Snow-
    snowyear.append('<tr>' + '\n' +
                        '<td bgcolor="#1F618D" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Normal First Measurable Snow (1981-2010)<br />' + '\n' +
                        '</p></td>' + '\n' +
                        '<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="2"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowyear.append(date_normal_first_snow)
    snowyear.append('<br />' + '\n')
    snowyear.append('</p></td>' + '\n')
    snowyear.append('</tr>' + '\n')

    # Normal First Seasonal 1" Snow-
    snowyear.append('<tr>' + '\n' +
                        '<td bgcolor="#1F618D" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Normal First Snow Of At Least 1"(1981-2010)<br />' + '\n' +
                        '</p></td>' + '\n' +
                        '<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="2"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowyear.append(date_normal_firstmeasure_snow)
    snowyear.append('<br />' + '\n')
    snowyear.append('</p></td>' + '\n')
    snowyear.append('</tr>' + '\n')

    # Latest Seasonal Measurable Snow-
    snowyear.append('<tr>' + '\n' +
                        '<td bgcolor="#1F618D" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Latest Seasonal Measurable Snow<br />' + '\n' +
                        '</p></td>' + '\n' +
                        '<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowyear.append(value_latest_snow)
    snowyear.append('" <br />' + '\n')
    snowyear.append('</p></td>' + '\n' +
                        '<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowyear.append(date_latest_snow)
    snowyear.append('<br />' + '\n' +
                        '</p></td>' + '\n' +
                        '</tr>' + '\n')

    # Latest Seasonal 1" Snow-
    snowyear.append('<tr>' + '\n' +
                        '<td bgcolor="#1F618D" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Latest Seasonal Snow Of At Least 1"<br />' + '\n' +
                        '</p></td>' + '\n' +
                        '<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowyear.append(value_latestone_snow)
    snowyear.append('" <br />' + '\n')
    snowyear.append('</p></td>' + '\n' +
                        '<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowyear.append(date_latestone_snow)
    snowyear.append('<br />' + '\n' +
                        '</p></td>' + '\n' +
                        '</tr>' + '\n')

    # Earliest Last Seasonal Measurable Snow-
    snowyear.append('<tr>' + '\n' +
                        '<td bgcolor="#1F618D" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Earliest Last Seasonal Measurable Snow<br />' + '\n' +
                        '</p></td>' + '\n' +
                        '<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowyear.append(value_earliestlatest_snow)
    snowyear.append('" <br />' + '\n')
    snowyear.append('</p></td>' + '\n' +
                        '<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowyear.append(date_earliestlatest_snow)
    snowyear.append('<br />' + '\n' +
                        '</p></td>' + '\n' +
                        '</tr>' + '\n')

    # Most Snow in a Calendar Year-
    snowyear.append('<tr>' + '\n' +
                        '<td bgcolor="#884EA0" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Most In A Calendar Year<br />' + '\n' +
                        '</p></td>' + '\n' +
                        '<td bgcolor="#C39BD3" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowyear.append(value_most_snow)
    snowyear.append('" <br />' + '\n')
    snowyear.append('</p></td>' + '\n' +
                        '<td bgcolor="#C39BD3" style="vertical-align: middle" align="center" colspan="2"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowyear.append(date_most_snow[0:4])
    snowyear.append('<br />' + '\n' +
                        '</p></td>' + '\n' +
                        '</tr>' + '\n')

    # Least Snow in a Calendar Year-
    snowyear.append('<tr>' + '\n' +
                        '<td bgcolor="#884EA0" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Least In A Calendar Year<br />' + '\n' +
                        '</p></td>' + '\n' +
                        '<td bgcolor="#C39BD3" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowyear.append(value_least_snow)
    snowyear.append('" <br />' + '\n')
    snowyear.append('</p></td>' + '\n' +
                        '<td bgcolor="#C39BD3" style="vertical-align: middle" align="center" colspan="2"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowyear.append(date_least_snow[0:4])
    snowyear.append('<br />' + '\n' +
                        '</p></td>' + '\n' +
                        '</tr>' + '\n')

    # Most Snow in a Season Year-
    snowyear.append('<tr>' + '\n' +
                        '<td bgcolor="#884EA0" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Most in a Season<br />' + '\n' +
                        '</p></td>' + '\n' +
                        '<td bgcolor="#C39BD3" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowyear.append(value_most_seasonyear_snow)
    snowyear.append('" <br />' + '\n')
    snowyear.append('</p></td>' + '\n' +
                        '<td bgcolor="#C39BD3" style="vertical-align: middle" align="center" colspan="2"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowyear.append(date_most_seasonyear_snow[0:4])
    snowyear.append('<br />' + '\n' +
                        '</p></td>' + '\n' +
                        '</tr>' + '\n')

    # Least Snow in a Season Year-
    snowyear.append('<tr>' + '\n' +
                        '<td bgcolor="#884EA0" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Least in a Season<br />' + '\n' +
                        '</p></td>' + '\n' +
                        '<td bgcolor="#C39BD3" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowyear.append(value_least_seasonyear_snow)
    snowyear.append('" <br />' + '\n')
    snowyear.append('</p></td>' + '\n' +
                        '<td bgcolor="#C39BD3" style="vertical-align: middle" align="center" colspan="2"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowyear.append(date_least_seasonyear_snow[0:4])
    snowyear.append('<br />' + '\n' +
                        '</p></td>' + '\n' +
                        '</tr>' + '\n')

    # Most Days with daily snowfall >1" in a season-
    snowyear.append('<tr>' + '\n' +
                        '<td bgcolor="#1F618D" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Most Days With Daily Snowfall >=1" In A Season<br />' + '\n' +
                        '</p></td>' + '\n' +
                        '<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowyear.append(value_most_daysone_snow)
    snowyear.append('<br />' + '\n')
    snowyear.append('</p></td>' + '\n' +
                        '<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowyear.append(str(int(date_most_daysone_snow[0:4])-1) + "-" + date_most_daysone_snow[0:4])
    snowyear.append('<br />' + '\n' +
                        '</p></td>' + '\n' +
                        '</tr>' + '\n')

    # Most days with measurable snowfall in a season-
    snowyear.append('<tr>' + '\n' +
                        '<td bgcolor="#1F618D" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Most Days With Measurable Snowfall In A Season<br />' + '\n' +
                        '</p></td>' + '\n' +
                        '<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowyear.append(value_most_daystrace_snow)
    snowyear.append('<br />' + '\n')
    snowyear.append('</p></td>' + '\n' +
                        '<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowyear.append(str(int(date_most_daystrace_snow[0:4])-1) + "-" + date_most_daystrace_snow[0:4])
    snowyear.append('<br />' + '\n' +
                        '</p></td>' + '\n' +
                        '</tr>' + '\n')

    # Highest recorded daily snowfall
    snowyear.append('<tr>' + '\n' +
                        '<td bgcolor="#1F618D" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Most In 1 Day<br />' + '\n' +
                        '</p></td>' + '\n' +
                        '<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowyear.append(value_most_daily_snow)
    snowyear.append('" <br />' + '\n')
    snowyear.append('</p></td>' + '\n' +
                        '<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowyear.append(date_most_daily_snow)
    snowyear.append('<br />' + '\n' +
                        '</p></td>' + '\n' +
                        '</tr>' + '\n')

    # Highest two day snowfall
    snowyear.append('<tr>' + '\n' +
                        '<td bgcolor="#1F618D" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Most In 2 Consective Days (2nd Day Shown)<br />' + '\n' +
                        '</p></td>' + '\n' +
                        '<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowyear.append(value_most_twodaily_snow)
    snowyear.append('" <br />' + '\n')
    snowyear.append('</p></td>' + '\n' +
                        '<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    snowyear.append(date_most_twodaily_snow)
    snowyear.append('<br />' + '\n' +
                        '</p></td>' + '\n' +
                        '</tr>' + '\n')

    # Longest Stretch of Measurable Snowfall
    for j in range(len(final_data_longest_measure_snow)):
        snowyear.append('<tr>'+ '\n')
        if j == 0:
            if (len(final_data_longest_measure_snow)) > 1:
                snowyear.append('<td bgcolor="#1F618D" style="vertical-align: middle" align="center" rowspan="' + str(len(final_data_longest_measure_snow)) + '" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Longest Stretch of Measurable Snowfall (End Date)<br />'+ '\n' +
                                    '</p></td>'+ '\n')
            else:
                snowyear.append('<td bgcolor="#1F618D" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Longest Stretch (End Date)<br />'+ '\n' +
                                    '</p></td>'+ '\n')
            snowyear.append('<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
            snowyear.append((final_data_longest_measure_snow[j][0]).decode("utf-8"))
            snowyear.append('<br />'+ '\n' +
                                '</p></td>'+ '\n' +
                                '<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="2"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
            snowyear.append(str(final_data_longest_measure_snow[j][1]))
            snowyear.append('<br />'+ '\n'
                                '</p></td>'+ '\n')	
        if j > 0:
            snowyear.append('<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
            snowyear.append(str(final_data_longest_measure_snow[j][0]))
            snowyear.append('<br />'+ '\n' +
                                '</p></td>'+ '\n' +
                                '<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="2"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
            snowyear.append(str(final_data_longest_measure_snow[j][1]))
            snowyear.append('<br />'+ '\n'
                                '</p></td>'+ '\n')			
    snowyear.append('</tr>'+ '\n')

    # END SNOW YEAR #

    # Add other static text (period of record/ normal)
    snowmonth.append('<tr>'+ '\n' +
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

    snowyear.append('<tr>'+ '\n' +
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

        
    ### Step 3: Export file as .html ###
    print(' Writing data to files... ')

    # Open output files for writing #
    # Monthly files
    final_snowmonth = open(output_file_month,"w+") # Open file for writing

    # Yearly files
    final_snowyear = open(output_file_year,"w+") # Open file for writing
    # - #

    # Monthly
    # For loop to write out files- #
    for j in range(len(snowmonth)):
        #print degree90[j]
        text = snowmonth[j]
        final_snowmonth.write(text)
    # - #

    # Yearly
    # For loop to write out files- #
    for j in range(len(snowyear)):
        #print degree90[j]
        text = snowyear[j]
        final_snowyear.write(text)
    # - #

    ### --- ###
    ### Step 4: Close all the open files and generate pdf files ###
    # Monthly files
    final_snowmonth.close()

    # Yearly files
    final_snowyear.close()

    # Create monthly pdf files #
    print(' Now creating monthly pdf files')
    pdfkit.from_file('../../PDFTxtFiles/Snowfall/SnowSumMonth_'+site+'.html', '../../PDFTxtFiles/Snowfall/SnowSumYear_'+site+'.pdf')
  
    print(' Now creating yearly pdf files')
    pdfkit.from_file('../../PDFTxtFiles/Snowfall/SnowSumYear_'+site+'.html', '../../PDFTxtFiles/Snowfall/SnowSumYear_'+site+'.pdf')

    print(' Script completed and files genereated... ')

    ### --- ###
    # Close Connection
    cursor.close()
    cnx.close()



for site in sites:
    htmlSite(site)