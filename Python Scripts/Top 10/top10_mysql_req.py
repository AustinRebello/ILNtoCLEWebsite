### HEADER ###
# Name: Brian Haines
# Date: 8/11/2015
# Purpose: Create a script that requests mysql data and generates html file
# Version/ update history:
#    1) 08-08-15: Script completed!
#    2) 01-22-17: Script updated to incorporate Kristens new design changes
#    3) 02-27-18: Added code for least snowiest months and sort by year (newest to oldest)
### --- ###

### Import needed modules ###
import mysql.connector
import datetime
import time
import datetime
#import pdfkit
### --- ###

### Defined Constants ###
# My SQL #
cnx = mysql.connector.connect(user='austinrebello', password='mysql',
                              host='localhost',
                              database='climate') 
cursor = cnx.cursor(buffered=True)
# Other #
current_month = datetime.datetime.now().strftime("%B") # Display the current month in words
current_year = (time.strftime("%Y")) # Display the current year
current_date = (time.strftime("%Y-%m-%d"))
month = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'] #Used for Title in HTML
month_nm = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sept', 'oct', 'nov', 'dec'] #Naming html file
sites_cap = ['CMH', 'CVG', 'DAY']
sites_low = ['cmh', 'cvg', 'day']
### --- ###

### Main Code ###
for i in range(0,len(month)): # Main for loop to go through and create all data for each month
  ## Intialize python lists to hold data ##
  #CVG
  cvg_top10 = [] # Initialize day_top10 list that holds all of the data from mysql
  cvg_top10.append([]) # Add a dimension to the list
  #CMH
  cmh_top10 = [] # Initialize da_top10 list that holds all of the data from mysql
  cmh_top10.append([]) # Add a dimension to the list
  #DAY
  day_top10 = [] # Initialize day_top10 list that holds all of the data from mysql
  day_top10.append([]) # Add a dimension to the list
  ## -- ##
  
  ## Output File List ###
  output_file_cvg = 'X:/Users/brian.haines/Projects/ClimateWebpage/PDFTxtFiles/Top10/CVG/climate_top10_cvg_' + month_nm[i] + '.html'
  output_file_cmh = 'X:/Users/brian.haines/Projects/ClimateWebpage/PDFTxtFiles/Top10/CMH/climate_top10_cmh_' + month_nm[i] + '.html'
  output_file_day = 'X:/Users/brian.haines/Projects/ClimateWebpage/PDFTxtFiles/Top10/DAY/climate_top10_day_' + month_nm[i] + '.html'
  ## -- ##

  Header_Warm_CVG = ('<style>' + '\n' + 'body {' + '\n' + 'text-align:center;' + '\n' + '}' + '\n' + '</style>'+ '\n' +
                        '<table align="center" border="0" cellpadding="1" cellspacing="1" style="width: 80%;">'+ '\n' +
                        '<tbody>'+ '\n' +
                        '<tr>'+ '\n' +
			'<td style="vertical-align: middle" align="center" colspan="3">' + '\n' +
                        '<p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">' + '\n' + 
                        'Last Update: ' + current_date + '\n' +
			'</p>'+ '\n' +
                        '</td>'+ '\n' +
                        '</tr>'+ '\n' +
                        '</tbody>'+ '\n' +
                        '</table>'+ '\n' +
                        '<br />'+ '\n' +
                        '<table width="80%" cellpadding="3" align="center">' + '\n' + '<tr bgcolor="#000000">' + '\n' +
                        '<td colspan="2">' + '\n' +
                        '<p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">'+ '\n' +
                        'Cincinnati ' + month[i] + ' Top 10 Lists' + ' (1872 - ' + current_year + ') ' + '</p></td>' + '\n' +
                        '</tr>' + '\n' +
                        '</table>' + '\n' +
                        '<br />'+ '\n' +
                        '<table cellspacing="0" cellpadding="3" border="1" align = "center" style="display:inline-block;margin:1em;">' + '\n' +
                        '<tbody>' + '\n'+
                        '<tr align="center">' + '\n' +
                        '<td colspan="2">' + '\n' +
                        '<p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">'+ '\n' +
                        'Top 10<br />Warmest</p></td>'  + '\n' +
                        '</tr>' +'\n'+
                        '<tr>' +'\n'+
			'<td bgcolor="#424949" style="vertical-align: middle;" align="center" colspan="1">' +'\n'+
                        '<p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">' + '\n' +
                        'Rank <br />' +'\n'+
			'</p>' +'\n'+
                        '</td>' +'\n'+
			'<td bgcolor="#424949" style="vertical-align: middle" align="center" colspan="1">' +'\n'+
                        '<p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">' + '\n' +
                        'Value/Yr<br />' +'\n'+
			'</p>' + '\n'+
                        '</td>' +'\n'+
		        '</tr>' +'\n')
  
  Header_Warm_CMH = ('<style>' + '\n' + 'body {' + '\n' + 'text-align:center;' + '\n' + '}' + '\n' + '</style>'+ '\n' +
                        '<table align="center" border="0" cellpadding="1" cellspacing="1" style="width: 80%;">'+ '\n' +
                        '<tbody>'+ '\n' +
                        '<tr>'+ '\n' +
			'<td style="vertical-align: middle" align="center" colspan="3">' + '\n' +
                        '<p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">' + '\n' + 
                        'Last Update: ' + current_date + '\n' +
			'</p>'+ '\n' +
                        '</td>'+ '\n' +
                        '</tr>'+ '\n' +
                        '</tbody>'+ '\n' +
                        '</table>'+ '\n' +
                        '<br />'+ '\n' +
                        '<table width="80%" cellpadding="3" align="center">' + '\n' + '<tr bgcolor="#000000">' + '\n' +
                        '<td colspan="2">' + '\n' +
                        '<p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">'+ '\n' +
                        'Columbus ' + month[i] + ' Top 10 Lists' + ' (1878 - ' + current_year + ') ' + '</p></td>' + '\n' +
                        '</tr>' + '\n' +
                        '</table>' + '\n' +
                        '<br />'+ '\n' +
                        '<table cellspacing="0" cellpadding="3" border="1" align = "center" style="display:inline-block;margin:1em;">' + '\n' +
                        '<tbody>' + '\n'+
                        '<tr align="center">' + '\n' +
                        '<td colspan="2">' + '\n' +
                        '<p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">'+ '\n' +
                        'Top 10<br />Warmest</p></td>'  + '\n' +
                        '</tr>' +'\n'+
                        '<tr>' +'\n'+
			'<td bgcolor="#424949" style="vertical-align: middle;" align="center" colspan="1">' +'\n'+
                        '<p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">' + '\n' +
                        'Rank <br />' +'\n'+
			'</p>' +'\n'+
                        '</td>' +'\n'+
			'<td bgcolor="#424949" style="vertical-align: middle" align="center" colspan="1">' +'\n'+
                        '<p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">' + '\n' +
                        'Value/Yr<br />' +'\n'+
			'</p>' + '\n'+
                        '</td>' +'\n'+
		        '</tr>' +'\n')

  Header_Warm_DAY = ('<style>' + '\n' + 'body {' + '\n' + 'text-align:center;' + '\n' + '}' + '\n' + '</style>'+ '\n' +
                        '<table align="center" border="0" cellpadding="1" cellspacing="1" style="width: 80%;">'+ '\n' +
                        '<tbody>'+ '\n' +
                        '<tr>'+ '\n' +
			'<td style="vertical-align: middle" align="center" colspan="3">' + '\n' +
                        '<p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">' + '\n' + 
                        'Last Update: ' + current_date + '\n' +
			'</p>'+ '\n' +
                        '</td>'+ '\n' +
                        '</tr>'+ '\n' +
                        '</tbody>'+ '\n' +
                        '</table>'+ '\n' +
                        '<br />'+ '\n' +
                        '<table width="80%" cellpadding="3" align="center">' + '\n' + '<tr bgcolor="#000000">' + '\n' +
                        '<td colspan="2">' + '\n' +
                        '<p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">'+ '\n' +
                        'Dayton ' + month[i] + ' Top 10 Lists' + ' (1893 - ' + current_year + ') ' + '</p></td>' + '\n' +
                        '</tr>' + '\n' +
                        '</table>' + '\n' +
                        '<br />'+ '\n' +
                        '<table cellspacing="0" cellpadding="3" border="1" align = "center" style="display:inline-block;margin:1em;">' + '\n' +
                        '<tbody>' + '\n'+
                        '<tr align="center">' + '\n' +
                        '<td colspan="2">' + '\n' +
                        '<p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">'+ '\n' +
                        'Top 10<br />Warmest</p></td>'  + '\n' +
                        '</tr>' +'\n'+
                        '<tr>' +'\n'+
			'<td bgcolor="#424949" style="vertical-align: middle;" align="center" colspan="1">' +'\n'+
                        '<p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">' + '\n' +
                        'Rank <br />' +'\n'+
			'</p>' +'\n'+
                        '</td>' +'\n'+
			'<td bgcolor="#424949" style="vertical-align: middle" align="center" colspan="1">' +'\n'+
                        '<p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">' + '\n' +
                        'Value/Yr<br />' +'\n'+
			'</p>' + '\n'+
                        '</td>' +'\n'+
		        '</tr>' +'\n')

  Header_Cold = ('<table align="center" border="1" cellpadding="3" cellspacing="0" class="images" style="display:inline-block;margin:1em;">' + '\n' +
                         '<tbody>' + '\n'+
                         '<tr>' + '\n' + '<td colspan="2">'+ '\n' +
                         '<p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">'+ '\n' +
                         'Top 10<br />Coldest</p></td>'  + '\n' +
                         '</tr>' +'\n'+
                	 '<tr>' +'\n'+
			 '<td bgcolor="#424949" style="vertical-align: middle;" align="center" colspan="1">' +'\n'+
                         '<p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Rank<br />' +'\n'+
			 '</p>' +'\n'+
                         '</td>' +'\n'+
			 '<td bgcolor="#424949" style="vertical-align: middle" align="center" colspan="1">' +'\n'+
                         '<p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Value/Yr<br />' +'\n'+
			 '</p>' +'\n'+
                         '</td>' +'\n'+
		         '</tr>' +'\n')

  Header_Wet = ('<table align="center" border="1" cellpadding="3" cellspacing="0" class="images" style="display:inline-block;margin:1em;">' + '\n' +
                         '<tbody>' + '\n'+
                         '<tr>' + '\n' + '<td colspan="2">'+ '\n' +
                         '<p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">'+ '\n' +
                         'Top 10<br />Wettest</p></td>'  + '\n' +
                         '</tr>' +'\n'+
                	 '<tr>' +'\n'+
			 '<td bgcolor="#424949" style="vertical-align: middle;" align="center" colspan="1">' +'\n'+
                         '<p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Rank<br />' +'\n'+
			 '</p>' +'\n'+
                         '</td>' +'\n'+
			 '<td bgcolor="#424949" style="vertical-align: middle" align="center" colspan="1">' +'\n'+
                         '<p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Value/Yr<br />' +'\n'+
			 '</p>' +'\n'+
                         '</td>' +'\n'+
		         '</tr>' +'\n')

  Header_Dry = ('<table align="center" border="1" cellpadding="3" cellspacing="0" class="images" style="display:inline-block;margin:1em;">' + '\n' +
                         '<tbody>' + '\n'+
                         '<tr>' + '\n' + '<td colspan="2">'+ '\n' +
                         '<p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">'+ '\n' +
                         'Top 10<br />Driest</p></td>'  + '\n' +
                         '</tr>' +'\n'+
                	 '<tr>' +'\n'+
			 '<td bgcolor="#424949" style="vertical-align: middle;" align="center" colspan="1">' +'\n'+
                         '<p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Rank<br />' +'\n'+
			 '</p>' +'\n'+
                         '</td>' +'\n'+
			 '<td bgcolor="#424949" style="vertical-align: middle" align="center" colspan="1">' +'\n'+
                         '<p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Value/Yr<br />' +'\n'+
			 '</p>' +'\n'+
                         '</td>' +'\n'+
		         '</tr>' +'\n')

  Header_Snow = ('<table align="center" border="1" cellpadding="3" cellspacing="0" class="images" style="display:inline-block;margin:1em;">' + '\n' +
                         '<tbody>' + '\n'+
                         '<tr>' + '\n' + '<td colspan="2">'+ '\n' +
                         '<p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">'+ '\n' +
                         'Top 10<br />Snowiest</p></td>'  + '\n' +
                         '</tr>' +'\n'+
                	 '<tr>' +'\n'+
			 '<td bgcolor="#424949" style="vertical-align: middle;" align="center" colspan="1">' +'\n'+
                         '<p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Rank<br />' +'\n'+
			 '</p>' +'\n'+
                         '</td>' +'\n'+
			 '<td bgcolor="#424949" style="vertical-align: middle" align="center" colspan="1">' +'\n'+
                         '<p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Value/Yr<br />' +'\n'+
			 '</p>' +'\n'+
                         '</td>' +'\n'+
		         '</tr>' +'\n')
  Header_LeastSnow = ('<table align="center" border="1" cellpadding="3" cellspacing="0" class="images" style="display:inline-block;margin:1em;">' + '\n' +
                         '<tbody>' + '\n'+
                         '<tr>' + '\n' + '<td colspan="2">'+ '\n' +
                         '<p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">'+ '\n' +
                         'Top 10<br />Least Snowiest</p></td>'  + '\n' +
                         '</tr>' +'\n'+
                	 '<tr>' +'\n'+
			 '<td bgcolor="#424949" style="vertical-align: middle;" align="center" colspan="1">' +'\n'+
                         '<p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Rank<br />' +'\n'+
			 '</p>' +'\n'+
                         '</td>' +'\n'+
			 '<td bgcolor="#424949" style="vertical-align: middle" align="center" colspan="1">' +'\n'+
                         '<p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Value/Yr<br />' +'\n'+
			 '</p>' +'\n'+
                         '</td>' +'\n'+
		         '</tr>' +'\n')

  Footer = ('</tbody></table>' + '\n')


  ## Get Top 10 warmest ##
  #CVG
  query_cvg = ("SELECT Year, Month, Monthly_Temp_Avg FROM climate.kcvg_monthly where Month = " + str(i+1) + " AND Monthly_Temp_Avg != 'M' ORDER BY Monthly_Temp_Avg+0 DESC, Year DESC;")
  cursor.execute(query_cvg)
  row_cvg = cursor.fetchone()
  cvg_top10[0].append(Header_Warm_CVG)
  color_cvg_num = []
  color_cvg_value = []
  color_cvg_num = ["#A51B13","#AF231A","#B82D24","#C4372E","#CF4239","#D94E45","#E0564D","#E86057","#F06A61","#F7736A"]
  color_cvg_value = ["#FCB1AB","#FDBDB7","#FDC5C0","#FECECA","#FDD5D1","#FEDCD8","#FEE2DE","#FEE9E5","#FDEEEC","#FDF5F4"]

  for dcv in range(0,10):
    #print(row_cvg)
    year_cvg = str(row_cvg[0])
    temp_cvg = str(row_cvg[2])
    cvg_top10[0].append('<tr>' + '\n' +
                        '<td bgcolor=' + color_cvg_num[dcv] + ' style="vertical-align: middle" align="center" colspan="1">' + '\n' +
                        '<p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">' + str(dcv+1) + '<br />' +'\n'+
			'</p></td>')
    cvg_top10[0].append('<td bgcolor=' + color_cvg_value[dcv] + ' style="vertical-align: middle" align="center" colspan="1">'
                        '<p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;" >' + temp_cvg + '| ' + year_cvg + '<br />' +'\n'+
                        '</p></td></tr>' + '\n')
    row_cvg = cursor.fetchone()    
  cvg_top10[0].append(Footer)

  #CMH
  query_cmh = ("SELECT Year, Month, Monthly_Temp_Avg FROM climate.kcmh_monthly where Month = " + str(i+1) + " AND Monthly_Temp_Avg != 'M' ORDER BY Monthly_Temp_Avg+0 DESC, Year DESC;")
  cursor.execute(query_cmh)
  row_cmh = cursor.fetchone()
  cmh_top10[0].append(Header_Warm_CMH)
  color_cmh_num = []
  color_cmh_value = []
  color_cmh_num = ["#A51B13","#AF231A","#B82D24","#C4372E","#CF4239","#D94E45","#E0564D","#E86057","#F06A61","#F7736A"]
  color_cmh_value = ["#FCB1AB","#FDBDB7","#FDC5C0","#FECECA","#FDD5D1","#FEDCD8","#FEE2DE","#FEE9E5","#FDEEEC","#FDF5F4"]
    
  for dcm in range(0,10):
    #print(row_cmh)
    year_cmh = str(row_cmh[0])
    temp_cmh = str(row_cmh[2])
    cmh_top10[0].append('<tr>' + '\n' +
                        '<td bgcolor=' + color_cmh_num[dcm] + ' style="vertical-align: middle" align="center" colspan="1">' + '\n' +
                        '<p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">' + str(dcm+1) + '<br />' +'\n'+
			'</p></td>')
    cmh_top10[0].append('<td bgcolor=' + color_cmh_value[dcm] + ' style="vertical-align: middle" align="center" colspan="1">'
                        '<p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;" >' + temp_cmh + '| ' + year_cmh + '<br />' +'\n'+
                        '</p></td></tr>' + '\n')
    row_cmh = cursor.fetchone()    
  cmh_top10[0].append(Footer)

  #DAY
  query_day = ("SELECT Year, Month, Monthly_Temp_Avg FROM climate.kday_monthly where Month = " + str(i+1) + " AND Monthly_Temp_Avg != 'M' ORDER BY Monthly_Temp_Avg+0 DESC, Year DESC;")
  cursor.execute(query_day)
  row_day = cursor.fetchone()
  day_top10[0].append(Header_Warm_DAY)
  color_day_num = []
  color_day_value = []
  color_day_num = ["#A51B13","#AF231A","#B82D24","#C4372E","#CF4239","#D94E45","#E0564D","#E86057","#F06A61","#F7736A"]
  color_day_value = ["#FCB1AB","#FDBDB7","#FDC5C0","#FECECA","#FDD5D1","#FEDCD8","#FEE2DE","#FEE9E5","#FDEEEC","#FDF5F4"]
    
  for dd in range(0,10):
    #print(row_day)
    year_day = str(row_day[0])
    temp_day = str(row_day[2])
    day_top10[0].append('<tr>' + '\n' +
                        '<td bgcolor=' + color_day_num[dd] + ' style="vertical-align: middle" align="center" colspan="1">' + '\n' +
                        '<p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">' + str(dd+1) + '<br />' +'\n'+
			'</p></td>')
    day_top10[0].append('<td bgcolor=' + color_day_value[dd] + ' style="vertical-align: middle" align="center" colspan="1">'
                        '<p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;" >' + temp_day + '| ' + year_day + '<br />' +'\n'+
                        '</p></td></tr>' + '\n')
    row_day = cursor.fetchone()    
  day_top10[0].append(Footer)


  ## Get Top 10 coldest ##
  #CVG
  query_cvg = ("SELECT Year, Month, Monthly_Temp_Avg FROM climate.kcvg_monthly where Month = " + str(i+1) + " AND Monthly_Temp_Avg != 'M' ORDER BY Monthly_Temp_Avg+0, Year DESC;")
  cursor.execute(query_cvg)
  row_cvg = cursor.fetchone()
  cvg_top10[0].append(Header_Cold)
  color_cvg_num = []
  color_cvg_value = []
  color_cvg_num = ["#3239C2","#3C43CA","#454CD1","#4E55D6","#555CDA","#6066DF","#6A70E5","#747AE9","#8187EF","#9095F5"]
  color_cvg_value = ["#9FA3FC","#A6AAFE","#ADB0FF","#B3B6FD","#BBBEFE","#C3C6FE","#C9CCFE","#D1D3FE","#D8DAFE","#E0E2FE"]

  for dcv in range(0,10):
    #print(row_cvg)
    year_cvg = str(row_cvg[0])
    temp_cvg = str(row_cvg[2])
    cvg_top10[0].append('<tr>' + '\n' +
                        '<td bgcolor=' + color_cvg_num[dcv] + ' style="vertical-align: middle" align="center" colspan="1">' + '\n' +
                        '<p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">' + str(dcv) + '<br />' +'\n'+
			'</p></td>')
    cvg_top10[0].append('<td bgcolor=' + color_cvg_value[dcv] + ' style="vertical-align: middle" align="center" colspan="1">'
                        '<p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;" >' + temp_cvg + '| ' + year_cvg + '<br />' +'\n'+
                        '</p></td></tr>' + '\n')
    row_cvg = cursor.fetchone()    
  cvg_top10[0].append(Footer)

  #CMH
  query_cmh = ("SELECT Year, Month, Monthly_Temp_Avg FROM climate.kcmh_monthly where Month = " + str(i+1) + " AND Monthly_Temp_Avg != 'M' ORDER BY Monthly_Temp_Avg+0, Year DESC;")
  cursor.execute(query_cmh)
  row_cmh = cursor.fetchone()
  cmh_top10[0].append(Header_Cold)
  color_cmh_num = []
  color_cmh_value = []
  color_cmh_num = ["#3239C2","#3C43CA","#454CD1","#4E55D6","#555CDA","#6066DF","#6A70E5","#747AE9","#8187EF","#9095F5"]
  color_cmh_value = ["#9FA3FC","#A6AAFE","#ADB0FF","#B3B6FD","#BBBEFE","#C3C6FE","#C9CCFE","#D1D3FE","#D8DAFE","#E0E2FE"]
    
  for dcm in range(0,10):
    #print(row_cmh)
    year_cmh = str(row_cmh[0])
    temp_cmh = str(row_cmh[2])
    cmh_top10[0].append('<tr>' + '\n' +
                        '<td bgcolor=' + color_cmh_num[dcm] + ' style="vertical-align: middle" align="center" colspan="1">' + '\n' +
                        '<p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">' + str(dcm+1) + '<br />' +'\n'+
			'</p></td>')
    cmh_top10[0].append('<td bgcolor=' + color_cmh_value[dcm] + ' style="vertical-align: middle" align="center" colspan="1">'
                        '<p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;" >' + temp_cmh + '| ' + year_cmh + '<br />' +'\n'+
                        '</p></td></tr>' + '\n')
    row_cmh = cursor.fetchone()    
  cmh_top10[0].append(Footer)

  #DAY
  query_day = ("SELECT Year, Month, Monthly_Temp_Avg FROM climate.kday_monthly where Month = " + str(i+1) + " AND Monthly_Temp_Avg != 'M' ORDER BY Monthly_Temp_Avg+0, Year DESC;")
  cursor.execute(query_day)
  row_day = cursor.fetchone()
  day_top10[0].append(Header_Cold)
  color_day_num = []
  color_day_value = []
  color_day_num = ["#3239C2","#3C43CA","#454CD1","#4E55D6","#555CDA","#6066DF","#6A70E5","#747AE9","#8187EF","#9095F5"]
  color_day_value = ["#9FA3FC","#A6AAFE","#ADB0FF","#B3B6FD","#BBBEFE","#C3C6FE","#C9CCFE","#D1D3FE","#D8DAFE","#E0E2FE"]
    
  for dd in range(0,10):
    #print(row_day)
    year_day = str(row_day[0])
    temp_day = str(row_day[2])
    day_top10[0].append('<tr>' + '\n' +
                        '<td bgcolor=' + color_day_num[dd] + ' style="vertical-align: middle" align="center" colspan="1">' + '\n' +
                        '<p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">' + str(dd+1) + '<br />' +'\n'+
			'</p></td>')
    day_top10[0].append('<td bgcolor=' + color_day_value[dd] + ' style="vertical-align: middle" align="center" colspan="1">'
                        '<p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;" >' + temp_day + '| ' + year_day + '<br />' +'\n'+
                        '</p></td></tr>' + '\n')
    row_day = cursor.fetchone()    
  day_top10[0].append(Footer)


  ## Get Top 10 wettest ##
  #CVG
  query_cvg = ("SELECT Year, Month, Monthly_Precip_Total FROM climate.kcvg_monthly where Month = " + str(i+1) + " AND Monthly_Precip_Total != 'M' ORDER BY Monthly_Precip_Total+0 DESC, Year DESC;")
  cursor.execute(query_cvg)
  row_cvg = cursor.fetchone()
  cvg_top10[0].append(Header_Wet)
  color_cvg_num = []
  color_cvg_value = []
  color_cvg_num = ["#27AF17","#2EB71D","#35BD24","#3CC32B","#44CB33","#4BD13A","#52D641","#58DA48","#5FDF4F","#68E459"]
  color_cvg_value = ["#91FD84","#98FE8C","#9DFE91","#A2FE97","#AAFEA0","#B0FFA6","#B7FEAE","#BDFDB5","#C6FEBF","#CDFDC7"]

  for dcv in range(0,10):
    #print(row_cvg)
    year_cvg = str(row_cvg[0])
    temp_cvg = str(row_cvg[2])
    cvg_top10[0].append('<tr>' + '\n' +
                        '<td bgcolor=' + color_cvg_num[dcv] + ' style="vertical-align: middle" align="center" colspan="1">' + '\n' +
                        '<p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">' + str(dcv+1) + '<br />' +'\n'+
			'</p></td>')
    cvg_top10[0].append('<td bgcolor=' + color_cvg_value[dcv] + ' style="vertical-align: middle" align="center" colspan="1">'
                        '<p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;" >' + temp_cvg + '| ' + year_cvg + '<br />' +'\n'+
                        '</p></td></tr>' + '\n')
    row_cvg = cursor.fetchone()    
  cvg_top10[0].append(Footer)

  #CMH
  query_cmh = ("SELECT Year, Month, Monthly_Precip_Total FROM climate.kcmh_monthly where Month = " + str(i+1) + " AND Monthly_Precip_Total != 'M' ORDER BY Monthly_Precip_Total+0 DESC, Year DESC;")
  cursor.execute(query_cmh)
  row_cmh = cursor.fetchone()
  cmh_top10[0].append(Header_Wet)
  color_cmh_num = []
  color_cmh_value = []
  color_cmh_num = ["#27AF17","#2EB71D","#35BD24","#3CC32B","#44CB33","#4BD13A","#52D641","#58DA48","#5FDF4F","#68E459"]
  color_cmh_value = ["#91FD84","#98FE8C","#9DFE91","#A2FE97","#AAFEA0","#B0FFA6","#B7FEAE","#BDFDB5","#C6FEBF","#CDFDC7"]
    
  for dcm in range(0,10):
    #print(row_cmh)
    year_cmh = str(row_cmh[0])
    temp_cmh = str(row_cmh[2])
    cmh_top10[0].append('<tr>' + '\n' +
                        '<td bgcolor=' + color_cmh_num[dcm] + ' style="vertical-align: middle" align="center" colspan="1">' + '\n' +
                        '<p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">' + str(dcm+1) + '<br />' +'\n'+
			'</p></td>')
    cmh_top10[0].append('<td bgcolor=' + color_cmh_value[dcm] + ' style="vertical-align: middle" align="center" colspan="1">'
                        '<p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;" >' + temp_cmh + '| ' + year_cmh + '<br />' +'\n'+
                        '</p></td></tr>' + '\n')
    row_cmh = cursor.fetchone()    
  cmh_top10[0].append(Footer)  

  #DAY
  query_day = ("SELECT Year, Month, Monthly_Precip_Total FROM climate.kday_monthly where Month = " + str(i+1) + " AND Monthly_Precip_Total != 'M' ORDER BY Monthly_Precip_Total+0 DESC, Year DESC;")
  cursor.execute(query_day)
  row_day = cursor.fetchone()
  day_top10[0].append(Header_Wet)
  color_day_num = []
  color_day_value = []
  color_day_num = ["#27AF17","#2EB71D","#35BD24","#3CC32B","#44CB33","#4BD13A","#52D641","#58DA48","#5FDF4F","#68E459"]
  color_day_value = ["#91FD84","#98FE8C","#9DFE91","#A2FE97","#AAFEA0","#B0FFA6","#B7FEAE","#BDFDB5","#C6FEBF","#CDFDC7"]
    
  for dd in range(0,10):
    #print(row_day)
    year_day = str(row_day[0])
    temp_day = str(row_day[2])
    day_top10[0].append('<tr>' + '\n' +
                        '<td bgcolor=' + color_day_num[dd] + ' style="vertical-align: middle" align="center" colspan="1">' + '\n' +
                        '<p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">' + str(dd+1) + '<br />' +'\n'+
			'</p></td>')
    day_top10[0].append('<td bgcolor=' + color_day_value[dd] + ' style="vertical-align: middle" align="center" colspan="1">'
                        '<p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;" >' + temp_day + '| ' + year_day + '<br />' +'\n'+
                        '</p></td></tr>' + '\n')
    row_day = cursor.fetchone()    
  day_top10[0].append(Footer)


  ## Get Top 10 driest ##
  #CVG
  query_cvg = ("SELECT Year, Month, Monthly_Precip_Total FROM climate.kcvg_monthly where Month = " + str(i+1) + " AND Monthly_Precip_Total != 'M' ORDER BY Monthly_Precip_Total+0, Year DESC;")
  cursor.execute(query_cvg)
  row_cvg = cursor.fetchone()
  cvg_top10[0].append(Header_Dry)
  color_cvg_num = []
  color_cvg_value = []
  color_cvg_num = ["#BD9027","#C2952D","#C69A33","#CBA03A","#D1A641","#D8AD49","#DEB352","#E3B95A","#E8BF63","#EEC66D"]
  color_cvg_value = ["#FEDE96","#FEE09C","#FEE2A3","#FEE4AA","#FEE6B2","#FEE9B9","#FEEBBF","#FEEDC6","#FEEFCD","#FEF1D5"]

  for dcv in range(0,10):
    #print(row_cvg)
    year_cvg = str(row_cvg[0])
    temp_cvg = str(row_cvg[2])
    cvg_top10[0].append('<tr>' + '\n' +
                        '<td bgcolor=' + color_cvg_num[dcv] + ' style="vertical-align: middle" align="center" colspan="1">' + '\n' +
                        '<p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">' + str(dcv+1) + '<br />' +'\n'+
			'</p></td>')
    cvg_top10[0].append('<td bgcolor=' + color_cvg_value[dcv] + ' style="vertical-align: middle" align="center" colspan="1">'
                        '<p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;" >' + temp_cvg + '| ' + year_cvg + '<br />' +'\n'+
                        '</p></td></tr>' + '\n')
    row_cvg = cursor.fetchone()    
  cvg_top10[0].append(Footer)

  #CMH
  query_cmh = ("SELECT Year, Month, Monthly_Precip_Total FROM climate.kcmh_monthly where Month = " + str(i+1) + " AND Monthly_Precip_Total != 'M' ORDER BY Monthly_Precip_Total+0, Year DESC;")
  cursor.execute(query_cmh)
  row_cmh = cursor.fetchone()
  cmh_top10[0].append(Header_Dry)
  color_cmh_num = []
  color_cmh_value = []
  color_cmh_num = ["#BD9027","#C2952D","#C69A33","#CBA03A","#D1A641","#D8AD49","#DEB352","#E3B95A","#E8BF63","#EEC66D"]
  color_cmh_value = ["#FEDE96","#FEE09C","#FEE2A3","#FEE4AA","#FEE6B2","#FEE9B9","#FEEBBF","#FEEDC6","#FEEFCD","#FEF1D5"]
    
  for dcm in range(0,10):
    #print(row_cmh)
    year_cmh = str(row_cmh[0])
    temp_cmh = str(row_cmh[2])
    cmh_top10[0].append('<tr>' + '\n' +
                        '<td bgcolor=' + color_cmh_num[dcm] + ' style="vertical-align: middle" align="center" colspan="1">' + '\n' +
                        '<p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">' + str(dcm+1) + '<br />' +'\n'+
			'</p></td>')
    cmh_top10[0].append('<td bgcolor=' + color_cmh_value[dcm] + ' style="vertical-align: middle" align="center" colspan="1">'
                        '<p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;" >' + temp_cmh + '| ' + year_cmh + '<br />' +'\n'+
                        '</p></td></tr>' + '\n')
    row_cmh = cursor.fetchone()    
  cmh_top10[0].append(Footer)

  #DAY
  query_day = ("SELECT Year, Month, Monthly_Precip_Total FROM climate.kday_monthly where Month = " + str(i+1) + " AND Monthly_Precip_Total != 'M' ORDER BY Monthly_Precip_Total+0, Year DESC;")
  cursor.execute(query_day)
  row_day = cursor.fetchone()
  day_top10[0].append(Header_Dry)
  color_day_num = []
  color_day_value = []
  color_day_num = ["#BD9027","#C2952D","#C69A33","#CBA03A","#D1A641","#D8AD49","#DEB352","#E3B95A","#E8BF63","#EEC66D"]
  color_day_value = ["#FEDE96","#FEE09C","#FEE2A3","#FEE4AA","#FEE6B2","#FEE9B9","#FEEBBF","#FEEDC6","#FEEFCD","#FEF1D5"]
    
  for dd in range(0,10):
    #print(row_day)
    year_day = str(row_day[0])
    temp_day = str(row_day[2])
    day_top10[0].append('<tr>' + '\n' +
                        '<td bgcolor=' + color_day_num[dd] + ' style="vertical-align: middle" align="center" colspan="1">' + '\n' +
                        '<p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">' + str(dd+1) + '<br />' +'\n'+
			'</p></td>')
    day_top10[0].append('<td bgcolor=' + color_day_value[dd] + ' style="vertical-align: middle" align="center" colspan="1">'
                        '<p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;" >' + temp_day + '| ' + year_day + '<br />' +'\n'+
                        '</p></td></tr>' + '\n')
    row_day = cursor.fetchone()    
  day_top10[0].append(Footer)


  ## Get Top 10 snowiest ##
  #CVG
  query_cvg = ("SELECT Year, Month, Monthly_Snow_Total FROM climate.kcvg_monthly where Month = " + str(i+1) + " AND Monthly_Snow_Total != 'M' AND Monthly_Snow_Total != 'T' ORDER BY Monthly_Snow_Total+0 DESC, Year DESC;")
  cursor.execute(query_cvg)
  row_cvg = cursor.fetchone()
  cvg_top10[0].append(Header_Snow)
  color_cvg_num = []
  color_cvg_value = []
  color_cvg_num = ["#26A4B6","#2DABBD","#33B0C2","#3AB5C7","#40BBCD","#47C0D1","#50C7D8","#5ACFDF","#64D5E5","#6EDBEB"]
  color_cvg_value = ["#9CF1FE","#A7F3FE","#ADF4FE","#B4F5FE","#BAF5FE","#C2F6FE","#C8F7FE","#D0F9FF","#D8F9FE","#DEF8FC"]
    
  for dcv in range(0,10):
    #print(row_day)
    year_cvg = str(row_cvg[0])
    temp_cvg = str(row_cvg[2])
    cvg_top10[0].append('<tr>' + '\n' +
                        '<td bgcolor=' + color_cvg_num[dcv] + ' style="vertical-align: middle" align="center" colspan="1">' + '\n' +
                        '<p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">' + str(dcv+1) + '<br />' +'\n'+
			'</p></td>')
    cvg_top10[0].append('<td bgcolor=' + color_cvg_value[dcv] + ' style="vertical-align: middle" align="center" colspan="1">'
                        '<p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;" >' + temp_cvg + '| ' + year_cvg + '<br />' +'\n'+
                        '</p></td></tr>' + '\n')
    row_cvg = cursor.fetchone()    
  cvg_top10[0].append(Footer)

  #CMH
  query_cmh = ("SELECT Year, Month, Monthly_Snow_Total FROM climate.kcmh_monthly where Month = " + str(i+1) + " AND Monthly_Snow_Total != 'M' AND Monthly_Snow_Total != 'T' ORDER BY Monthly_Snow_Total+0 DESC, Year DESC;")
  cursor.execute(query_cmh)
  row_cmh = cursor.fetchone()
  cmh_top10[0].append(Header_Snow)
  color_cmh_num = []
  color_cmh_value = []
  color_cmh_num = ["#26A4B6","#2DABBD","#33B0C2","#3AB5C7","#40BBCD","#47C0D1","#50C7D8","#5ACFDF","#64D5E5","#6EDBEB"]
  color_cmh_value = ["#9CF1FE","#A7F3FE","#ADF4FE","#B4F5FE","#BAF5FE","#C2F6FE","#C8F7FE","#D0F9FF","#D8F9FE","#DEF8FC"]
    
  for dcm in range(0,10):
    #print(row_cmh)
    year_cmh = str(row_cmh[0])
    temp_cmh = str(row_cmh[2])
    cmh_top10[0].append('<tr>' + '\n' +
                        '<td bgcolor=' + color_cmh_num[dcm] + ' style="vertical-align: middle" align="center" colspan="1">' + '\n' +
                        '<p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">' + str(dcm+1) + '<br />' +'\n'+
			'</p></td>')
    cmh_top10[0].append('<td bgcolor=' + color_cmh_value[dcm] + ' style="vertical-align: middle" align="center" colspan="1">'
                        '<p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;" >' + temp_cmh + '| ' + year_cmh + '<br />' +'\n'+
                        '</p></td></tr>' + '\n')
    row_cmh = cursor.fetchone()    
  cmh_top10[0].append(Footer)

  #DAY
  query_day = ("SELECT Year, Month, Monthly_Snow_Total FROM climate.kday_monthly where Month = " + str(i+1) + " AND Monthly_Snow_Total != 'M' AND Monthly_Snow_Total != 'T' ORDER BY Monthly_Snow_Total+0 DESC, Year DESC;")
  cursor.execute(query_day)
  row_day = cursor.fetchone()
  day_top10[0].append(Header_Snow)
  color_day_num = []
  color_day_value = []
  color_day_num = ["#26A4B6","#2DABBD","#33B0C2","#3AB5C7","#40BBCD","#47C0D1","#50C7D8","#5ACFDF","#64D5E5","#6EDBEB"]
  color_day_value = ["#9CF1FE","#A7F3FE","#ADF4FE","#B4F5FE","#BAF5FE","#C2F6FE","#C8F7FE","#D0F9FF","#D8F9FE","#DEF8FC"]

  for dd in range(0,10):
    #print(row_day)
    year_day = str(row_day[0])
    temp_day = str(row_day[2])
    day_top10[0].append('<tr>' + '\n' +
                        '<td bgcolor=' + color_day_num[dd] + ' style="vertical-align: middle" align="center" colspan="1">' + '\n' +
                        '<p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">' + str(dd+1) + '<br />' +'\n'+
			'</p></td>')
    day_top10[0].append('<td bgcolor=' + color_day_value[dd] + ' style="vertical-align: middle" align="center" colspan="1">'
                        '<p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;" >' + temp_day + '| ' + year_day + '<br />' +'\n'+
                        '</p></td></tr>' + '\n')
    row_day = cursor.fetchone()    
  day_top10[0].append(Footer)

  ## Get Top 10 least snowiest ##
  #CVG
  query_cvg = ("SELECT Year, Month, Monthly_Snow_Total FROM climate.kcvg_monthly where Month = " + str(i+1) + " AND Monthly_Snow_Total != 'M' AND Monthly_Snow_Total != 'T' ORDER BY Monthly_Snow_Total+0 ASC, Year DESC;")
  cursor.execute(query_cvg)
  row_cvg = cursor.fetchone()
  cvg_top10[0].append(Header_LeastSnow)
  color_cvg_num = []
  color_cvg_value = []
  color_cvg_num = ["#26A4B6","#2DABBD","#33B0C2","#3AB5C7","#40BBCD","#47C0D1","#50C7D8","#5ACFDF","#64D5E5","#6EDBEB"]
  color_cvg_value = ["#9CF1FE","#A7F3FE","#ADF4FE","#B4F5FE","#BAF5FE","#C2F6FE","#C8F7FE","#D0F9FF","#D8F9FE","#DEF8FC"]
    
  for dcv in range(0,10):
    #print(row_day)
    year_cvg = str(row_cvg[0])
    temp_cvg = str(row_cvg[2])
    cvg_top10[0].append('<tr>' + '\n' +
                        '<td bgcolor=' + color_cvg_num[dcv] + ' style="vertical-align: middle" align="center" colspan="1">' + '\n' +
                        '<p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">' + str(dcv+1) + '<br />' +'\n'+
			'</p></td>')
    cvg_top10[0].append('<td bgcolor=' + color_cvg_value[dcv] + ' style="vertical-align: middle" align="center" colspan="1">'
                        '<p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;" >' + temp_cvg + '| ' + year_cvg + '<br />' +'\n'+
                        '</p></td></tr>' + '\n')
    row_cvg = cursor.fetchone()    
  cvg_top10[0].append(Footer)

  #CMH
  query_cmh = ("SELECT Year, Month, Monthly_Snow_Total FROM climate.kcmh_monthly where Month = " + str(i+1) + " AND Monthly_Snow_Total != 'M' AND Monthly_Snow_Total != 'T' ORDER BY Monthly_Snow_Total+0 ASC, Year DESC;")
  cursor.execute(query_cmh)
  row_cmh = cursor.fetchone()
  cmh_top10[0].append(Header_LeastSnow)
  color_cmh_num = []
  color_cmh_value = []
  color_cmh_num = ["#26A4B6","#2DABBD","#33B0C2","#3AB5C7","#40BBCD","#47C0D1","#50C7D8","#5ACFDF","#64D5E5","#6EDBEB"]
  color_cmh_value = ["#9CF1FE","#A7F3FE","#ADF4FE","#B4F5FE","#BAF5FE","#C2F6FE","#C8F7FE","#D0F9FF","#D8F9FE","#DEF8FC"]
    
  for dcm in range(0,10):
    #print(row_cmh)
    year_cmh = str(row_cmh[0])
    temp_cmh = str(row_cmh[2])
    cmh_top10[0].append('<tr>' + '\n' +
                        '<td bgcolor=' + color_cmh_num[dcm] + ' style="vertical-align: middle" align="center" colspan="1">' + '\n' +
                        '<p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">' + str(dcm+1) + '<br />' +'\n'+
			'</p></td>')
    cmh_top10[0].append('<td bgcolor=' + color_cmh_value[dcm] + ' style="vertical-align: middle" align="center" colspan="1">'
                        '<p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;" >' + temp_cmh + '| ' + year_cmh + '<br />' +'\n'+
                        '</p></td></tr>' + '\n')
    row_cmh = cursor.fetchone()    
  cmh_top10[0].append(Footer)

  #DAY
  query_day = ("SELECT Year, Month, Monthly_Snow_Total FROM climate.kday_monthly where Month = " + str(i+1) + " AND Monthly_Snow_Total != 'M' AND Monthly_Snow_Total != 'T' ORDER BY Monthly_Snow_Total+0 ASC, Year DESC;")
  cursor.execute(query_day)
  row_day = cursor.fetchone()
  day_top10[0].append(Header_LeastSnow)
  color_day_num = []
  color_day_value = []
  color_day_num = ["#26A4B6","#2DABBD","#33B0C2","#3AB5C7","#40BBCD","#47C0D1","#50C7D8","#5ACFDF","#64D5E5","#6EDBEB"]
  color_day_value = ["#9CF1FE","#A7F3FE","#ADF4FE","#B4F5FE","#BAF5FE","#C2F6FE","#C8F7FE","#D0F9FF","#D8F9FE","#DEF8FC"]
    
  for dd in range(0,10):
    #print(row_day)
    year_day = str(row_day[0])
    temp_day = str(row_day[2])
    day_top10[0].append('<tr>' + '\n' +
                        '<td bgcolor=' + color_day_num[dd] + ' style="vertical-align: middle" align="center" colspan="1">' + '\n' +
                        '<p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">' + str(dd+1) + '<br />' +'\n'+
			'</p></td>')
    day_top10[0].append('<td bgcolor=' + color_day_value[dd] + ' style="vertical-align: middle" align="center" colspan="1">'
                        '<p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;" >' + temp_day + '| ' + year_day + '<br />' +'\n'+
                        '</p></td></tr>' + '\n')
    row_day = cursor.fetchone()    
  day_top10[0].append(Footer)


  ## Output files ##
  final_cvg = open(output_file_cvg,"w")
  final_cmh = open(output_file_cmh,"w")
  final_day = open(output_file_day,"w")

  for j in range(0,len(cvg_top10[0])):
      text_cvg='\n'.join(listitem_cvg[j] for listitem_cvg in cvg_top10)
      text_cmh='\n'.join(listitem_cmh[j] for listitem_cmh in cmh_top10)
      text_day='\n'.join(listitem_day[j] for listitem_day in day_top10)
      final_cvg.write(text_cvg)
      final_cmh.write(text_cmh)
      final_day.write(text_day)

  final_cvg.close()
  final_cmh.close()
  final_day.close()


