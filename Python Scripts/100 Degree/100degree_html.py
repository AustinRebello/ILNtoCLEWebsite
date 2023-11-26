# Name: Brian Haines
# Date: 1/16/2017
# Purpose: Create a script that requests 100 degree information
# Version/ update history:
#    1) 1-15-2017: Added 100 degree tables to mysql and finised 100degreecount_sql.py
#    2) 1-16-2017: Finished 100 degree script to get all pdfs automatically made
#    *** Still need to look at por date for Longest 100 degree strech ***
#    *** Add max missing to code? ***
#    3) 2-21-2017: Updated por date for 100 stretch. Also updated path output and float for normal

#######################################
# Import modules required by Acis
import urllib.request as urlL
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
    
    # mysql constants #
    cnx = mysql.connector.connect(user='austinrebello', password='mysql',
                              host='localhost',
                              database='climate') 
    cursor = cnx.cursor(buffered=True)
    # - #
    
    ### --- ###

    
    ### Ouput files for html ###
    output_file = '../../PDFTxtFiles/100degree/100degree_'+site+'.html' # Output file path
    ### --- ###

    
    ### Parameters for data request ###
    # Number of 100 degree days in current year
    params_100_cy = {"sid":site.upper()+"thr","sdate":str(cy),"edate":str(cy),"meta":"name","elems":[{"name":"maxt","interval":"yly","duration":"yly","reduce":{"reduce":"cnt_ge_100"}}]};
    # - #
    # Number of 100 degree days in a year
    params_100_year = {"sid":site.upper()+"thr","sdate":"por","edate":str(int(cy)-1),"meta":"name","elems":[{"name":"maxt","interval":"yly","duration":"yly","reduce":{"reduce":"cnt_ge_100"}}]};
    # - #

    # Earliest 100 degree day every year
    params_100_first = {"sid":site.upper()+"thr","sdate":"por","edate":"por","meta":"name","elems":[{"name":"maxt","interval":"yly","duration":"yly","reduce":"first_ge_100","smry":"min"}]};
    # - #

    # Latest 100 degree day every year
    params_100_last = {"sid":site.upper()+"thr","sdate":"por","edate":"por","meta":"name","elems":[{"name":"maxt","interval":"yly","duration":"yly","reduce":"last_ge_100","smry":"max"}]};
    # - #

    # Longest 100 degree stretch
    params_100_stretch = {"sid":site.upper()+"thr","sdate":"1872-01-01","edate":"por","meta":"name","elems":[{"name":"maxt","interval":[1,0,0],"duration":"std","season_start":[5,1],"reduce":{"reduce":"run_ge_100","add":"date","n":1}}]};
    # - #
    ### --- ###
    
   
    ### Step 1: Obtain data from XMACIS and format ###
    # Number of 100 degree days this year- #
    data_100_cy = GridData(params_100_cy) # Num of 100 degree days
    data_100_cy = str(data_100_cy) # Convert the data over to a string
    splitline = data_100_cy.split(":")
    data_100_cy_final = []
    cy_year = str(splitline[3].strip(" ' /n /t [ ] /u }"))[0:4]
    cy_value = str(splitline[3].strip(" ' /n /t [ ] /u }"))[6:10].strip(" u '")
    data_100_cy_final.append([cy_year,cy_value])
    # - #
    
    # Number of 100 degree days in a year #
    data_100_year = GridData(params_100_year) # Num of 100 degree days
    # - #

    # Normal 100 degree days (1981-2010 average)- CVG #
    data_100_year = str(data_100_year) # Convert the data over to a string
    data_100_avg = 0 # Start the average at zero
    splitline = data_100_year.split(",") # Split out the data
    counter = 0 # Start the counter at zero
    for line in splitline:
        new = line.strip(" ' /n /t [ ] /u }") # Strip each line of all the crud and output the year/ number of 100 days
        #print new
        if ((counter > 218) & (counter < 279)): # If the counter is between the given years of 1981- 2010 count the number of 100 degree days
           if (int(counter)%2==0): # The "even number" lines are the amount of 100 degree days
               data_100_avg = int(new) + data_100_avg # Add the number of 100 degree days for each year together
        counter = counter + 1 # Advance the counter
    data_100_avg = round((float(data_100_avg)/30),1) # Caculate the average number of 100 degree days based off the 1981-2010 normals
    # - #

    # Most 100 degree days in a year- CVG #
    data_100_year = str(data_100_year)
    splitline = data_100_year.split(",")
    counter = 0
    totalcount = 0
    index = 0
    dtype = [('date','S10'),('count',int)]
    values = []
    data_100_most_final = []
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
    data_100_most = np.sort(np.array(values,dtype),order='count')[::-1]
    data_100_most_final.append((data_100_most[0][0],data_100_most[0][1]))
    for j in range(len(data_100_most)):
        if data_100_most[j][1] == data_100_most[j+1][1]:
            data_100_most_final.append((data_100_most[j+1][0],data_100_most[j+1][1]))
        else:
            break
    # - #
    
    # Least number of 100 degree days in a year- #
    data_100_least = data_100_most[::-1]
    data_100_least_final = []
    data_100_least_final.append((data_100_least[0][0],data_100_least[0][1]))
    for j in range(len(data_100_least)):
        if data_100_least[j][1] == data_100_least[j+1][1]:
            data_100_least_final.append((data_100_least[j+1][0],data_100_least[j+1][1]))
        else:
            break
    # - #

    # Date of first 100 degree day in a year- #
    data_100_first = GridData(params_100_first)
    data_100_first = str(data_100_first)
    splitline = data_100_first.split(",")
    data_100_first_final = (splitline[(len(splitline)-1)]).strip(" /u ' smry' : [ } ]")
    # - #

    # Date of last 100 degree day in a year- #
    data_100_last = GridData(params_100_last)
    data_100_last = str(data_100_last)
    splitline = data_100_last.split(",")
    data_100_last_final = (splitline[(len(splitline)-1)]).strip(" /u ' smry' : [ } ]")
    # - #

    # Longest 100 degree stretch
    data_100_stretch = GridData(params_100_stretch)
    data_100_stretch = str(data_100_stretch)
    splitline = data_100_stretch.split(",")
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
    data_100_stretch_order = np.sort(np.array(values,dtype),order='count')[::-1]
    data_100_stretch_order_final = []
    data_100_stretch_order_final.append((data_100_stretch_order[0][0],data_100_stretch_order[0][1]))
    for j in range(len(data_100_stretch_order)):
        if data_100_stretch_order[j][1] == data_100_stretch_order[j+1][1]:
            #print data_100_cmh_least[j+1]
            data_100_stretch_order_final.append((data_100_stretch_order[j+1][0],data_100_stretch_order[j+1][1]))
        else:
            break

    # Most 100 degree days in a month- CVG #
    month_totals = []
    # Get most 100 degree days in April, May, June, July, August, September, October #
    month_number = ('04','05','06','07','08','09','10')
    for monum in range(len(month_number)):
        #print str(month_number[monum])
        query = ("SELECT year_"+site+", count_"+site+" FROM climate.100degree_"+site+" where month_"+site+" = '"+str(month_number[monum])+"' ORDER BY count_"+site+"+0 DESC, year_"+site+" DESC;")
        #print query
        cursor.execute(query)
        row = cursor.fetchone()
        #print ( str(month_number[monum]) + str(row) )
        month_totals.append(str(month_number[monum]) + "," + str(row))
    # - #
    ### --- ###

    ### Step 2: 100 degree climate information list setup- includes needed html for formatting ###
    # List setup #
    degree100 = [] # Initialize list
    # - #

    # Header/ MISC Info #
    degree100.append('<table align="center" border="0" cellpadding="1" cellspacing="1" style="width: 750px;">'+ '\n' +
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
    # - #

    # Number of 100 degree days so far this year #
    degree100.append('<table align="center" border="1" cellpadding="1" cellspacing="1" style="width: 750px;">'+ '\n' +
                        '<tbody>'+ '\n' +
                        '<tr>'+ '\n' +
			'<td bgcolor="#424949" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">'+ str(data_100_cy_final[0][0]) +' Total<br />'+ '\n' +
			'</p></td>'+ '\n' +
			'<td bgcolor="#CCD1D1" style="vertical-align: middle" align="center" colspan="3"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">' +
                        str(data_100_cy_final[0][1]) + '<br />'+ '\n' +
			'</p></td>'+ '\n' +
                        '</tr>')
    # - #
    
    # Normal per year #
    normal100_per_year = str(data_100_avg)
    degree100.append('<tr>'+ '\n' +
			'<td bgcolor="#922B21" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Normal Per Year<br />'+ '\n' +
			'</p></td>'+ '\n' +
			'<td bgcolor="#F2D7D5" style="vertical-align: middle" align="center" colspan="3"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    degree100.append(normal100_per_year)
    degree100.append('<br />'+ '\n' +
			'</p></td>'+ '\n' +
                        '</tr>'+ '\n')
    # - #
    
    # Most in a year #
    most100_per_year = (data_100_most_final)
    for j in range(len(most100_per_year)):
        degree100.append('<tr>'+ '\n')
        if j == 0:
            if (len(most100_per_year)) > 1:
                degree100.append('<td bgcolor="#922B21" style="vertical-align: middle" align="center" rowspan="' + str(len(most100_per_year)) + '" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Most In A Year<br />'+ '\n' +
                                    '</p></td>'+ '\n')
            else:
                degree100.append('<td bgcolor="#922B21" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Most In A Year<br />'+ '\n' +
                                    '</p></td>'+ '\n')
            degree100.append('<td bgcolor="#F2D7D5" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
            degree100.append((most100_per_year[j][0]).decode("utf-8"))
            degree100.append('<br />'+ '\n' +
                                '</p></td>'+ '\n' +
                                '<td bgcolor="#F2D7D5" style="vertical-align: middle" align="center" colspan="2"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
            degree100.append(str(most100_per_year[j][1]))
            degree100.append('<br />'+ '\n'
                                '</p></td>'+ '\n')	
        if j > 0:
            degree100.append('<td bgcolor="#F2D7D5" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
            degree100.append((most100_per_year[j][0]).decode("utf-8"))
            degree100.append('<br />'+ '\n' +
                                '</p></td>'+ '\n' +
                                '<td bgcolor="#F2D7D5" style="vertical-align: middle" align="center" colspan="2"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
            degree100.append(str(most100_per_year[j][1]))
            degree100.append('<br />'+ '\n'
                                '</p></td>'+ '\n')			
    degree100.append('</tr>'+ '\n')
    # - #
    
    # Earliest in a year #  
    earliest100 = str(data_100_first_final)
    degree100.append('<tr>'+ '\n' +
                        '<td bgcolor="#B03A2E" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Earliest<br />'+ '\n' +
      			'</p></td>'+ '\n' +
                        '<td bgcolor="#F5B7B1" style="vertical-align: middle" align="center" colspan="2"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    degree100.append(earliest100)
    degree100.append('<br />'+ '\n' +
      			'</p></td>'+ '\n' +
                        '</tr>'+ '\n')
    # - #
    
    # Latest in a year #    
    latest100 = str(data_100_last_final)
    degree100.append('<tr>'+ '\n' +
			'<td bgcolor="#B03A2E" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Latest<br />'+ '\n' +
                	'</p></td>'+ '\n' +
                        '<td bgcolor="#F5B7B1" style="vertical-align: middle" align="center" colspan="2"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    degree100.append(latest100)
    degree100.append('<br />'+ '\n' +
                        '</p></td>'+ '\n' +
                        '</tr>'+ '\n') 
    # - #
        
    # Most in June
    month_totals_june = str(month_totals[2])
    month_totals_juneyr_final = month_totals_june[4:11].strip(", '")
    month_totals_junenum_final = month_totals_june[12:21].strip("u ' ) ")
    degree100.append('<tr>'+ '\n' +
                        '<td bgcolor="#BA4A00" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Most in June<br />'+ '\n' +
                	'</p></td>'+ '\n' +
                    	'<td bgcolor="#EDBB99" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    degree100.append(month_totals_juneyr_final)
    degree100.append('<br />'+'</p></td>'+ '<td bgcolor="#EDBB99" style="vertical-align: middle" align="center" colspan="2"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    degree100.append(month_totals_junenum_final)
    degree100.append('<br />'+ '\n' +
                        '</p></td>'+ '\n' +
                        '</tr>'+ '\n') 

    # Most in July
    month_totals_july = str(month_totals[3])
    month_totals_julyyr_final = month_totals_july[4:11].strip(", '")
    month_totals_julynum_final = month_totals_july[12:21].strip("u ' ) ")
    degree100.append('<tr>'+ '\n' +
                        '<td bgcolor="#BA4A00" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Most in July<br />'+ '\n' +
                	'</p></td>'+ '\n' +
                    	'<td bgcolor="#EDBB99" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    degree100.append(month_totals_julyyr_final)
    degree100.append('<br />'+'</p></td>'+ '<td bgcolor="#EDBB99" style="vertical-align: middle" align="center" colspan="2"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    degree100.append(month_totals_julynum_final)
    degree100.append('<br />'+ '\n' +
                        '</p></td>'+ '\n' +
                        '</tr>'+ '\n') 
    
    # Most in August
    month_totals_august = str(month_totals[4])
    month_totals_augustyr_final = month_totals_august[4:11].strip(", '")
    month_totals_augustnum_final = month_totals_august[12:21].strip("u ' ) ")
    degree100.append('<tr>'+ '\n' +
                        '<td bgcolor="#BA4A00" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Most in August<br />'+ '\n' +
                	'</p></td>'+ '\n' +
                    	'<td bgcolor="#EDBB99" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    degree100.append(month_totals_augustyr_final)
    degree100.append('<br />'+'</p></td>'+ '<td bgcolor="#EDBB99" style="vertical-align: middle" align="center" colspan="2"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    degree100.append(month_totals_augustnum_final)
    degree100.append('<br />'+ '\n' +
                        '</p></td>'+ '\n' +
                        '</tr>'+ '\n') 
    
    # Most in September
    month_totals_sept = str(month_totals[5])
    month_totals_septyr_final = month_totals_sept[4:11].strip(", '")
    month_totals_septnum_final = month_totals_sept[12:21].strip("u ' ) ")
    degree100.append('<tr>'+ '\n' +
                        '<td bgcolor="#BA4A00" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Most in September<br />'+ '\n' +
                	'</p></td>'+ '\n' +
                    	'<td bgcolor="#EDBB99" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    degree100.append(month_totals_septyr_final)
    degree100.append('<br />'+'</p></td>'+ '<td bgcolor="#EDBB99" style="vertical-align: middle" align="center" colspan="2"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    degree100.append(month_totals_septnum_final)
    degree100.append('<br />'+ '\n' +
                        '</p></td>'+ '\n' +
                        '</tr>'+ '\n') 
    
    # Longest stretch
    longest100 = (data_100_stretch_order_final)
    for j in range(len(longest100)):
        degree100.append('<tr>'+ '\n')
        if j == 0:
            if (len(longest100)) > 1:
                degree100.append('<td bgcolor="#CA6F1E" style="vertical-align: middle" align="center" rowspan="' + str(len(longest100)) + '" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Longest Stretch (End Date)<br />'+ '\n' +
                                    '</p></td>'+ '\n')
            else:
                degree100.append('<td bgcolor="#CA6F1E" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Longest Stretch (End Date)<br />'+ '\n' +
                                    '</p></td>'+ '\n')
            degree100.append('<td bgcolor="#F5CBA7" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
            degree100.append((longest100[j][0]).decode("utf-8"))
            degree100.append('<br />'+ '\n' +
                                '</p></td>'+ '\n' +
                                '<td bgcolor="#F5CBA7" style="vertical-align: middle" align="center" colspan="2"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
            degree100.append(str(longest100[j][1]))
            degree100.append('<br />'+ '\n'
                                '</p></td>'+ '\n')	
        if j > 0:
            degree100.append('<td bgcolor="#F5CBA7" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
            degree100.append((longest100[j][0]).decode("utf-8"))
            degree100.append('<br />'+ '\n' +
                                '</p></td>'+ '\n' +
                                '<td bgcolor="#F5CBA7" style="vertical-align: middle" align="center" colspan="2"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
            degree100.append(str(longest100[j][1]))
            degree100.append('<br />'+ '\n'
                                '</p></td>'+ '\n')			
    degree100.append('</tr>'+ '\n')    

    # Add other static text (period of record/ normal
    # CVG
    degree100.append('<tr>'+ '\n' +
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
    final_100degree = open(output_file,"w+") # Open cvg file for writing
    # - #

    # For loop to write out files- CVG #
    for j in range(len(degree100)):
        #print degree100[j]
        text = degree100[j]
        final_100degree.write(text)
    # - #
    ### --- ###


    ### Step 4: Close all the open files and generate pdf files ###
    final_100degree.close()

    # Create pdf files #
    print(' Now creating pdf files')
    # CVG
    pdfkit.from_file('../../PDFTxtFiles/100degree/100degree_'+site+'.html', '../../PDFTxtFiles/100degree/100degree_'+site+'.pdf')

    # - #

    ### --- ###
    # Close Connection
    cursor.close()
    cnx.close()


for site in sites:
    htmlSite(site)