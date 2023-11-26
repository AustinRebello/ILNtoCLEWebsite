# Name: Brian Haines/ KC
# Modified By: Austin Rebello
# Date: 2/3/2017
# Purpose: Create a script that requests 0 degree information makes html and pdf files
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
    output_file = '../../PDFTxtFiles/0degree/0degree_'+site+'.html' # Output file path
    
    ### Parameters for data request ###
    # Number of 0 degree days in current year
    params_0_cy = {"sid":site.upper()+"thr","sdate":str(cy),"edate":str(cy),"meta":"name","elems":[{"name":"mint","interval":"yly","duration":"yly","reduce":{"reduce":"cnt_le_0"}}]}
    # - #
    # Number of 0 degree days in a year
    params_0_year = {"sid":site.upper()+"thr","sdate":"por","edate":str(int(cy)-1),"meta":"name","elems":[{"name":"mint","interval":"yly","duration":"yly","reduce":{"reduce":"cnt_le_0"}}]}
    # - #
    # Number of 0 degree days in a year
    params_0_max_year = {"sid":site.upper()+"thr","sdate":"por","edate":str(int(cy)-1),"meta":"name","elems":[{"name":"maxt","interval":"yly","duration":"yly","reduce":{"reduce":"cnt_le_0"}}]}
    # - #
    # Earliest 0 degree day every year
    params_0_earliest = {"sid":site.upper()+"thr","sdate":"1872-6-30","edate":"por","elems":[{"name":"mint","interval":[1,0,0],"duration":"std","season_start":"7-1","reduce":"first_le_0","smry":"min"}]}
    # - #

    # Latest 0 degree day every year
    params_0_last = {"sid":site.upper()+"thr","sdate":"1872-6-30","edate":"por","elems":[{"name":"mint","interval":[1,0,0],"duration":"std","season_start":"7-1","reduce":"last_le_0","smry":"max"}]}
    # - #

    # Longest 0 degree stretch
    params_0_stretch = {"sid":site.upper()+"thr","sdate":"1872-06-30","edate":"por","meta":"name","elems":[{"name":"mint","interval":[1,0,0],"duration":"std","season_start":"7-1","reduce":{"reduce":"run_le_0","add":"date","n":1}}]}
    # - #
    ### --- ###

    ### Step 1: Obtain data from XMACIS and format ###
    # Number of 0 degree days this year- CVG #
    data_0_cy = GridData(params_0_cy) # Num of 0 degree days for CVG
    data_0_cy = str(data_0_cy) # Convert the data over to a string
    splitline = data_0_cy.split(":")
    data_0_cy_final = []
    cy_year = str(splitline[3].strip(" ' /n /t [ ] /u }"))[0:4]
    cy_value = str(splitline[3].strip(" ' /n /t [ ] /u }"))[6:11].strip(" u '")
    data_0_cy_final.append([cy_year,cy_value])
    
    # Number of 0 degree days in a year
    data_0_year = GridData(params_0_year) # Num of 0 degree days for CVG
    # - #

    # Number of 0 degree days where highs <0 in a year
    data_0_max_year = GridData(params_0_max_year) # Num of 0 degree days for CVG
    # - #

    # Normal 0 degree days (1981-2010 average)- CVG #
    data_0_year = str(data_0_year) # Convert the data over to a string
    data_0_avg = 0 # Start the average at zero
    splitline = data_0_year.split(",") # Split out the data
    counter = 0 # Start the counter at zero
    for line in splitline:
        new = line.strip(" ' /n /t [ ] /u }") # Strip each line of all the crud and output the year/ number of 100 days
        #print new
        if ((counter > 218) & (counter < 279)): # If the counter is between the given years of 1981- 2010 count the number of 100 degree days
           if (int(counter)%2==0): # The "even number" lines are the amount of 100 degree days
               data_0_avg = int(new) + data_0_avg # Add the number of 100 degree days for each year together
        counter = counter + 1 # Advance the counter
    data_0_avg = round((float(data_0_avg)/30),1) # Caculate the average number of 100 degree days based off the 1981-2010 normals
    # - #
    
    # Date of first 0 degree day in a year- 
    data_0_earliest = GridData(params_0_earliest)
    data_0_earliest = str(data_0_earliest)
    splitline = data_0_earliest.split(",")
    data_0_earliest_final = (splitline[(len(splitline)-1)]).strip(" /u ' smry' : [ } ]")
    # - #
    
    # Date of last 0 degree day in a year-
    data_0_last = GridData(params_0_last)
    data_0_last = str(data_0_last)
    splitline = data_0_last.split(",")
    data_0_last_final = (splitline[(len(splitline)-1)]).strip(" /u ' smry' : [ } ]")
    # - #
    
    # Most 0 degree days in a month-
    month_totals = []
    # Get most 0 degree days in October, November, December, January, February, March, April #
    month_number = ('11','12','01','02','03')
    for monum in range(len(month_number)):
        #print str(month_number[monum])
        query = ("SELECT year_"+site+", count_"+site+" FROM climate.0degree_"+site+" where month_"+site+" = '"+str(month_number[monum])+"' ORDER BY count_"+site+"+0 DESC, year_"+site+" DESC;")
        #print query
        cursor.execute(query)
        row = cursor.fetchone()
        #print ( str(month_number[monum]) + str(row) )
        month_totals.append(str(month_number[monum]) + "," + str(row))
    # - #
    
    # Most 0 degree day highs in a month-
    month_high_totals = []
    # Get most 0 degree days in October, November, December, January, February, March, April #
    month_number = ('11','12','01','02','03')
    for monum in range(len(month_number)):
        #print str(month_number[monum])
        query = ("SELECT year_"+site+", counthigh_"+site+" FROM climate.0degree_"+site+" where month_"+site+" = '"+str(month_number[monum])+"' ORDER BY counthigh_"+site+"+0 DESC, year_"+site+" DESC;")
        #print query
        cursor.execute(query)
        row = cursor.fetchone()
        #print ( str(month_number[monum]) + str(row) )
        month_high_totals.append(str(month_number[monum]) + "," + str(row))
    # - #
    
    # Most 0 degree days in a year-
    data_0_year = str(data_0_year)
    splitline = data_0_year.split(",")
    counter = 0
    totalcount = 0
    index = 0
    dtype = [('date','S10'),('count',int)]
    values = []
    data_0_most_final = []
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
    data_0_most = np.sort(np.array(values,dtype),order='count')[::-1]
    data_0_most_final.append((data_0_most[0][0],data_0_most[0][1]))
    for j in range(len(data_0_most)):
        if data_0_most[j][1] == data_0_most[j+1][1]:
            data_0_most_final.append((data_0_most[j+1][0],data_0_most[j+1][1]))
        else:
            break
    # - #
    
    # Most 0 degree days highs in a year-
    data_0_max_year = str(data_0_max_year)
    splitline = data_0_max_year.split(",")
    counter = 0
    totalcount = 0
    index = 0
    dtype = [('date','S10'),('count',int)]
    values = []
    data_0_max_most_final = []
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
    data_0_max_most = np.sort(np.array(values,dtype),order='count')[::-1]
    data_0_max_most_final.append((data_0_max_most[0][0],data_0_max_most[0][1]))
    for j in range(len(data_0_max_most)):
        if data_0_max_most[j][1] == data_0_max_most[j+1][1]:
            data_0_max_most_final.append((data_0_max_most[j+1][0],data_0_max_most[j+1][1]))
        else:
            break
    # - #
    
    # Longest 0 degree strech
    # CVG
    data_0_stretch = GridData(params_0_stretch)
    data_0_stretch = str(data_0_stretch)
    splitline = data_0_stretch.split(",")
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
    data_0_stretch_order = np.sort(np.array(values,dtype),order='count')[::-1]
    data_0_stretch_order_final = []
    data_0_stretch_order_final.append((data_0_stretch_order[0][0],data_0_stretch_order[0][1]))
    for j in range(len(data_0_stretch_order)):
        if data_0_stretch_order[j][1] == data_0_stretch_order[j+1][1]:
            #print data_0_cmh_least[j+1]
            data_0_stretch_order_final.append((data_0_stretch_order[j+1][0],data_0_stretch_order[j+1][1]))
        else:
            break

    ### Step 2: 0 degree climate information list setup- includes needed html for formatting ###
    # List setup #
    degree0 = [] # Initializelows list
    # - #

    # Header/ MISC Info #
    degree0.append('<table align="center" border="0" cellpadding="1" cellspacing="1" style="width: 750px;">'+ '\n' +
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

    # Number of 0 degree days so far this year #
    # CVG
    degree0.append('<tr>'+ '\n' +
			'<td bgcolor="#424949" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">' +
                        str(data_0_cy_final[0][0]) +' Total<br />'+ '\n' +
			'</p></td>'+ '\n' +
			'<td bgcolor="#CCD1D1" style="vertical-align: middle" align="center" colspan="3"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">' +
                        str(data_0_cy_final[0][1]) + '<br />'+ '\n' +
			'</p></td>'+ '\n' +
                        '</tr>')
    
    # Normal per year #
    # CVG
    normal0_per_year = str(data_0_avg)
    degree0.append('<tr>'+ '\n' +
			'<td bgcolor="#1F618D" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Normal Per Year<br />'+ '\n' +
			'</p></td>'+ '\n' +
			'<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="3"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    degree0.append(normal0_per_year)
    degree0.append('<br />'+ '\n' +
			'</p></td>'+ '\n' +
                        '</tr>'+ '\n')
    
    # Earliest in a year #  
    # CVG
    earliest0 = str(data_0_earliest_final)
    degree0.append('<tr>'+ '\n' +
                        '<td bgcolor="#1F618D" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Earliest<br />'+ '\n' +
      			'</p></td>'+ '\n' +
                        '<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="2"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    degree0.append(earliest0)
    degree0.append('<br />'+ '\n' +
      			'</p></td>'+ '\n' +
                        '</tr>'+ '\n')
    
    # Latest in a year #    
    # CVG
    latest0 = str(data_0_last_final)
    degree0.append('<tr>'+ '\n' +
			'<td bgcolor="#1F618D" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Latest<br />'+ '\n' +
                	'</p></td>'+ '\n' +
                        '<td bgcolor="#7FB3D5" style="vertical-align: middle" align="center" colspan="2"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    degree0.append(latest0)
    degree0.append('<br />'+ '\n' +
                        '</p></td>'+ '\n' +
                        '</tr>'+ '\n') 
    
    # Most 0 degree days November #
    month_totals_nov = str(month_totals[0])
    month_totals_novyr_final = month_totals_nov[4:11].strip("' ,")
    month_totals_novnum_final = month_totals_nov[12:21].strip("u ' ) ")
    degree0.append('<tr>'+ '\n' +
                        '<td bgcolor="#884EA0" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Most Subzero Lows in November<br />'+ '\n' +
                	'</p></td>'+ '\n' +
                    	'<td bgcolor="#C39BD3" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    degree0.append(month_totals_novyr_final)
    degree0.append('<br />'+'</p></td>'+ '<td bgcolor="#C39BD3" style="vertical-align: middle" align="center" colspan="2"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    degree0.append(month_totals_novnum_final)
    degree0.append('<br />'+ '\n' +
                        '</p></td>'+ '\n' +
                        '</tr>'+ '\n')
    
    # Most 0 degree days December #
    # CVG
    month_totals_dec = str(month_totals[1])
    month_totals_decyr_final = month_totals_dec[4:11].strip("' ,")
    month_totals_decnum_final = month_totals_dec[12:21].strip("u ' ) ")
    degree0.append('<tr>'+ '\n' +
                        '<td bgcolor="#884EA0" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Most Subzero Lows in December<br />'+ '\n' +
                	'</p></td>'+ '\n' +
                    	'<td bgcolor="#C39BD3" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    degree0.append(month_totals_decyr_final)
    degree0.append('<br />'+'</p></td>'+ '<td bgcolor="#C39BD3" style="vertical-align: middle" align="center" colspan="2"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    degree0.append(month_totals_decnum_final)
    degree0.append('<br />'+ '\n' +
                        '</p></td>'+ '\n' +
                        '</tr>'+ '\n') 
    
    # Most 0 degree days January #
    # CVG
    month_totals_jan = str(month_totals[2])
    month_totals_janyr_final = month_totals_jan[4:11].strip("' ,")
    month_totals_jannum_final = month_totals_jan[12:21].strip("u ' ) ")
    degree0.append('<tr>'+ '\n' +
                        '<td bgcolor="#884EA0" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Most Subzero Lows in January<br />'+ '\n' +
                	'</p></td>'+ '\n' +
                    	'<td bgcolor="#C39BD3" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    degree0.append(month_totals_janyr_final)
    degree0.append('<br />'+'</p></td>'+ '<td bgcolor="#C39BD3" style="vertical-align: middle" align="center" colspan="2"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    degree0.append(month_totals_jannum_final)
    degree0.append('<br />'+ '\n' +
                        '</p></td>'+ '\n' +
                        '</tr>'+ '\n')
    
    # Most 0 degree days February #
    # CVG
    month_totals_feb = str(month_totals[3])
    month_totals_febyr_final = month_totals_feb[4:11].strip("' ,")
    month_totals_febnum_final = month_totals_feb[12:21].strip("u ' ) ")
    degree0.append('<tr>'+ '\n' +
                        '<td bgcolor="#884EA0" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Most Subzero Lows in February<br />'+ '\n' +
                	'</p></td>'+ '\n' +
                    	'<td bgcolor="#C39BD3" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    degree0.append(month_totals_febyr_final)
    degree0.append('<br />'+'</p></td>'+ '<td bgcolor="#C39BD3" style="vertical-align: middle" align="center" colspan="2"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    degree0.append(month_totals_febnum_final)
    degree0.append('<br />'+ '\n' +
                        '</p></td>'+ '\n' +
                        '</tr>'+ '\n') 

    # Most 0 degree days March #
    # CVG
    month_totals_mar = str(month_totals[4])
    month_totals_maryr_final = month_totals_mar[4:11].strip("' ,")
    month_totals_marnum_final = month_totals_mar[12:21].strip("u ' ) ")
    degree0.append('<tr>'+ '\n' +
                        '<td bgcolor="#884EA0" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Most Subzero Lows in March<br />'+ '\n' +
                	'</p></td>'+ '\n' +
                    	'<td bgcolor="#C39BD3" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    degree0.append(month_totals_maryr_final)
    degree0.append('<br />'+'</p></td>'+ '<td bgcolor="#C39BD3" style="vertical-align: middle" align="center" colspan="2"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    degree0.append(month_totals_marnum_final)
    degree0.append('<br />'+ '\n' +
                        '</p></td>'+ '\n' +
                        '</tr>'+ '\n') 
    
    
    # Most 0 degree day highs November #
    # CVG
    month_high_totals_nov = str(month_high_totals[0])
    month_high_totals_novyr_final = month_high_totals_nov[4:11].strip("' ,")
    month_high_totals_novnum_final = month_high_totals_nov[12:21].strip("u ' ) ")
    degree0.append('<tr>'+ '\n' +
                        '<td bgcolor="#884EA0" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Most Subzero Highs in November<br />'+ '\n' +
                	'</p></td>'+ '\n' +
                    	'<td bgcolor="#C39BD3" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    degree0.append(month_high_totals_novyr_final)
    degree0.append('<br />'+'</p></td>'+ '<td bgcolor="#C39BD3" style="vertical-align: middle" align="center" colspan="2"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    degree0.append(month_high_totals_novnum_final)
    degree0.append('<br />'+ '\n' +
                        '</p></td>'+ '\n' +
                        '</tr>'+ '\n') 
    
    # Most 0 degree day highs December #
    # CVG
    month_high_totals_dec = str(month_high_totals[1])
    month_high_totals_decyr_final = month_high_totals_dec[4:11].strip("' ,")
    month_high_totals_decnum_final = month_high_totals_dec[12:21].strip("u ' ) ")
    degree0.append('<tr>'+ '\n' +
                        '<td bgcolor="#884EA0" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Most Subzero Highs in December<br />'+ '\n' +
                	'</p></td>'+ '\n' +
                    	'<td bgcolor="#C39BD3" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    degree0.append(month_high_totals_decyr_final)
    degree0.append('<br />'+'</p></td>'+ '<td bgcolor="#C39BD3" style="vertical-align: middle" align="center" colspan="2"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    degree0.append(month_high_totals_decnum_final)
    degree0.append('<br />'+ '\n' +
                        '</p></td>'+ '\n' +
                        '</tr>'+ '\n') 
    
    # Most 0 degree day highs January #
    # CVG
    month_high_totals_jan = str(month_high_totals[2])
    month_high_totals_janyr_final = month_high_totals_jan[4:11].strip("' ,")
    month_high_totals_jannum_final = month_high_totals_jan[12:21].strip("u ' ) ")
    degree0.append('<tr>'+ '\n' +
                        '<td bgcolor="#884EA0" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Most Subzero Highs in January<br />'+ '\n' +
                	'</p></td>'+ '\n' +
                    	'<td bgcolor="#C39BD3" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    degree0.append(month_high_totals_janyr_final)
    degree0.append('<br />'+'</p></td>'+ '<td bgcolor="#C39BD3" style="vertical-align: middle" align="center" colspan="2"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    degree0.append(month_high_totals_jannum_final)
    degree0.append('<br />'+ '\n' +
                        '</p></td>'+ '\n' +
                        '</tr>'+ '\n') 
    
    # Most 0 degree day highs February #
    # CVG
    month_high_totals_feb = str(month_high_totals[3])
    month_high_totals_febyr_final = month_high_totals_feb[4:11].strip("' ,")
    month_high_totals_febnum_final = month_high_totals_feb[12:21].strip("u ' ) ")
    degree0.append('<tr>'+ '\n' +
                        '<td bgcolor="#884EA0" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Most Subzero Highs in February<br />'+ '\n' +
                	'</p></td>'+ '\n' +
                    	'<td bgcolor="#C39BD3" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    degree0.append(month_high_totals_febyr_final)
    degree0.append('<br />'+'</p></td>'+ '<td bgcolor="#C39BD3" style="vertical-align: middle" align="center" colspan="2"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    degree0.append(month_high_totals_febnum_final)
    degree0.append('<br />'+ '\n' +
                        '</p></td>'+ '\n' +
                        '</tr>'+ '\n')
    
    # Most 0 degree day highs March #
    # CVG
    month_high_totals_mar = str(month_high_totals[4])
    month_high_totals_maryr_final = month_high_totals_mar[4:11].strip("' ,")
    month_high_totals_marnum_final = month_high_totals_mar[12:21].strip("u ' ) ")
    degree0.append('<tr>'+ '\n' +
                        '<td bgcolor="#884EA0" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Most Subzero Highs in March<br />'+ '\n' +
                	'</p></td>'+ '\n' +
                    	'<td bgcolor="#C39BD3" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    degree0.append(month_high_totals_maryr_final)
    degree0.append('<br />'+'</p></td>'+ '<td bgcolor="#C39BD3" style="vertical-align: middle" align="center" colspan="2"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
    degree0.append(month_high_totals_marnum_final)
    degree0.append('<br />'+ '\n' +
                        '</p></td>'+ '\n' +
                        '</tr>'+ '\n') 
    
    # Most 0 degree day lows in a year #
    # CVG
    most0_per_year = (data_0_most_final)
    for j in range(len(most0_per_year)):
        degree0.append('<tr>'+ '\n')
        if j == 0:
            if (len(most0_per_year)) > 1:
                degree0.append('<td bgcolor="#2E86C1" style="vertical-align: middle" align="center" rowspan="' + str(len(most0_per_year)) + '" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Most Subzero Lows In A Year<br />'+ '\n' +
                                    '</p></td>'+ '\n')
            else:
                degree0.append('<td bgcolor="#2E86C1" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Most Subzero Lows In A Year<br />'+ '\n' +
                                    '</p></td>'+ '\n')
            degree0.append('<td bgcolor="#85C1E9" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
            degree0.append((most0_per_year[j][0]).decode("utf-8"))
            degree0.append('<br />'+ '\n' +
                                '</p></td>'+ '\n' +
                                '<td bgcolor="#85C1E9" style="vertical-align: middle" align="center" colspan="2"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
            degree0.append(str(most0_per_year[j][1]))
            degree0.append('<br />'+ '\n'
                                '</p></td>'+ '\n')	
        if j > 0:
            degree0.append('<td bgcolor="#85C1E9" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
            degree0.append((most0_per_year[j][0]).decode("utf-8"))
            degree0.append('<br />'+ '\n' +
                                '</p></td>'+ '\n' +
                                '<td bgcolor="#85C1E9" style="vertical-align: middle" align="center" colspan="2"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
            degree0.append(str(most0_per_year[j][1]))
            degree0.append('<br />'+ '\n'
                                '</p></td>'+ '\n')			
    degree0.append('</tr>'+ '\n')
    
    # Most 0 degree day highs in a year #
    # CVG
    most0_max_per_year = (data_0_max_most_final)
    for j in range(len(most0_max_per_year)):
        degree0.append('<tr>'+ '\n')
        if j == 0:
            if (len(most0_max_per_year)) > 1:
                degree0.append('<td bgcolor="#2E86C1" style="vertical-align: middle" align="center" rowspan="' + str(len(most0_max_per_year)) + '" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Most Subzero Highs In A Year<br />'+ '\n' +
                                    '</p></td>'+ '\n')
            else:
                degree0.append('<td bgcolor="#2E86C1" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Most Subzero Highs In A Year<br />'+ '\n' +
                                    '</p></td>'+ '\n')
            degree0.append('<td bgcolor="#85C1E9" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
            degree0.append((most0_max_per_year[j][0]).decode("utf-8"))
            degree0.append('<br />'+ '\n' +
                                '</p></td>'+ '\n' +
                                '<td bgcolor="#85C1E9" style="vertical-align: middle" align="center" colspan="2"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
            degree0.append(str(most0_max_per_year[j][1]))
            degree0.append('<br />'+ '\n'
                                '</p></td>'+ '\n')	
        if j > 0:
            degree0.append('<td bgcolor="#85C1E9" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
            degree0.append((most0_max_per_year[j][0]).decode("utf-8"))
            degree0.append('<br />'+ '\n' +
                                '</p></td>'+ '\n' +
                                '<td bgcolor="#85C1E9" style="vertical-align: middle" align="center" colspan="2"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
            degree0.append(str(most0_max_per_year[j][1]))
            degree0.append('<br />'+ '\n'
                                '</p></td>'+ '\n')			
    degree0.append('</tr>'+ '\n')
    
    # Longest stretch
    # CVG
    longest0 = (data_0_stretch_order_final)
    for j in range(len(longest0)):
        degree0.append('<tr>'+ '\n')
        if j == 0:
            if (len(longest0)) > 1:
                degree0.append('<td bgcolor="#2E86C1" style="vertical-align: middle" align="center" rowspan="' + str(len(longest0)) + '" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Longest Stretch of Subzero Lows (End Date)<br />'+ '\n' +
                                    '</p></td>'+ '\n')
            else:
                degree0.append('<td bgcolor="#2E86C1" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Longest Stretch of Subzero Lows (End Date)<br />'+ '\n' +
                                    '</p></td>'+ '\n')
            degree0.append('<td bgcolor="#85C1E9" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
            degree0.append((longest0[j][0]).decode("utf-8"))
            degree0.append('<br />'+ '\n' +
                                '</p></td>'+ '\n' +
                                '<td bgcolor="#85C1E9" style="vertical-align: middle" align="center" colspan="2"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
            degree0.append(str(longest0[j][1]))
            degree0.append('<br />'+ '\n'
                                '</p></td>'+ '\n')	
        if j > 0:
            degree0.append('<td bgcolor="#85C1E9" style="vertical-align: middle" align="center" colspan="1"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
            degree0.append((longest0[j][0]).decode("utf-8"))
            degree0.append('<br />'+ '\n' +
                                '</p></td>'+ '\n' +
                                '<td bgcolor="#85C1E9" style="vertical-align: middle" align="center" colspan="2"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">')
            degree0.append(str(longest0[j][1]))
            degree0.append('<br />'+ '\n'
                                '</p></td>'+ '\n')			
    degree0.append('</tr>'+ '\n')  
    
    # Add other static text (period of record/ normal)
    # CVG
    degree0.append('<tr>'+ '\n' +
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
    final_0degree = open(output_file,"w+") # Open file for writing
    
    # For loop to write out files- CVG #
    for j in range(len(degree0)):
        text = degree0[j]
        final_0degree.write(text)
    # - #
    
    ### Step 4: Close all the open files and generate pdf files ###
    final_0degree.close()

    # Create pdf files #
    print(' Now creating pdf files')
    pdfkit.from_file('../../PDFTxtFiles/0degree/0degree_'+site+'.html', '../../PDFTxtFiles/0degree/0degree_'+site+'.pdf')
    print(' Script completed and files genereated... ')
    # - #
    
    # Close Connection
    cursor.close()
    cnx.close()

### --- ###

for site in sites:
    htmlSite(site)
    