### End of main code ###
cursor.close()
cnx.close()

print(' Now creating pdf files')
for i in range(0,3):
  pdfkit.from_file('X:/Users/brian.haines/Projects/ClimateWebpage/PDFTxtFiles/Top10/' + sites_cap[i] + '/climate_top10_' + sites_low[i] + '_jan.html', 'X:/Users/brian.haines/Projects/ClimateWebpage/PDFTxtFiles/Top10/' + sites_cap[i] + '/cms_media+climo_webpage+climate_top10_' + sites_low[i] + '_jan.pdf')
  pdfkit.from_file('X:/Users/brian.haines/Projects/ClimateWebpage/PDFTxtFiles/Top10/' + sites_cap[i] + '/climate_top10_' + sites_low[i] + '_jan.html', 'X:/Users/ILN_Common/1-BrianandKristen/ClimateWebpage/PDFTxtFiles/Top10/' + sites_cap[i] + '/cms_media+climo_webpage+climate_top10_' + sites_low[i] + '_jan.pdf')
  pdfkit.from_file('X:/Users/brian.haines/Projects/ClimateWebpage/PDFTxtFiles/Top10/' + sites_cap[i] + '/climate_top10_' + sites_low[i] + '_jan.html', 'X:/Apps/WinSCP/ldad_upload/data_ldad_public_nwswwas/cms_media+climo_webpage+climate_top10_' + sites_low[i] + '_jan.pdf')
  pdfkit.from_file('X:/Users/brian.haines/Projects/ClimateWebpage/PDFTxtFiles/Top10/' + sites_cap[i] + '/climate_top10_' + sites_low[i] + '_feb.html', 'X:/Users/brian.haines/Projects/ClimateWebpage/PDFTxtFiles/Top10/' + sites_cap[i] + '/cms_media+climo_webpage+climate_top10_' + sites_low[i] + '_feb.pdf')
  pdfkit.from_file('X:/Users/brian.haines/Projects/ClimateWebpage/PDFTxtFiles/Top10/' + sites_cap[i] + '/climate_top10_' + sites_low[i] + '_feb.html', 'X:/Users/ILN_Common/1-BrianandKristen/ClimateWebpage/PDFTxtFiles/Top10/' + sites_cap[i] + '/cms_media+climo_webpage+climate_top10_' + sites_low[i] + '_feb.pdf')
  pdfkit.from_file('X:/Users/brian.haines/Projects/ClimateWebpage/PDFTxtFiles/Top10/' + sites_cap[i] + '/climate_top10_' + sites_low[i] + '_feb.html', 'X:/Apps/WinSCP/ldad_upload/data_ldad_public_nwswwas/cms_media+climo_webpage+climate_top10_' + sites_low[i] + '_feb.pdf')
  pdfkit.from_file('X:/Users/brian.haines/Projects/ClimateWebpage/PDFTxtFiles/Top10/' + sites_cap[i] + '/climate_top10_' + sites_low[i] + '_mar.html', 'X:/Users/brian.haines/Projects/ClimateWebpage/PDFTxtFiles/Top10/' + sites_cap[i] + '/cms_media+climo_webpage+climate_top10_' + sites_low[i] + '_mar.pdf')
  pdfkit.from_file('X:/Users/brian.haines/Projects/ClimateWebpage/PDFTxtFiles/Top10/' + sites_cap[i] + '/climate_top10_' + sites_low[i] + '_mar.html', 'X:/Users/ILN_Common/1-BrianandKristen/ClimateWebpage/PDFTxtFiles/Top10/' + sites_cap[i] + '/cms_media+climo_webpage+climate_top10_' + sites_low[i] + '_mar.pdf')
  pdfkit.from_file('X:/Users/brian.haines/Projects/ClimateWebpage/PDFTxtFiles/Top10/' + sites_cap[i] + '/climate_top10_' + sites_low[i] + '_mar.html', 'X:/Apps/WinSCP/ldad_upload/data_ldad_public_nwswwas/cms_media+climo_webpage+climate_top10_' + sites_low[i] + '_mar.pdf')
  pdfkit.from_file('X:/Users/brian.haines/Projects/ClimateWebpage/PDFTxtFiles/Top10/' + sites_cap[i] + '/climate_top10_' + sites_low[i] + '_apr.html', 'X:/Users/brian.haines/Projects/ClimateWebpage/PDFTxtFiles/Top10/' + sites_cap[i] + '/cms_media+climo_webpage+climate_top10_' + sites_low[i] + '_apr.pdf')
  pdfkit.from_file('X:/Users/brian.haines/Projects/ClimateWebpage/PDFTxtFiles/Top10/' + sites_cap[i] + '/climate_top10_' + sites_low[i] + '_apr.html', 'X:/Users/ILN_Common/1-BrianandKristen/ClimateWebpage/PDFTxtFiles/Top10/' + sites_cap[i] + '/cms_media+climo_webpage+climate_top10_' + sites_low[i] + '_apr.pdf')
  pdfkit.from_file('X:/Users/brian.haines/Projects/ClimateWebpage/PDFTxtFiles/Top10/' + sites_cap[i] + '/climate_top10_' + sites_low[i] + '_apr.html', 'X:/Apps/WinSCP/ldad_upload/data_ldad_public_nwswwas/cms_media+climo_webpage+climate_top10_' + sites_low[i] + '_apr.pdf')
  pdfkit.from_file('X:/Users/brian.haines/Projects/ClimateWebpage/PDFTxtFiles/Top10/' + sites_cap[i] + '/climate_top10_' + sites_low[i] + '_may.html', 'X:/Users/brian.haines/Projects/ClimateWebpage/PDFTxtFiles/Top10/' + sites_cap[i] + '/cms_media+climo_webpage+climate_top10_' + sites_low[i] + '_may.pdf')
  pdfkit.from_file('X:/Users/brian.haines/Projects/ClimateWebpage/PDFTxtFiles/Top10/' + sites_cap[i] + '/climate_top10_' + sites_low[i] + '_may.html', 'X:/Users/ILN_Common/1-BrianandKristen/ClimateWebpage/PDFTxtFiles/Top10/' + sites_cap[i] + '/cms_media+climo_webpage+climate_top10_' + sites_low[i] + '_may.pdf')
  pdfkit.from_file('X:/Users/brian.haines/Projects/ClimateWebpage/PDFTxtFiles/Top10/' + sites_cap[i] + '/climate_top10_' + sites_low[i] + '_may.html', 'X:/Apps/WinSCP/ldad_upload/data_ldad_public_nwswwas/cms_media+climo_webpage+climate_top10_' + sites_low[i] + '_may.pdf')
  pdfkit.from_file('X:/Users/brian.haines/Projects/ClimateWebpage/PDFTxtFiles/Top10/' + sites_cap[i] + '/climate_top10_' + sites_low[i] + '_jun.html', 'X:/Users/brian.haines/Projects/ClimateWebpage/PDFTxtFiles/Top10/' + sites_cap[i] + '/cms_media+climo_webpage+climate_top10_' + sites_low[i] + '_jun.pdf')
  pdfkit.from_file('X:/Users/brian.haines/Projects/ClimateWebpage/PDFTxtFiles/Top10/' + sites_cap[i] + '/climate_top10_' + sites_low[i] + '_jun.html', 'X:/Users/ILN_Common/1-BrianandKristen/ClimateWebpage/PDFTxtFiles/Top10/' + sites_cap[i] + '/cms_media+climo_webpage+climate_top10_' + sites_low[i] + '_jun.pdf')
  pdfkit.from_file('X:/Users/brian.haines/Projects/ClimateWebpage/PDFTxtFiles/Top10/' + sites_cap[i] + '/climate_top10_' + sites_low[i] + '_jun.html', 'X:/Apps/WinSCP/ldad_upload/data_ldad_public_nwswwas/cms_media+climo_webpage+climate_top10_' + sites_low[i] + '_jun.pdf')
  pdfkit.from_file('X:/Users/brian.haines/Projects/ClimateWebpage/PDFTxtFiles/Top10/' + sites_cap[i] + '/climate_top10_' + sites_low[i] + '_jul.html', 'X:/Users/brian.haines/Projects/ClimateWebpage/PDFTxtFiles/Top10/' + sites_cap[i] + '/cms_media+climo_webpage+climate_top10_' + sites_low[i] + '_jul.pdf')
  pdfkit.from_file('X:/Users/brian.haines/Projects/ClimateWebpage/PDFTxtFiles/Top10/' + sites_cap[i] + '/climate_top10_' + sites_low[i] + '_jul.html', 'X:/Users/ILN_Common/1-BrianandKristen/ClimateWebpage/PDFTxtFiles/Top10/' + sites_cap[i] + '/cms_media+climo_webpage+climate_top10_' + sites_low[i] + '_jul.pdf')
  pdfkit.from_file('X:/Users/brian.haines/Projects/ClimateWebpage/PDFTxtFiles/Top10/' + sites_cap[i] + '/climate_top10_' + sites_low[i] + '_jul.html', 'X:/Apps/WinSCP/ldad_upload/data_ldad_public_nwswwas/cms_media+climo_webpage+climate_top10_' + sites_low[i] + '_jul.pdf')
  pdfkit.from_file('X:/Users/brian.haines/Projects/ClimateWebpage/PDFTxtFiles/Top10/' + sites_cap[i] + '/climate_top10_' + sites_low[i] + '_aug.html', 'X:/Users/brian.haines/Projects/ClimateWebpage/PDFTxtFiles/Top10/' + sites_cap[i] + '/cms_media+climo_webpage+climate_top10_' + sites_low[i] + '_aug.pdf')
  pdfkit.from_file('X:/Users/brian.haines/Projects/ClimateWebpage/PDFTxtFiles/Top10/' + sites_cap[i] + '/climate_top10_' + sites_low[i] + '_aug.html', 'X:/Users/ILN_Common/1-BrianandKristen/ClimateWebpage/PDFTxtFiles/Top10/' + sites_cap[i] + '/cms_media+climo_webpage+climate_top10_' + sites_low[i] + '_aug.pdf')
  pdfkit.from_file('X:/Users/brian.haines/Projects/ClimateWebpage/PDFTxtFiles/Top10/' + sites_cap[i] + '/climate_top10_' + sites_low[i] + '_aug.html', 'X:/Apps/WinSCP/ldad_upload/data_ldad_public_nwswwas/cms_media+climo_webpage+climate_top10_' + sites_low[i] + '_aug.pdf')
  pdfkit.from_file('X:/Users/brian.haines/Projects/ClimateWebpage/PDFTxtFiles/Top10/' + sites_cap[i] + '/climate_top10_' + sites_low[i] + '_sept.html', 'X:/Users/brian.haines/Projects/ClimateWebpage/PDFTxtFiles/Top10/' + sites_cap[i] + '/cms_media+climo_webpage+climate_top10_' + sites_low[i] + '_sept.pdf')
  pdfkit.from_file('X:/Users/brian.haines/Projects/ClimateWebpage/PDFTxtFiles/Top10/' + sites_cap[i] + '/climate_top10_' + sites_low[i] + '_sept.html', 'X:/Users/ILN_Common/1-BrianandKristen/ClimateWebpage/PDFTxtFiles/Top10/' + sites_cap[i] + '/cms_media+climo_webpage+climate_top10_' + sites_low[i] + '_sept.pdf')
  pdfkit.from_file('X:/Users/brian.haines/Projects/ClimateWebpage/PDFTxtFiles/Top10/' + sites_cap[i] + '/climate_top10_' + sites_low[i] + '_sept.html', 'X:/Apps/WinSCP/ldad_upload/data_ldad_public_nwswwas/cms_media+climo_webpage+climate_top10_' + sites_low[i] + '_sept.pdf')
  pdfkit.from_file('X:/Users/brian.haines/Projects/ClimateWebpage/PDFTxtFiles/Top10/' + sites_cap[i] + '/climate_top10_' + sites_low[i] + '_oct.html', 'X:/Users/brian.haines/Projects/ClimateWebpage/PDFTxtFiles/Top10/' + sites_cap[i] + '/cms_media+climo_webpage+climate_top10_' + sites_low[i] + '_oct.pdf')
  pdfkit.from_file('X:/Users/brian.haines/Projects/ClimateWebpage/PDFTxtFiles/Top10/' + sites_cap[i] + '/climate_top10_' + sites_low[i] + '_oct.html', 'X:/Users/ILN_Common/1-BrianandKristen/ClimateWebpage/PDFTxtFiles/Top10/' + sites_cap[i] + '/cms_media+climo_webpage+climate_top10_' + sites_low[i] + '_oct.pdf')
  pdfkit.from_file('X:/Users/brian.haines/Projects/ClimateWebpage/PDFTxtFiles/Top10/' + sites_cap[i] + '/climate_top10_' + sites_low[i] + '_oct.html', 'X:/Apps/WinSCP/ldad_upload/data_ldad_public_nwswwas/cms_media+climo_webpage+climate_top10_' + sites_low[i] + '_oct.pdf')
  pdfkit.from_file('X:/Users/brian.haines/Projects/ClimateWebpage/PDFTxtFiles/Top10/' + sites_cap[i] + '/climate_top10_' + sites_low[i] + '_nov.html', 'X:/Users/brian.haines/Projects/ClimateWebpage/PDFTxtFiles/Top10/' + sites_cap[i] + '/cms_media+climo_webpage+climate_top10_' + sites_low[i] + '_nov.pdf')
  pdfkit.from_file('X:/Users/brian.haines/Projects/ClimateWebpage/PDFTxtFiles/Top10/' + sites_cap[i] + '/climate_top10_' + sites_low[i] + '_nov.html', 'X:/Users/ILN_Common/1-BrianandKristen/ClimateWebpage/PDFTxtFiles/Top10/' + sites_cap[i] + '/cms_media+climo_webpage+climate_top10_' + sites_low[i] + '_nov.pdf')
  pdfkit.from_file('X:/Users/brian.haines/Projects/ClimateWebpage/PDFTxtFiles/Top10/' + sites_cap[i] + '/climate_top10_' + sites_low[i] + '_nov.html', 'X:/Apps/WinSCP/ldad_upload/data_ldad_public_nwswwas/cms_media+climo_webpage+climate_top10_' + sites_low[i] + '_nov.pdf')
  pdfkit.from_file('X:/Users/brian.haines/Projects/ClimateWebpage/PDFTxtFiles/Top10/' + sites_cap[i] + '/climate_top10_' + sites_low[i] + '_dec.html', 'X:/Users/brian.haines/Projects/ClimateWebpage/PDFTxtFiles/Top10/' + sites_cap[i] + '/cms_media+climo_webpage+climate_top10_' + sites_low[i] + '_dec.pdf')
  pdfkit.from_file('X:/Users/brian.haines/Projects/ClimateWebpage/PDFTxtFiles/Top10/' + sites_cap[i] + '/climate_top10_' + sites_low[i] + '_dec.html', 'X:/Users/ILN_Common/1-BrianandKristen/ClimateWebpage/PDFTxtFiles/Top10/' + sites_cap[i] + '/cms_media+climo_webpage+climate_top10_' + sites_low[i] + '_dec.pdf')
  pdfkit.from_file('X:/Users/brian.haines/Projects/ClimateWebpage/PDFTxtFiles/Top10/' + sites_cap[i] + '/climate_top10_' + sites_low[i] + '_dec.html', 'X:/Apps/WinSCP/ldad_upload/data_ldad_public_nwswwas/cms_media+climo_webpage+climate_top10_' + sites_low[i] + '_dec.pdf')

print(' Script completed and files genereated... ')

