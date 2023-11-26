# Name: Brian Haines/ KC
# Modified By: Austin Rebello
# Date: 2/3/2017
# Purpose: Create a script that requests 32 degree information makes html and pdf files
# Version/ update history:
#    1) 2/21/2017- Finished! 
#    2) 11-26-2023: Updated code to Python3 and for NWS CLE, made code more dynamic, fixed bugs with data clensing

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
    
    # mysql constants #
    cnx = mysql.connector.connect(user='austinrebello', password='mysql',
                                host='localhost',
                                database='climate') 
    cursor = cnx.cursor(buffered=True)
    # - #
    
    ### --- ###

    
    ### Ouput files for html ###
    output_file = '../../PDFTxtFiles/32degree/32degree_'+site+'.html' # Output file path
    
    ### Parameters for data request ###
    # Number of 32 degree days in current year
    params_32_cy = {"sid":site.upper()+"thr","sdate":str(cy),"edate":str(cy),"meta":"name","elems":[{"name":"mint","interval":"yly","duration":"yly","reduce":{"reduce":"cnt_le_32"}}]}
    # - #
    # Number of 32 degree days in a year
    params_32_year = {"sid":site.upper()+"thr","sdate":"por","edate":str(int(cy)-1),"meta":"name","elems":[{"name":"mint","interval":"yly","duration":"yly","reduce":{"reduce":"cnt_le_32"}}]}
    # - #
    # Number of 32 degree days in a year
    params_32_max_year = {"sid":site.upper()+"thr","sdate":"por","edate":str(int(cy)-1),"meta":"name","elems":[{"name":"maxt","interval":"yly","duration":"yly","reduce":{"reduce":"cnt_le_32"}}]}
    # - #
    # Earliest 32 degree day every year
    params_32_earliest = {"sid":site.upper()+"thr","sdate":"1872-6-30","edate":"por","elems":[{"name":"mint","interval":[1,0,0],"duration":"std","season_start":"7-1","reduce":"first_le_32","smry":"min"}]}
    # - #

    # Latest 32 degree day every year
    params_32_last = {"sid":site.upper()+"thr","sdate":"1872-6-30","edate":"por","elems":[{"name":"mint","interval":[1,0,0],"duration":"std","season_start":"7-1","reduce":"last_le_32","smry":"max"}]}
    # - #

    # Longest 32 degree stretch
    params_32_stretch = {"sid":site.upper()+"thr","sdate":"1872-06-30","edate":"por","meta":"name","elems":[{"name":"mint","interval":[1,0,0],"duration":"std","season_start":"7-1","reduce":{"reduce":"run_le_32","add":"date","n":1}}]}
    # - #
    ### --- ###

    ### Step 1: Obtain data from XMACIS and format ###
    # Number of 32 degree days this year- CVG #
    data_32_cy = GridData(params_32_cy) # Num of 32 degree days for CVG
    data_32_cy = str(data_32_cy) # Convert the data over to a string
    splitline = data_32_cy.split(":")
    data_32_cy_final = []
    cy_year = str(splitline[3].strip(" ' /n /t [ ] /u }"))[0:4]
    cy_value = str(splitline[3].strip(" ' /n /t [ ] /u }"))[6:11].strip(" u '")
    data_32_cy_final.append([cy_year,cy_value])
    
    # Number of 32 degree days in a year
    data_32_year = GridData(params_32_year) # Num of 32 degree days for CVG
    # - #

    # Number of 32 degree days where highs <32 in a year
    data_32_max_year = GridData(params_32_max_year) # Num of 32 degree days for CVG
    # - #

    # Normal 32 degree days (1981-2010 average)- CVG #
    data_32_year = str(data_32_year) # Convert the data over to a string
    data_32_avg = 0 # Start the average at zero
    splitline = data_32_year.split(",") # Split out the data
    counter = 0 # Start the counter at zero
    for line in splitline:
        new = line.strip(" ' /n /t [ ] /u }") # Strip each line of all the crud and output the year/ number of 100 days
        #print new
        if ((counter > 218) & (counter < 279)): # If the counter is between the given years of 1981- 2010 count the number of 100 degree days
           if (int(counter)%2==0): # The "even number" lines are the amount of 100 degree days
               data_32_avg = int(new) + data_32_avg # Add the number of 100 degree days for each year together
        counter = counter + 1 # Advance the counter
    data_32_avg = round((float(data_32_avg)/30),1) # Caculate the average number of 100 degree days based off the 1981-2010 normals
    # - #
    
    # Date of first 32 degree day in a year- 
    data_32_earliest = GridData(params_32_earliest)
    data_32_earliest = str(data_32_earliest)
    splitline = data_32_earliest.split(",")
    data_32_earliest_final = (splitline[(len(splitline)-1)]).strip(" /u ' smry' : [ } ]")
    # - #
    
    # Date of last 32 degree day in a year-
    data_32_last = GridData(params_32_last)
    data_32_last = str(data_32_last)
    splitline = data_32_last.split(",")
    data_32_last_final = (splitline[(len(splitline)-1)]).strip(" /u ' smry' : [ } ]")
    # - #
    
    # Most 32 degree days in a month-
    month_totals = []
    # Get most 32 degree days in October, November, December, January, February, March, April #
    month_number = ('10','11','12','01','02','03','04')
    for monum in range(len(month_number)):
        #print str(month_number[monum])
        query = ("SELECT year_"+site+", count_"+site+" FROM climate.32degree_"+site+" where month_"+site+" = '"+str(month_number[monum])+"' ORDER BY count_"+site+"+0 DESC, year_"+site+" DESC;")
        #print query
        cursor.execute(query)
        row = cursor.fetchone()
        #print ( str(month_number[monum]) + str(row) )
        month_totals.append(str(month_number[monum]) + "," + str(row))
    # - #
    
    # Most 32 degree day highs in a month-
    month_high_totals = []
    # Get most 32 degree days in October, November, December, January, February, March, April #
    month_number = ('10','11','12','01','02','03','04')
    for monum in range(len(month_number)):
        #print str(month_number[monum])
        query = ("SELECT year_"+site+", counthigh_"+site+" FROM climate.32degree_"+site+" where month_"+site+" = '"+str(month_number[monum])+"' ORDER BY counthigh_"+site+"+0 DESC, year_"+site+" DESC;")
        #print query
        cursor.execute(query)
        row = cursor.fetchone()
        #print ( str(month_number[monum]) + str(row) )
        month_high_totals.append(str(month_number[monum]) + "," + str(row))
    # - #
    
    # Most 32 degree days in a year-
    data_32_year = str(data_32_year)
    splitline = data_32_year.split(",")
    counter = 0
    totalcount = 0
    index = 0
    dtype = [('date','S10'),('count',int)]
    values = []
    data_32_most_final = []
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
    data_32_most = np.sort(np.array(values,dtype),order='count')[::-1]
    data_32_most_final.append((data_32_most[0][0],data_32_most[0][1]))
    for j in range(len(data_32_most)):
        if data_32_most[j][1] == data_32_most[j+1][1]:
            data_32_most_final.append((data_32_most[j+1][0],data_32_most[j+1][1]))
        else:
            break
    # - #
    
    # Most 32 degree days highs in a year-
    data_32_max_year = str(data_32_max_year)
    splitline = data_32_max_year.split(",")
    counter = 0
    totalcount = 0
    index = 0
    dtype = [('date','S10'),('count',int)]
    values = []
    data_32_max_most_final = []
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
    data_32_max_most = np.sort(np.array(values,dtype),order='count')[::-1]
    data_32_max_most_final.append((data_32_max_most[0][0],data_32_max_most[0][1]))
    for j in range(len(data_32_max_most)):
        if data_32_max_most[j][1] == data_32_max_most[j+1][1]:
            data_32_max_most_final.append((data_32_max_most[j+1][0],data_32_max_most[j+1][1]))
        else:
            break
    # - #
    
    # Longest 32 degree strech
    # CVG
    data_32_stretch = GridData(params_32_stretch)
    data_32_stretch = str(data_32_stretch)
    splitline = data_32_stretch.split(",")
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
    data_32_stretch_order = np.sort(np.array(values,dtype),order='count')[::-1]
    data_32_stretch_order_final = []
    data_32_stretch_order_final.append((data_32_stretch_order[0][0],data_32_stretch_order[0][1]))
    for j in range(len(data_32_stretch_order)):
        if data_32_stretch_order[j][1] == data_32_stretch_order[j+1][1]:
            #print data_32_cmh_least[j+1]
            data_32_stretch_order_final.append((data_32_stretch_order[j+1][0],data_32_stretch_order[j+1][1]))
        else:
            break

    ### Step 2: 32 degree climate information list setup- includes needed html for formatting ###
    # List setup #
    degree32 = [] # Initializelows list
    # - #

    # Header/ MISC Info #
    degree32.append('<table align="center" border="0" cellpadding="1" cellspacing="1" style="width: 750px;">'+ '\n' +
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
                        '<tbody>'+ '\n')

    # Number of 32 degree days so far this year #
    # CVG
    degree32.append('<tr>'+ '\n' +
			'<td bgcolor="#424949" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">' +
                        str(data_32_cy_final[0][0]) +' Total<br />'+ '\n' +
			'</p></td>'+ '\n' +
			'<td bgcolor="#CCD1D1" style="vertical-align: middle" align="center" colspan="3"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">' +
                        str(data_32_cy_final[0][1]) + '<br />'+ '\n' +
			'</p></td>'+ '\n' +
                        '</tr>')
    
    # Normal per year #
    # CVG
    normal32_per_year = str(data_32_avg)
    degree32.append('<tr>'+ '\n' +
			'<td bgcolor="#1F618D" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Normal Per Year<br />'+ '\n' +
			'</p></td>'+ '\n' +
			'<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="3"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    degree32.append(normal32_per_year)
    degree32.append('<br />'+ '\n' +
			'</p></td>'+ '\n' +
                        '</tr>'+ '\n')
    
    # Earliest in a year #  
    # CVG
    earliest32 = str(data_32_earliest_final)
    degree32.append('<tr>'+ '\n' +
                        '<td bgcolor="#1F618D" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Earliest<br />'+ '\n' +
      			'</p></td>'+ '\n' +
                        '<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="2"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    degree32.append(earliest32)
    degree32.append('<br />'+ '\n' +
      			'</p></td>'+ '\n' +
                        '</tr>'+ '\n')
    
    # Latest in a year #    
    # CVG
    latest32 = str(data_32_last_final)
    degree32.append('<tr>'+ '\n' +
			'<td bgcolor="#1F618D" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Latest<br />'+ '\n' +
                	'</p></td>'+ '\n' +
                        '<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="2"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    degree32.append(latest32)
    degree32.append('<br />'+ '\n' +
                        '</p></td>'+ '\n' +
                        '</tr>'+ '\n') 
    
    # Most 32 degree days October #
    month_totals_oct = str(month_totals[0])
    month_totals_octyr_final = month_totals_oct[4:11].strip("' ,")
    month_totals_octnum_final = month_totals_oct[12:21].strip("u ' ) ")
    degree32.append('<tr>'+ '\n' +
                        '<td bgcolor="#884EA0" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Most Subfreezing lows in October<br />'+ '\n' +
                	'</p></td>'+ '\n' +
                    	'<td bgcolor="#C39BD3" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    degree32.append(month_totals_octyr_final)
    degree32.append('<br />'+'</p></td>'+ '<td bgcolor="#C39BD3" style="vertical-align: middle" align="center" colspan="2"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    degree32.append(month_totals_octnum_final)
    degree32.append('<br />'+ '\n' +
                        '</p></td>'+ '\n' +
                        '</tr>'+ '\n')
    
    # Most 32 degree days November #
    month_totals_nov = str(month_totals[1])
    month_totals_novyr_final = month_totals_nov[4:11].strip("' ,")
    month_totals_novnum_final = month_totals_nov[12:21].strip("u ' ) ")
    degree32.append('<tr>'+ '\n' +
                        '<td bgcolor="#884EA0" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Most Subfreezing lows in November<br />'+ '\n' +
                	'</p></td>'+ '\n' +
                    	'<td bgcolor="#C39BD3" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    degree32.append(month_totals_novyr_final)
    degree32.append('<br />'+'</p></td>'+ '<td bgcolor="#C39BD3" style="vertical-align: middle" align="center" colspan="2"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    degree32.append(month_totals_novnum_final)
    degree32.append('<br />'+ '\n' +
                        '</p></td>'+ '\n' +
                        '</tr>'+ '\n')
    
    # Most 32 degree days December #
    # CVG
    month_totals_dec = str(month_totals[2])
    month_totals_decyr_final = month_totals_dec[4:11].strip("' ,")
    month_totals_decnum_final = month_totals_dec[12:21].strip("u ' ) ")
    degree32.append('<tr>'+ '\n' +
                        '<td bgcolor="#884EA0" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Most Subfreezing lows in December<br />'+ '\n' +
                	'</p></td>'+ '\n' +
                    	'<td bgcolor="#C39BD3" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    degree32.append(month_totals_decyr_final)
    degree32.append('<br />'+'</p></td>'+ '<td bgcolor="#C39BD3" style="vertical-align: middle" align="center" colspan="2"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    degree32.append(month_totals_decnum_final)
    degree32.append('<br />'+ '\n' +
                        '</p></td>'+ '\n' +
                        '</tr>'+ '\n') 
    
    # Most 32 degree days January #
    # CVG
    month_totals_jan = str(month_totals[3])
    month_totals_janyr_final = month_totals_jan[4:11].strip("' ,")
    month_totals_jannum_final = month_totals_jan[12:21].strip("u ' ) ")
    degree32.append('<tr>'+ '\n' +
                        '<td bgcolor="#884EA0" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Most Subfreezing lows in January<br />'+ '\n' +
                	'</p></td>'+ '\n' +
                    	'<td bgcolor="#C39BD3" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    degree32.append(month_totals_janyr_final)
    degree32.append('<br />'+'</p></td>'+ '<td bgcolor="#C39BD3" style="vertical-align: middle" align="center" colspan="2"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    degree32.append(month_totals_jannum_final)
    degree32.append('<br />'+ '\n' +
                        '</p></td>'+ '\n' +
                        '</tr>'+ '\n')
    
    # Most 32 degree days February #
    # CVG
    month_totals_feb = str(month_totals[4])
    month_totals_febyr_final = month_totals_feb[4:11].strip("' ,")
    month_totals_febnum_final = month_totals_feb[12:21].strip("u ' ) ")
    degree32.append('<tr>'+ '\n' +
                        '<td bgcolor="#884EA0" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Most Subfreezing lows in February<br />'+ '\n' +
                	'</p></td>'+ '\n' +
                    	'<td bgcolor="#C39BD3" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    degree32.append(month_totals_febyr_final)
    degree32.append('<br />'+'</p></td>'+ '<td bgcolor="#C39BD3" style="vertical-align: middle" align="center" colspan="2"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    degree32.append(month_totals_febnum_final)
    degree32.append('<br />'+ '\n' +
                        '</p></td>'+ '\n' +
                        '</tr>'+ '\n') 

    # Most 32 degree days March #
    # CVG
    month_totals_mar = str(month_totals[5])
    month_totals_maryr_final = month_totals_mar[4:11].strip("' ,")
    month_totals_marnum_final = month_totals_mar[12:21].strip("u ' ) ")
    degree32.append('<tr>'+ '\n' +
                        '<td bgcolor="#884EA0" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Most Subfreezing lows in March<br />'+ '\n' +
                	'</p></td>'+ '\n' +
                    	'<td bgcolor="#C39BD3" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    degree32.append(month_totals_maryr_final)
    degree32.append('<br />'+'</p></td>'+ '<td bgcolor="#C39BD3" style="vertical-align: middle" align="center" colspan="2"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    degree32.append(month_totals_marnum_final)
    degree32.append('<br />'+ '\n' +
                        '</p></td>'+ '\n' +
                        '</tr>'+ '\n') 
    
    # Most 32 degree days April #
    # CVG
    month_totals_apr = str(month_totals[6])
    month_totals_apryr_final = month_totals_apr[4:11].strip("' ,")
    month_totals_aprnum_final = month_totals_apr[12:21].strip("u ' ) ")
    degree32.append('<tr>'+ '\n' +
                        '<td bgcolor="#884EA0" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Most Subfreezing lows in April<br />'+ '\n' +
                	'</p></td>'+ '\n' +
                    	'<td bgcolor="#C39BD3" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    degree32.append(month_totals_apryr_final)
    degree32.append('<br />'+'</p></td>'+ '<td bgcolor="#C39BD3" style="vertical-align: middle" align="center" colspan="2"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    degree32.append(month_totals_aprnum_final)
    degree32.append('<br />'+ '\n' +
                        '</p></td>'+ '\n' +
                        '</tr>'+ '\n') 
    
    # Most 32 degree day highs October #
    # CVG
    month_high_totals_oct = str(month_high_totals[0])
    month_high_totals_octyr_final = month_high_totals_oct[4:11].strip("' ,")
    month_high_totals_octnum_final = month_high_totals_oct[12:21].strip("u ' ) ")
    degree32.append('<tr>'+ '\n' +
                        '<td bgcolor="#884EA0" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Most Subfreezing highs in October<br />'+ '\n' +
                	'</p></td>'+ '\n' +
                    	'<td bgcolor="#C39BD3" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    degree32.append(month_high_totals_octyr_final)
    degree32.append('<br />'+'</p></td>'+ '<td bgcolor="#C39BD3" style="vertical-align: middle" align="center" colspan="2"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    degree32.append(month_high_totals_octnum_final)
    degree32.append('<br />'+ '\n' +
                        '</p></td>'+ '\n' +
                        '</tr>'+ '\n') 
    
    # Most 32 degree day highs November #
    # CVG
    month_high_totals_nov = str(month_high_totals[1])
    month_high_totals_novyr_final = month_high_totals_nov[4:11].strip("' ,")
    month_high_totals_novnum_final = month_high_totals_nov[12:21].strip("u ' ) ")
    degree32.append('<tr>'+ '\n' +
                        '<td bgcolor="#884EA0" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Most Subfreezing highs in November<br />'+ '\n' +
                	'</p></td>'+ '\n' +
                    	'<td bgcolor="#C39BD3" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    degree32.append(month_high_totals_novyr_final)
    degree32.append('<br />'+'</p></td>'+ '<td bgcolor="#C39BD3" style="vertical-align: middle" align="center" colspan="2"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    degree32.append(month_high_totals_novnum_final)
    degree32.append('<br />'+ '\n' +
                        '</p></td>'+ '\n' +
                        '</tr>'+ '\n') 
    
    # Most 32 degree day highs December #
    # CVG
    month_high_totals_dec = str(month_high_totals[2])
    month_high_totals_decyr_final = month_high_totals_dec[4:11].strip("' ,")
    month_high_totals_decnum_final = month_high_totals_dec[12:21].strip("u ' ) ")
    degree32.append('<tr>'+ '\n' +
                        '<td bgcolor="#884EA0" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Most Subfreezing highs in December<br />'+ '\n' +
                	'</p></td>'+ '\n' +
                    	'<td bgcolor="#C39BD3" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    degree32.append(month_high_totals_decyr_final)
    degree32.append('<br />'+'</p></td>'+ '<td bgcolor="#C39BD3" style="vertical-align: middle" align="center" colspan="2"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    degree32.append(month_high_totals_decnum_final)
    degree32.append('<br />'+ '\n' +
                        '</p></td>'+ '\n' +
                        '</tr>'+ '\n') 
    
    # Most 32 degree day highs January #
    # CVG
    month_high_totals_jan = str(month_high_totals[3])
    month_high_totals_janyr_final = month_high_totals_jan[4:11].strip("' ,")
    month_high_totals_jannum_final = month_high_totals_jan[12:21].strip("u ' ) ")
    degree32.append('<tr>'+ '\n' +
                        '<td bgcolor="#884EA0" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Most Subfreezing highs in January<br />'+ '\n' +
                	'</p></td>'+ '\n' +
                    	'<td bgcolor="#C39BD3" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    degree32.append(month_high_totals_janyr_final)
    degree32.append('<br />'+'</p></td>'+ '<td bgcolor="#C39BD3" style="vertical-align: middle" align="center" colspan="2"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    degree32.append(month_high_totals_jannum_final)
    degree32.append('<br />'+ '\n' +
                        '</p></td>'+ '\n' +
                        '</tr>'+ '\n') 
    
    # Most 32 degree day highs February #
    # CVG
    month_high_totals_feb = str(month_high_totals[4])
    month_high_totals_febyr_final = month_high_totals_feb[4:11].strip("' ,")
    month_high_totals_febnum_final = month_high_totals_feb[12:21].strip("u ' ) ")
    degree32.append('<tr>'+ '\n' +
                        '<td bgcolor="#884EA0" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Most Subfreezing highs in February<br />'+ '\n' +
                	'</p></td>'+ '\n' +
                    	'<td bgcolor="#C39BD3" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    degree32.append(month_high_totals_febyr_final)
    degree32.append('<br />'+'</p></td>'+ '<td bgcolor="#C39BD3" style="vertical-align: middle" align="center" colspan="2"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    degree32.append(month_high_totals_febnum_final)
    degree32.append('<br />'+ '\n' +
                        '</p></td>'+ '\n' +
                        '</tr>'+ '\n')
    
    # Most 32 degree day highs March #
    # CVG
    month_high_totals_mar = str(month_high_totals[5])
    month_high_totals_maryr_final = month_high_totals_mar[4:11].strip("' ,")
    month_high_totals_marnum_final = month_high_totals_mar[12:21].strip("u ' ) ")
    degree32.append('<tr>'+ '\n' +
                        '<td bgcolor="#884EA0" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Most Subfreezing highs in March<br />'+ '\n' +
                	'</p></td>'+ '\n' +
                    	'<td bgcolor="#C39BD3" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    degree32.append(month_high_totals_maryr_final)
    degree32.append('<br />'+'</p></td>'+ '<td bgcolor="#C39BD3" style="vertical-align: middle" align="center" colspan="2"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    degree32.append(month_high_totals_marnum_final)
    degree32.append('<br />'+ '\n' +
                        '</p></td>'+ '\n' +
                        '</tr>'+ '\n') 
    
    # Most 32 degree day highs April #
    # CVG
    month_high_totals_apr = str(month_high_totals[6])
    month_high_totals_apryr_final = month_high_totals_apr[4:11].strip("' ,")
    month_high_totals_aprnum_final = month_high_totals_apr[12:21].strip("u ' ) ")
    degree32.append('<tr>'+ '\n' +
                        '<td bgcolor="#884EA0" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Most Subfreezing highs in April<br />'+ '\n' +
                	'</p></td>'+ '\n' +
                    	'<td bgcolor="#C39BD3" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    degree32.append(month_high_totals_apryr_final)
    degree32.append('<br />'+'</p></td>'+ '<td bgcolor="#C39BD3" style="vertical-align: middle" align="center" colspan="2"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    degree32.append(month_high_totals_aprnum_final)
    degree32.append('<br />'+ '\n' +
                        '</p></td>'+ '\n' +
                        '</tr>'+ '\n')
    
    # Most 32 degree day lows in a year #
    # CVG
    most32_per_year = (data_32_most_final)
    for j in range(len(most32_per_year)):
        degree32.append('<tr>'+ '\n')
        if j == 0:
            if (len(most32_per_year)) > 1:
                degree32.append('<td bgcolor="#2E86C1" style="vertical-align: middle" align="center" rowspan="' + str(len(most32_per_year)) + '" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Most Subfreezing Lows In A Year<br />'+ '\n' +
                                    '</p></td>'+ '\n')
            else:
                degree32.append('<td bgcolor="#2E86C1" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Most Subfreezing Lows In A Year<br />'+ '\n' +
                                    '</p></td>'+ '\n')
            degree32.append('<td bgcolor="#85C1E9" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
            degree32.append((most32_per_year[j][0]).decode("utf-8"))
            degree32.append('<br />'+ '\n' +
                                '</p></td>'+ '\n' +
                                '<td bgcolor="#85C1E9" style="vertical-align: middle" align="center" colspan="2"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
            degree32.append(str(most32_per_year[j][1]))
            degree32.append('<br />'+ '\n'
                                '</p></td>'+ '\n')	
        if j > 0:
            degree32.append('<td bgcolor="#85C1E9" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
            degree32.append((most32_per_year[j][0]).decode("utf-8"))
            degree32.append('<br />'+ '\n' +
                                '</p></td>'+ '\n' +
                                '<td bgcolor="#85C1E9" style="vertical-align: middle" align="center" colspan="2"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
            degree32.append(str(most32_per_year[j][1]))
            degree32.append('<br />'+ '\n'
                                '</p></td>'+ '\n')			
    degree32.append('</tr>'+ '\n')
    
    # Most 32 degree day highs in a year #
    # CVG
    most32_max_per_year = (data_32_max_most_final)
    for j in range(len(most32_max_per_year)):
        degree32.append('<tr>'+ '\n')
        if j == 0:
            if (len(most32_max_per_year)) > 1:
                degree32.append('<td bgcolor="#2E86C1" style="vertical-align: middle" align="center" rowspan="' + str(len(most32_max_per_year)) + '" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Most Subfreezing Highs In A Year<br />'+ '\n' +
                                    '</p></td>'+ '\n')
            else:
                degree32.append('<td bgcolor="#2E86C1" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Most Subfreezing Highs In A Year<br />'+ '\n' +
                                    '</p></td>'+ '\n')
            degree32.append('<td bgcolor="#85C1E9" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
            degree32.append((most32_max_per_year[j][0]).decode("utf-8"))
            degree32.append('<br />'+ '\n' +
                                '</p></td>'+ '\n' +
                                '<td bgcolor="#85C1E9" style="vertical-align: middle" align="center" colspan="2"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
            degree32.append(str(most32_max_per_year[j][1]))
            degree32.append('<br />'+ '\n'
                                '</p></td>'+ '\n')	
        if j > 0:
            degree32.append('<td bgcolor="#85C1E9" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
            degree32.append((most32_max_per_year[j][0]).decode("utf-8"))
            degree32.append('<br />'+ '\n' +
                                '</p></td>'+ '\n' +
                                '<td bgcolor="#85C1E9" style="vertical-align: middle" align="center" colspan="2"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
            degree32.append(str(most32_max_per_year[j][1]))
            degree32.append('<br />'+ '\n'
                                '</p></td>'+ '\n')			
    degree32.append('</tr>'+ '\n')
    
    # Longest stretch
    # CVG
    longest32 = (data_32_stretch_order_final)
    for j in range(len(longest32)):
        degree32.append('<tr>'+ '\n')
        if j == 0:
            if (len(longest32)) > 1:
                degree32.append('<td bgcolor="#2E86C1" style="vertical-align: middle" align="center" rowspan="' + str(len(longest32)) + '" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Longest Stretch of Subfreezing Lows (End Date)<br />'+ '\n' +
                                    '</p></td>'+ '\n')
            else:
                degree32.append('<td bgcolor="#2E86C1" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Longest Stretch of Subfreezing Lows (End Date)<br />'+ '\n' +
                                    '</p></td>'+ '\n')
            degree32.append('<td bgcolor="#85C1E9" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
            degree32.append((longest32[j][0]).decode("utf-8"))
            degree32.append('<br />'+ '\n' +
                                '</p></td>'+ '\n' +
                                '<td bgcolor="#85C1E9" style="vertical-align: middle" align="center" colspan="2"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
            degree32.append(str(longest32[j][1]))
            degree32.append('<br />'+ '\n'
                                '</p></td>'+ '\n')	
        if j > 0:
            degree32.append('<td bgcolor="#85C1E9" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
            degree32.append((longest32[j][0]).decode("utf-8"))
            degree32.append('<br />'+ '\n' +
                                '</p></td>'+ '\n' +
                                '<td bgcolor="#85C1E9" style="vertical-align: middle" align="center" colspan="2"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
            degree32.append(str(longest32[j][1]))
            degree32.append('<br />'+ '\n'
                                '</p></td>'+ '\n')			
    degree32.append('</tr>'+ '\n')  
    
    # Add other static text (period of record/ normal)
    # CVG
    degree32.append('<tr>'+ '\n' +
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
    
    ### Step 3: Export file as .html ###
    print(' Writing data to files... ')

    # Open output files for writing #
    final_32degree = open(output_file,"w+") # Open file for writing
    
    # For loop to write out files- CVG #
    for j in range(len(degree32)):
        text = degree32[j]
        final_32degree.write(text)
    # - #
    
    ### Step 4: Close all the open files and generate pdf files ###
    final_32degree.close()

    # Create pdf files #
    print(' Now creating pdf files')
    pdfkit.from_file('../../PDFTxtFiles/32degree/32degree_'+site+'.html', '../../PDFTxtFiles/32degree/32degree_'+site+'.pdf')
    print(' Script completed and files genereated... ')
    # - #
    
    # Close Connection
    cursor.close()
    cnx.close()

### --- ###

for site in sites:
    htmlSite(site)
    