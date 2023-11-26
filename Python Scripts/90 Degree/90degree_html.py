# Name: Brian Haines
# Date: 11/24/16
# Purpose: Create a script that requests 90 degree information
# Version/ update history:
#    1) 11-24-16: Initial attempt to file
#    2) 12-22-16: Finished skelton of code. Outputs data for each site without html
#                 formatting
#    3) 1-13-17: Finished editing code with files being outputted to O drive
#    4) 1-21-17: Updated output directory and changed normal in a year to float (allow decimals)

#######################################
# Import modules required by Acis
import urllib.request as urlL
import json
import re
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
    degree_sign= u'\N{DEGREE SIGN}' # The symbol for degrees
    mydate = datetime.datetime.now()
    cm = mydate.strftime("%B") # Current month
    cy = mydate.strftime("%Y") # Current month
    current_date = (time.strftime("%Y-%m-%d")) # Current date
    
    # mysql constants #
    cnx = mysql.connector.connect(user='austinrebello', password='mysql',
                              host='localhost',
                              database='climate') 
    cursor = cnx.cursor(buffered=True)
    # - #
    
    ### --- ###

    
    ### Ouput files for html ###
    output_file = '../../PDFTxtFiles/90degree/90degree_'+site+'.html' # CVG output file path
    ### --- ###

    
    ### Parameters for data request ###
    # Number of 90 degree days in current year
    params_90_cy = {"sid":site.upper()+"thr","sdate":str(cy),"edate":str(cy),"meta":"name","elems":[{"name":"maxt","interval":"yly","duration":"yly","reduce":{"reduce":"cnt_ge_90"}}]};
    # - #
    # Number of 90 degree days in a year
    params_90_year = {"sid":site.upper()+"thr","sdate":"por","edate":str(int(cy)-1),"meta":"name","elems":[{"name":"maxt","interval":"yly","duration":"yly","reduce":{"reduce":"cnt_ge_90"}}]};
    # - #

    # Earliest 90 degree day every year
    params_90_first = {"sid":site.upper()+"thr","sdate":"por","edate":"por","meta":"name","elems":[{"name":"maxt","interval":"yly","duration":"yly","reduce":"first_ge_90","smry":"min"}]};
    # - #

    # Latest 90 degree day every year
    params_90_last = {"sid":site.upper()+"thr","sdate":"por","edate":"por","meta":"name","elems":[{"name":"maxt","interval":"yly","duration":"yly","reduce":"last_ge_90","smry":"max"}]};
    # - #

    # Longest 90 degree stretch
    params_90_stretch = {"sid":site.upper()+"thr","sdate":"1872-01-01","edate":"por","meta":"name","elems":[{"name":"maxt","interval":[1,0,0],"duration":"std","season_start":[5,1],"reduce":{"reduce":"run_ge_90","add":"date","n":1}}]};
    # - #
    ### --- ###
    
   
    ### Step 1: Obtain data from XMACIS and format ###
    # Number of 90 degree days this year- CVG #
    data_90_cy = GridData(params_90_cy) # Num of 90 degree days for CVG
    data_90_cy = str(data_90_cy) # Convert the data over to a string
    splitline = data_90_cy.split(":")
    data_90_cy_final = []
    cy_year = str(splitline[3].strip(" ' /n /t [ ] /u }"))[0:4]
    cy_value = str(splitline[3].strip(" ' /n /t [ ] /u }"))[6:10].strip(" u '")
    data_90_cy_final.append([cy_year,cy_value])
    # - #
    
    # Number of 90 degree days in a year #
    data_90_year = GridData(params_90_year) # Num of 90 degree days for CVG
    # - #

    # Normal 90 degree days (1981-2010 average)- CVG #
    data_90_year = str(data_90_year) # Convert the data over to a string
    data_90_avg = 0 # Start the average at zero
    splitline = data_90_year.split(",") # Split out the data
    counter = 0 # Start the counter at zero
    for line in splitline:
        new = line.strip(" ' /n /t [ ] /u }") # Strip each line of all the crud and output the year/ number of 90 days
        #print new
        if ((counter > 218) & (counter < 279)): # If the counter is between the given years of 1981- 2010 count the number of 90 degree days
           if (int(counter)%2==0): # The "even number" lines are the amount of 90 degree days
               data_90_avg = int(new) + data_90_avg # Add the number of 90 degree days for each year together
        counter = counter + 1 # Advance the counter
    data_90_avg = round((float(data_90_avg)/30),1) # Caculate the average number of 90 degree days based off the 1981-2010 normals
    # - #

    # Most 90 degree days in a year- CVG #
    data_90_year = str(data_90_year)
    splitline = data_90_year.split(",")
    counter = 0
    totalcount = 0
    index = 0
    dtype = [('date','S10'),('count',int)]
    values = []
    data_90_most_final = []
    for line in splitline:
        new = line.strip(" ' /n /t [ ] /u }")
        if totalcount >0:
            if counter == 0:
                year = str(new)
            if counter == 1:
                try:
                    count = int(new)
                except:
                    count = 0
                values.append([])
                values[index]=(year,count)
                counter = -1
                index = index + 1
            counter = counter + 1
        totalcount = totalcount + 1
    data_90_most = np.sort(np.array(values,dtype),order='count')[::-1]
    data_90_most_final.append((data_90_most[0][0],data_90_most[0][1]))
    for j in range(len(data_90_most)):
        if data_90_most[j][1] == data_90_most[j+1][1]:
            data_90_most_final.append((data_90_most[j+1][0],data_90_most[j+1][1]))
        else:
            break
    # - #

    # Least number of 90 degree days in a year- CVG #
    data_90_least = data_90_most[::-1]
    data_90_least_final = []
    data_90_least_final.append((data_90_least[0][0],data_90_least[0][1]))
    for j in range(len(data_90_least)):
        if data_90_least[j][1] == data_90_least[j+1][1] and len(re.sub("\D", "", (data_90_least[j+1][0]).decode("utf-8"))):
            data_90_least_final.append((data_90_least[j+1][0],data_90_least[j+1][1]))
        else:
            break
    # - #

    # Date of first 90 degree day in a year- #
    data_90_first = GridData(params_90_first)
    data_90_first = str(data_90_first)
    splitline = data_90_first.split(",")
    data_90_first_final = (splitline[(len(splitline)-1)]).strip(" /u ' smry' : [ } ]")
    # - #

    # Date of last 90 degree day in a year- CVG #
    data_90_last = GridData(params_90_last)
    data_90_last = str(data_90_last)
    splitline = data_90_last.split(",")
    data_90_last_final = (splitline[(len(splitline)-1)]).strip(" /u ' smry' : [ } ]")
    # - #

    # Longest 90 degree strech
    data_90_stretch = GridData(params_90_stretch)
    data_90_stretch = str(data_90_stretch)
    splitline = data_90_stretch.split(",")
    counter = 0
    totalcount = 0
    index = 0
    dtype = [('date','S10'),('count',int)]
    values = []
    #np.sort(a,order='count')
    for line in splitline:
        new = line.strip(" ' /n /t [ ] /u }")
        if totalcount >3:
            #print line
            if counter == 1:
                try:
                    date_count = int(new)
                except:
                    date_count = 0
            if counter == 2:
                end_date = str(new)
                values.append([])
                values[index]=(end_date,date_count)
                counter = -1
                index = index + 1
            counter = counter + 1
        totalcount = totalcount + 1
    data_90_stretch_order = np.sort(np.array(values,dtype),order='count')[::-1]
    data_90_stretch_order_final = []
    data_90_stretch_order_final.append((data_90_stretch_order[0][0],data_90_stretch_order[0][1]))
    for j in range(len(data_90_stretch_order)):
        if data_90_stretch_order[j][1] == data_90_stretch_order[j+1][1]:
            #print data_90_cmh_least[j+1]
            data_90_stretch_order_final.append((data_90_stretch_order[j+1][0],data_90_stretch_order[j+1][1]))
        else:
            break

    # Most 90 degree days in a month- #
    month_totals = []
    # Get most 90 degree days in April, May, June, July, August, September, October #
    month_number = ('04','05','06','07','08','09','10')
    for monum in range(len(month_number)):
        #print str(month_number[monum])
        query = ("SELECT year_"+site+", count_"+site+" FROM climate.90degree_"+site+" where month_"+site+" = '"+str(month_number[monum])+"' ORDER BY count_"+site+"+0 DESC, year_"+site+" DESC;")
        #print query
        cursor.execute(query)
        row = cursor.fetchone()
        #print ( str(month_number[monum]) + str(row) )
        month_totals.append(str(month_number[monum]) + "," + str(row))
    # - #
    
    ### --- ###

    ### Step 2: 90 degree climate information list setup- includes needed html for formatting ###
    # List setup #
    degree90 = [] # Initialize CVG list
    # - #

    # Header/ MISC Info #
    # CVG
    degree90.append('<table align="center" border="0" cellpadding="1" cellspacing="1" style="width: 750px;">'+ '\n' +
                        '<tbody>'+ '\n' +
                        '<tr>'+ '\n' +
			'<td style="vertical-align: middle" align="center" colspan="3"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">'+ '\n' +
                        'Last Update: ' + current_date+ '\n' +
                        '<br />'+ '\n' +
                        '<br />'+ '\n' +
			'</p></td>'+ '\n' +
                        '</tr>'+ '\n' +
                        '</tbody>'+ '\n' +
                        '</table>'+ '\n')

    # Number of 90 degree days so far this year #
    degree90.append('<table align="center" border="1" cellpadding="1" cellspacing="1" style="width: 750px;">'+ '\n' +
                        '<tbody>'+ '\n' +
                        '<tr>'+ '\n' +
			'<td bgcolor="#424949" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">' +str(data_90_cy_final[0][0])+ ' Total<br />'+ '\n' +
			'</p></td>'+ '\n' +
			'<td bgcolor="#CCD1D1" style="vertical-align: middle" align="center" colspan="3"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">' +
                        str(data_90_cy_final[0][1]) + '<br />'+ '\n' +
			'</p></td>'+ '\n' +
                        '</tr>')
    # - #
    
    # Normal per year #
    normal90_per_year = str(data_90_avg)
    degree90.append('<tr>'+ '\n' +
			'<td bgcolor="#922B21" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Normal Per Year<br />'+ '\n' +
			'</p></td>'+ '\n' +
			'<td bgcolor="#F2D7D5" style="vertical-align: middle" align="center" colspan="3"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    degree90.append(normal90_per_year)
    degree90.append('<br />'+ '\n' +
			'</p></td>'+ '\n' +
                        '</tr>'+ '\n')
    # - #
    
    # Most in a year #
    most90_per_year = (data_90_most_final)
    for j in range(len(most90_per_year)):
        degree90.append('<tr>'+ '\n')
        if j == 0:
            if (len(most90_per_year)) > 1:
                degree90.append('<td bgcolor="#922B21" style="vertical-align: middle" align="center" rowspan="' + str(len(most90_per_year)) + '" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Most In A Year<br />'+ '\n' +
                                    '</p></td>'+ '\n')
            else:
                degree90.append('<td bgcolor="#922B21" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Most In A Year<br />'+ '\n' +
                                    '</p></td>'+ '\n')
            degree90.append('<td bgcolor="#F2D7D5" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
            degree90.append((most90_per_year[j][0]).decode("utf-8"))
            degree90.append('<br />'+ '\n' +
                                '</p></td>'+ '\n' +
                                '<td bgcolor="#F2D7D5" style="vertical-align: middle" align="center" colspan="2"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
            degree90.append(str(most90_per_year[j][1]))
            degree90.append('<br />'+ '\n'
                                '</p></td>'+ '\n')	
        if j > 0:
            degree90.append('<td bgcolor="#F2D7D5" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
            degree90.append((most90_per_year[j][0]).decode("utf-8"))
            degree90.append('<br />'+ '\n' +
                                '</p></td>'+ '\n' +
                                '<td bgcolor="#F2D7D5" style="vertical-align: middle" align="center" colspan="2"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
            degree90.append(str(most90_per_year[j][1]))
            degree90.append('<br />'+ '\n'
                                '</p></td>'+ '\n')			
    degree90.append('</tr>'+ '\n')
    # - #
    
    # Fewest in a year #
    least90_per_year = (data_90_least_final)
    numOfFewest = len(least90_per_year)
    if numOfFewest > 5:
        numOfFewest = 5
    for j in range(len(least90_per_year), len(least90_per_year)-numOfFewest, -1):
        degree90.append('<tr>'+ '\n')
        if j == len(least90_per_year):

            if (numOfFewest) > 1:
                degree90.append('<td bgcolor="#922B21" style="vertical-align: middle" align="center" rowspan="' + str(numOfFewest) + '" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Fewest In A Year<br />'+ '\n' +
                                    '</p></td>'+ '\n')
            else:
                degree90.append('<td bgcolor="#922B21" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Fewest In A Year<br />'+ '\n' +
                                    '</p></td>'+ '\n')
            degree90.append('<td bgcolor="#F2D7D5" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
            degree90.append((least90_per_year[j-1][0]).decode("utf-8")) 
            degree90.append('<br />'+ '\n' +
                                '</p></td>'+ '\n' +
                                '<td bgcolor="#F2D7D5" style="vertical-align: middle" align="center" colspan="2"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
            degree90.append(str(least90_per_year[j-1][1]))
            degree90.append('<br />'+ '\n'
                                '</p></td>'+ '\n')
            brokenLine = False
        else:
            degree90.append('<td bgcolor="#F2D7D5" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
            degree90.append((least90_per_year[j-1][0]).decode("utf-8"))
            degree90.append('<br />'+ '\n' +
                                '</p></td>'+ '\n' +
                                '<td bgcolor="#F2D7D5" style="vertical-align: middle" align="center" colspan="2"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
            degree90.append(str(least90_per_year[j-1][1]))
            degree90.append('<br />'+ '\n'
                                '</p></td>'+ '\n')			
    degree90.append('</tr>'+ '\n')

    # - #
    
    # Earliest in a year #  
    earliest90 = str(data_90_first_final)
    degree90.append('<tr>'+ '\n' +
                        '<td bgcolor="#B03A2E" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Earliest<br />'+ '\n' +
      			'</p></td>'+ '\n' +
                        '<td bgcolor="#F5B7B1" style="vertical-align: middle" align="center" colspan="2"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    degree90.append(earliest90)
    degree90.append('<br />'+ '\n' +
      			'</p></td>'+ '\n' +
                        '</tr>'+ '\n')
    # - #
    
    # Latest in a year #    
    latest90 = str(data_90_last_final)
    degree90.append('<tr>'+ '\n' +
			'<td bgcolor="#B03A2E" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Latest<br />'+ '\n' +
                	'</p></td>'+ '\n' +
                        '<td bgcolor="#F5B7B1" style="vertical-align: middle" align="center" colspan="2"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    degree90.append(latest90)
    degree90.append('<br />'+ '\n' +
                        '</p></td>'+ '\n' +
                        '</tr>'+ '\n') 

    # - #
    
    # Most in April
    month_totals_apr = str(month_totals[0])
    month_totals_apryr_final = month_totals_apr[4:11].strip("' ,")
    month_totals_aprnum_final = month_totals_apr[12:21].strip("u ' ) ")
    degree90.append('<tr>'+ '\n' +
                        '<td bgcolor="#BA4A00" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Most in April<br />'+ '\n' +
                	'</p></td>'+ '\n' +
                    	'<td bgcolor="#EDBB99" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    degree90.append(month_totals_apryr_final)
    degree90.append('<br />'+'</p></td>'+ '<td bgcolor="#EDBB99" style="vertical-align: middle" align="center" colspan="2"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    degree90.append(month_totals_aprnum_final)
    degree90.append('<br />'+ '\n' +
                        '</p></td>'+ '\n' +
                        '</tr>'+ '\n') 
    
    # Most in May
    month_totals_may = str(month_totals[1])
    month_totals_mayyr_final = month_totals_may[4:11].strip("' ,")
    month_totals_maynum_final = month_totals_may[12:21].strip("u ' ) ")
    degree90.append('<tr>'+ '\n' +
                        '<td bgcolor="#BA4A00" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Most in May<br />'+ '\n' +
                	'</p></td>'+ '\n' +
                    	'<td bgcolor="#EDBB99" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    degree90.append(month_totals_mayyr_final)
    degree90.append('<br />'+'</p></td>'+ '<td bgcolor="#EDBB99" style="vertical-align: middle" align="center" colspan="2"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    degree90.append(month_totals_maynum_final)
    degree90.append('<br />'+ '\n' +
                        '</p></td>'+ '\n' +
                        '</tr>'+ '\n') 
    
    # Most in June
    month_totals_june = str(month_totals[2])
    month_totals_juneyr_final = month_totals_june[4:11].strip("' ,")
    month_totals_junenum_final = month_totals_june[12:21].strip("u ' ) ")
    degree90.append('<tr>'+ '\n' +
                        '<td bgcolor="#BA4A00" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Most in June<br />'+ '\n' +
                	'</p></td>'+ '\n' +
                    	'<td bgcolor="#EDBB99" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    degree90.append(month_totals_juneyr_final)
    degree90.append('<br />'+'</p></td>'+ '<td bgcolor="#EDBB99" style="vertical-align: middle" align="center" colspan="2"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    degree90.append(month_totals_junenum_final)
    degree90.append('<br />'+ '\n' +
                        '</p></td>'+ '\n' +
                        '</tr>'+ '\n') 
    
    # Most in July
    month_totals_july = str(month_totals[3])
    month_totals_julyyr_final = month_totals_july[4:11].strip("' ,")
    month_totals_julynum_final = month_totals_july[12:21].strip("u ' ) ")
    degree90.append('<tr>'+ '\n' +
                        '<td bgcolor="#BA4A00" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Most in July<br />'+ '\n' +
                	'</p></td>'+ '\n' +
                    	'<td bgcolor="#EDBB99" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    degree90.append(month_totals_julyyr_final)
    degree90.append('<br />'+'</p></td>'+ '<td bgcolor="#EDBB99" style="vertical-align: middle" align="center" colspan="2"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    degree90.append(month_totals_julynum_final)
    degree90.append('<br />'+ '\n' +
                        '</p></td>'+ '\n' +
                        '</tr>'+ '\n') 

    
    # Most in August
    month_totals_august = str(month_totals[4])
    month_totals_augustyr_final = month_totals_august[4:11].strip("' ,")
    month_totals_augustnum_final = month_totals_august[12:21].strip("u ' ) ")
    degree90.append('<tr>'+ '\n' +
                        '<td bgcolor="#BA4A00" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Most in August<br />'+ '\n' +
                	'</p></td>'+ '\n' +
                    	'<td bgcolor="#EDBB99" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    degree90.append(month_totals_augustyr_final)
    degree90.append('<br />'+'</p></td>'+ '<td bgcolor="#EDBB99" style="vertical-align: middle" align="center" colspan="2"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    degree90.append(month_totals_augustnum_final)
    degree90.append('<br />'+ '\n' +
                        '</p></td>'+ '\n' +
                        '</tr>'+ '\n') 
    
    # Most in September
    month_totals_sept = str(month_totals[5])
    month_totals_septyr_final = month_totals_sept[4:11].strip("' ,")
    month_totals_septnum_final = month_totals_sept[12:21].strip("u ' ) ")
    degree90.append('<tr>'+ '\n' +
                        '<td bgcolor="#BA4A00" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Most in September<br />'+ '\n' +
                	'</p></td>'+ '\n' +
                    	'<td bgcolor="#EDBB99" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    degree90.append(month_totals_septyr_final)
    degree90.append('<br />'+'</p></td>'+ '<td bgcolor="#EDBB99" style="vertical-align: middle" align="center" colspan="2"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    degree90.append(month_totals_septnum_final)
    degree90.append('<br />'+ '\n' +
                        '</p></td>'+ '\n' +
                        '</tr>'+ '\n') 
    
    # Most in October
    month_totals_oct = str(month_totals[6])
    month_totals_octyr_final = month_totals_oct[4:11].strip("' ,")
    month_totals_octnum_final = month_totals_oct[12:21].strip("u ' ) ")
    degree90.append('<tr>'+ '\n' +
                        '<td bgcolor="#BA4A00" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Most in October<br />'+ '\n' +
                	'</p></td>'+ '\n' +
                    	'<td bgcolor="#EDBB99" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    degree90.append(month_totals_octyr_final)
    degree90.append('<br />'+'</p></td>'+ '<td bgcolor="#EDBB99" style="vertical-align: middle" align="center" colspan="2"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    degree90.append(month_totals_octnum_final)
    degree90.append('<br />'+ '\n' +
                        '</p></td>'+ '\n' +
                        '</tr>'+ '\n')
    
    # Longest stretch
    longest90 = (data_90_stretch_order_final)
    for j in range(len(longest90)):
        degree90.append('<tr>'+ '\n')
        if j == 0:
            if (len(longest90)) > 1:
                degree90.append('<td bgcolor="#CA6F1E" style="vertical-align: middle" align="center" rowspan="' + str(len(longest90)) + '" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Longest Stretch (End Date)<br />'+ '\n' +
                                    '</p></td>'+ '\n')
            else:
                degree90.append('<td bgcolor="#CA6F1E" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Longest Stretch (End Date)<br />'+ '\n' +
                                    '</p></td>'+ '\n')
            degree90.append('<td bgcolor="#F5CBA7" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
            degree90.append((longest90[j][0]).decode("utf-8"))
            degree90.append('<br />'+ '\n' +
                                '</p></td>'+ '\n' +
                                '<td bgcolor="#F5CBA7" style="vertical-align: middle" align="center" colspan="2"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
            degree90.append(str(longest90[j][1]))
            degree90.append('<br />'+ '\n'
                                '</p></td>'+ '\n')	
        if j > 0:
            degree90.append('<td bgcolor="#F5CBA7" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
            degree90.append((longest90[j][0]).decode("utf-8"))
            degree90.append('<br />'+ '\n' +
                                '</p></td>'+ '\n' +
                                '<td bgcolor="#F5CBA7" style="vertical-align: middle" align="center" colspan="2"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
            degree90.append(str(longest90[j][1]))
            degree90.append('<br />'+ '\n'
                                '</p></td>'+ '\n')			
    degree90.append('</tr>'+ '\n')    

    # Add other static text (period of record/ normal
    degree90.append('<tr>'+ '\n' +
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
                        '</table>')


    ### --- ###
        
    ### Step 3: Export file as .html ###
    print(' Writing data to files... ')

    # Open output files for writing #
    final_90degree = open(output_file,"w+") # Open cvg file for writing
    # - #

    # For loop to write out files- CVG #
    for j in range(len(degree90)):
        #print degree90[j]
        text = degree90[j]
        final_90degree.write(text)
    # - #


    ### --- ###


    ### Step 4: Close all the open files and generate pdf files ###
    final_90degree.close()

    # Create pdf files #
    print(' Now creating pdf files')
    pdfkit.from_file('../../PDFTxtFiles/90degree/90degree_'+site+'.html', '../../PDFTxtFiles/90degree/90degree_'+site+'.pdf')

    # Close Connection
    cursor.close()
    cnx.close()

for site in sites:
    htmlSite(site)
    