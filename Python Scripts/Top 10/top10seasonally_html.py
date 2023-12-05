### HEADER ###
# Name: Brian Haines
# Modified By: Austin Rebello
# Date: 8/11/2015
# Purpose: Create a script that requests mysql data and generates html file
# Version/ update history:
#    1) 08-08-15: Script completed!
#    2) 01-22-17: Script updated to incorporate Kristens new design changes
#    3) 02-27-18: Added code for least snowiest months and sort by year (newest to oldest)
#    4) 11-26-23: Converted to Python 3 and to NWS CLE
### --- ###

### Import needed modules ###
import mysql.connector
import datetime
import time
import datetime
import pdfkit
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
season = ["Winter", "Spring", "Summer", "Fall"] #Used for Title in HTML
season_nm = ['winter' , 'spring', 'summer', 'fall'] #Naming html file
sites = [["cak", 1887],["cle", 1871],["eri", 1873],["mfd", 1899],["tol", 1871],["yng", 1896]]

### --- ###

### Main Code ###
def htmlSite(site, porStart):
        print('Generating HTML file for '+site)
        ## Intialize python lists to hold data ##
        top10 = []
        
        top10.append(
                '<style>' + '\n' + 'body {' + '\n' + 'text-align:center;' + '\n' + '}' + '\n' + '</style>'+ '\n' +
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
                                        '</table>'+ '\n'
        )
         ## Output File List ###
        output_file = '../../PDFTxtFiles/Top10/Seasonally/'+site.upper()+'/seasonal.html'
        ## -- ##
        
        for i in range(0,len(season)): # Main for loop to go through and create all data for each month
                Header_Warm = (
                                        '<table width="80%" cellpadding="3" align="center">' + '\n' + '<tr bgcolor="#000000">' + '\n' +
                                        '<td colspan="2">' + '\n' +
                                        '<p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">'+ '\n' +
                                        site.upper()+' ' + season[i] + ' Top 10 Lists' + ' ('+str(porStart)+' - ' + current_year + ') ' + '</p></td>' + '\n' +
                                        '</tr>' + '\n' +
                                        '</table>' + '\n' +
                                        '<br />'+ '\n' +
                                        '<table cellspacing="0" cellpadding="3" border="1" align = "center" style="display:inline-block;margin:0em;">' + '\n' +
                                        '<tbody>' + '\n'+
                                        '<tr align="center">' + '\n' +
                                        '<td colspan="3">' + '\n' +
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
                                        '<p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Value<br />' +'\n'+
                                        '</p>' +'\n'+
                                        '</td>' +'\n'+
                                        '<td bgcolor="#424949" style="vertical-align: middle" align="center" colspan="1">' +'\n'+
                                        '<p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Year<br />' +'\n'+
                                        '</p>' +'\n'+
                                        '</td>' +'\n'+
                                        '</tr>' +'\n')

                Header_Cold = ('<table align="center" border="1" cellpadding="3" cellspacing="0" class="images" style="display:inline-block;margin:0em;">' + '\n' +
                                        '<tbody>' + '\n'+
                                        '<tr>' + '\n' + '<td colspan="3">'+ '\n' +
                                        '<p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">'+ '\n' +
                                        'Top 10<br />Coldest</p></td>'  + '\n' +
                                        '</tr>' +'\n'+
                                        '<tr>' +'\n'+
                                        '<td bgcolor="#424949" style="vertical-align: middle;" align="center" colspan="1">' +'\n'+
                                        '<p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Rank<br />' +'\n'+
                                        '</p>' +'\n'+
                                        '</td>' +'\n'+
                                        '<td bgcolor="#424949" style="vertical-align: middle" align="center" colspan="1">' +'\n'+
                                        '<p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Value<br />' +'\n'+
                                        '</p>' +'\n'+
                                        '</td>' +'\n'+
                                        '<td bgcolor="#424949" style="vertical-align: middle" align="center" colspan="1">' +'\n'+
                                        '<p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Year<br />' +'\n'+
                                        '</p>' +'\n'+
                                        '</td>' +'\n'+
                                        '</tr>' +'\n')

                Header_Wet = ('<table align="center" border="1" cellpadding="3" cellspacing="0" class="images" style="display:inline-block;margin:0em;">' + '\n' +
                                        '<tbody>' + '\n'+
                                        '<tr>' + '\n' + '<td colspan="3">'+ '\n' +
                                        '<p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">'+ '\n' +
                                        'Top 10<br />Wettest</p></td>'  + '\n' +
                                        '</tr>' +'\n'+
                                        '<tr>' +'\n'+
                                        '<td bgcolor="#424949" style="vertical-align: middle;" align="center" colspan="1">' +'\n'+
                                        '<p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Rank<br />' +'\n'+
                                        '</p>' +'\n'+
                                        '</td>' +'\n'+
                                        '<td bgcolor="#424949" style="vertical-align: middle" align="center" colspan="1">' +'\n'+
                                        '<p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Value<br />' +'\n'+
                                        '</p>' +'\n'+
                                        '</td>' +'\n'+
                                        '<td bgcolor="#424949" style="vertical-align: middle" align="center" colspan="1">' +'\n'+
                                        '<p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Year<br />' +'\n'+
                                        '</p>' +'\n'+
                                        '</td>' +'\n'+
                                        '</tr>' +'\n')

                Header_Dry = ('<table align="center" border="1" cellpadding="3" cellspacing="0" class="images" style="display:inline-block;margin:0em;">' + '\n' +
                                        '<tbody>' + '\n'+
                                        '<tr>' + '\n' + '<td colspan="3">'+ '\n' +
                                        '<p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">'+ '\n' +
                                        'Top 10<br />Driest</p></td>'  + '\n' +
                                        '</tr>' +'\n'+
                                        '<tr>' +'\n'+
                                        '<td bgcolor="#424949" style="vertical-align: middle;" align="center" colspan="1">' +'\n'+
                                        '<p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Rank<br />' +'\n'+
                                        '</p>' +'\n'+
                                        '</td>' +'\n'+
                                        '<td bgcolor="#424949" style="vertical-align: middle" align="center" colspan="1">' +'\n'+
                                        '<p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Value<br />' +'\n'+
                                        '</p>' +'\n'+
                                        '</td>' +'\n'+
                                        '<td bgcolor="#424949" style="vertical-align: middle" align="center" colspan="1">' +'\n'+
                                        '<p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Year<br />' +'\n'+
                                        '</p>' +'\n'+
                                        '</td>' +'\n'+
                                        '</tr>' +'\n')

                Header_Snow = ('<table align="center" border="1" cellpadding="3" cellspacing="0" class="images" style="display:inline-block;margin:0em;">' + '\n' +
                                        '<tbody>' + '\n'+
                                        '<tr>' + '\n' + '<td colspan="3">'+ '\n' +
                                        '<p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">'+ '\n' +
                                        'Top 10<br />Snowiest</p></td>'  + '\n' +
                                        '</tr>' +'\n'+
                                        '<tr>' +'\n'+
                                        '<td bgcolor="#424949" style="vertical-align: middle;" align="center" colspan="1">' +'\n'+
                                        '<p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Rank<br />' +'\n'+
                                        '</p>' +'\n'+
                                        '</td>' +'\n'+
                                        '<td bgcolor="#424949" style="vertical-align: middle" align="center" colspan="1">' +'\n'+
                                        '<p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Value<br />' +'\n'+
                                        '</p>' +'\n'+
                                        '</td>' +'\n'+
                                        '<td bgcolor="#424949" style="vertical-align: middle" align="center" colspan="1">' +'\n'+
                                        '<p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Year<br />' +'\n'+
                                        '</p>' +'\n'+
                                        '</td>' +'\n'+
                                        '</tr>' +'\n')
                Header_LeastSnow = ('<table align="center" border="1" cellpadding="3" cellspacing="0" class="images" style="display:inline-block;margin:0em;">' + '\n' +
                                        '<tbody>' + '\n'+
                                        '<tr>' + '\n' + '<td colspan="3">'+ '\n' +
                                        '<p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">'+ '\n' +
                                        'Top 10<br />Least Snowiest</p></td>'  + '\n' +
                                        '</tr>' +'\n'+
                                        '<tr>' +'\n'+
                                        '<td bgcolor="#424949" style="vertical-align: middle;" align="center" colspan="1">' +'\n'+
                                        '<p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Rank<br />' +'\n'+
                                        '</p>' +'\n'+
                                        '</td>' +'\n'+
                                        '<td bgcolor="#424949" style="vertical-align: middle" align="center" colspan="1">' +'\n'+
                                        '<p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Value<br />' +'\n'+
                                        '</p>' +'\n'+
                                        '</td>' +'\n'+
                                        '<td bgcolor="#424949" style="vertical-align: middle" align="center" colspan="1">' +'\n'+
                                        '<p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">Year<br />' +'\n'+
                                        '</p>' +'\n'+
                                        '</td>' +'\n'+
                                        '</tr>' +'\n')

                Footer = ('</tbody></table>' + '\n')


                ## Get Top 10 warmest ##
                query = ("SELECT Year, Season, Seasonal_Temp_Avg FROM climate.seasonally_"+site+" where season = '" + season[i].upper() + "' AND Seasonal_Temp_Avg != 'M' ORDER BY Seasonal_Temp_Avg+0 DESC, Year DESC;")
                cursor.execute(query)
                row = cursor.fetchone()
                top10.append(Header_Warm)
                color_num = []
                color_value = []
                color_num = ["#A51B13","#AF231A","#B82D24","#C4372E","#CF4239","#D94E45","#E0564D","#E86057","#F06A61","#F7736A"]
                color_value = ["#FCB1AB","#FDBDB7","#FDC5C0","#FECECA","#FDD5D1","#FEDCD8","#FEE2DE","#FEE9E5","#FDEEEC","#FDF5F4"]

                for dcv in range(0,10):
                        #print(row)
                        year = str(row[0])
                        temp = str(row[2])
                        top10.append('<tr>' + '\n' +
                                                '<td bgcolor=' + color_num[dcv] + ' style="vertical-align: middle" align="center" colspan="1">' + '\n' +
                                                '<p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">' + str(dcv+1) + '<br />' +'\n'+
                                                '</p></td>')
                        top10.append('<td bgcolor=' + color_value[dcv] + ' style="vertical-align: middle" align="center" colspan="1">'
                                                '<p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;" >' + temp + '<br />' +'\n'+
                                                '</p></td>' + '\n')
                        top10.append('<td bgcolor=' + color_value[dcv] + ' style="vertical-align: middle" align="center" colspan="1">'
                                                '<p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;" >' + year + '<br />' +'\n'+
                                                '</p></td></tr>' + '\n')
                        row = cursor.fetchone()    
                top10.append(Footer)

                ## Get Top 10 coldest ##
                query = ("SELECT Year, Season, Seasonal_Temp_Avg FROM climate.seasonally_"+site+" where Season = '" + season[i].upper() + "' AND Seasonal_Temp_Avg != 'M' ORDER BY Seasonal_Temp_Avg+0, Year DESC;")
                cursor.execute(query)
                row = cursor.fetchone()
                top10.append(Header_Cold)
                color_num = []
                color_value = []
                color_num = ["#3239C2","#3C43CA","#454CD1","#4E55D6","#555CDA","#6066DF","#6A70E5","#747AE9","#8187EF","#9095F5"]
                color_value = ["#9FA3FC","#A6AAFE","#ADB0FF","#B3B6FD","#BBBEFE","#C3C6FE","#C9CCFE","#D1D3FE","#D8DAFE","#E0E2FE"]

                for dcv in range(0,10):
                        #print(row)
                        year = str(row[0])
                        temp = str(row[2])
                        top10.append('<tr>' + '\n' +
                                                '<td bgcolor=' + color_num[dcv] + ' style="vertical-align: middle" align="center" colspan="1">' + '\n' +
                                                '<p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">' + str(dcv) + '<br />' +'\n'+
                                                '</p></td>')
                        top10.append('<td bgcolor=' + color_value[dcv] + ' style="vertical-align: middle" align="center" colspan="1">'
                                                '<p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;" >' + temp +  '<br />' +'\n'+
                                                '</p></td>' + '\n')
                        top10.append('<td bgcolor=' + color_value[dcv] + ' style="vertical-align: middle" align="center" colspan="1">'
                                                '<p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;" >' + year + '<br />' +'\n'+
                                                '</p></td></tr>' + '\n')
                        row = cursor.fetchone()    
                top10.append(Footer)

                ## Get Top 10 wettest ##
                query = ("SELECT Year, Season, Seasonal_Precip_Total FROM climate.seasonally_"+site+" where Season = '" + season[i].upper() + "' AND Seasonal_Precip_Total != 'M' ORDER BY Seasonal_Precip_Total+0 DESC, Year DESC;")
                cursor.execute(query)
                row = cursor.fetchone()
                top10.append(Header_Wet)
                color_num = []
                color_value = []
                color_num = ["#27AF17","#2EB71D","#35BD24","#3CC32B","#44CB33","#4BD13A","#52D641","#58DA48","#5FDF4F","#68E459"]
                color_value = ["#91FD84","#98FE8C","#9DFE91","#A2FE97","#AAFEA0","#B0FFA6","#B7FEAE","#BDFDB5","#C6FEBF","#CDFDC7"]

                for dcv in range(0,10):
                        #print(row)
                        year = str(row[0])
                        temp = str(row[2])
                        top10.append('<tr>' + '\n' +
                                                '<td bgcolor=' + color_num[dcv] + ' style="vertical-align: middle" align="center" colspan="1">' + '\n' +
                                                '<p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">' + str(dcv+1) + '<br />' +'\n'+
                                                '</p></td>')
                        top10.append('<td bgcolor=' + color_value[dcv] + ' style="vertical-align: middle" align="center" colspan="1">'
                                                '<p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;" >' + temp + '<br />' +'\n'+
                                                '</p></td>' + '\n')
                        top10.append('<td bgcolor=' + color_value[dcv] + ' style="vertical-align: middle" align="center" colspan="1">'
                                                '<p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;" >' + year + '<br />' +'\n'+
                                                '</p></td></tr>' + '\n')
                        row = cursor.fetchone()    
                top10.append(Footer)

                ## Get Top 10 driest ##
                query = ("SELECT Year, Season, Seasonal_Precip_Total FROM climate.seasonally_"+site+" where Season = '" + season[i].upper() + "' AND Seasonal_Precip_Total != 'M' ORDER BY Seasonal_Precip_Total+0, Year DESC;")
                cursor.execute(query)
                row = cursor.fetchone()
                top10.append(Header_Dry)
                color_num = []
                color_value = []
                color_num = ["#BD9027","#C2952D","#C69A33","#CBA03A","#D1A641","#D8AD49","#DEB352","#E3B95A","#E8BF63","#EEC66D"]
                color_value = ["#FEDE96","#FEE09C","#FEE2A3","#FEE4AA","#FEE6B2","#FEE9B9","#FEEBBF","#FEEDC6","#FEEFCD","#FEF1D5"]

                for dcv in range(0,10):
                        #print(row)
                        year = str(row[0])
                        temp = str(row[2])
                        top10.append('<tr>' + '\n' +
                                                '<td bgcolor=' + color_num[dcv] + ' style="vertical-align: middle" align="center" colspan="1">' + '\n' +
                                                '<p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">' + str(dcv+1) + '<br />' +'\n'+
                                                '</p></td>')
                        top10.append('<td bgcolor=' + color_value[dcv] + ' style="vertical-align: middle" align="center" colspan="1">'
                                                '<p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;" >' + temp +  '<br />' +'\n'+
                                                '</p></td>' + '\n')
                        top10.append('<td bgcolor=' + color_value[dcv] + ' style="vertical-align: middle" align="center" colspan="1">'
                                                '<p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;" >'  + year + '<br />' +'\n'+
                                                '</p></td></tr>' + '\n')
                        row = cursor.fetchone()    
                top10.append(Footer)

                ## Get Top 10 snowiest ##
                query = ("SELECT Year, Season, Seasonal_Snow_Total FROM climate.seasonally_"+site+" where Season = '" + season[i].upper() + "' AND Seasonal_Snow_Total != 'M' ORDER BY Case Seasonal_Snow_Total  WHEN 'T' THEN 0.0000001 else Seasonal_Snow_Total+0 END DESC, Year DESC;")
                cursor.execute(query)
                row = cursor.fetchone()
                top10.append(Header_Snow)
                color_num = []
                color_value = []
                color_num = ["#26A4B6","#2DABBD","#33B0C2","#3AB5C7","#40BBCD","#47C0D1","#50C7D8","#5ACFDF","#64D5E5","#6EDBEB"]
                color_value = ["#9CF1FE","#A7F3FE","#ADF4FE","#B4F5FE","#BAF5FE","#C2F6FE","#C8F7FE","#D0F9FF","#D8F9FE","#DEF8FC"]
                
                for dcv in range(0,10):
                        #print(row_day)
                        year = str(row[0])
                        temp = str(row[2])
                        top10.append('<tr>' + '\n' +
                                                '<td bgcolor=' + color_num[dcv] + ' style="vertical-align: middle" align="center" colspan="1">' + '\n' +
                                                '<p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">' + str(dcv+1) + '<br />' +'\n'+
                                                '</p></td>')
                        top10.append('<td bgcolor=' + color_value[dcv] + ' style="vertical-align: middle" align="center" colspan="1">'
                                                '<p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;" >' + temp +  '<br />' +'\n'+
                                                '</p></td>' + '\n')
                        top10.append('<td bgcolor=' + color_value[dcv] + ' style="vertical-align: middle" align="center" colspan="1">'
                                                '<p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;" >' + year + '<br />' +'\n'+
                                                '</p></td></tr>' + '\n')
                        
                        row = cursor.fetchone()    
                top10.append(Footer)


                ## Get Top 10 least snowiest ##
                query = ("SELECT Year, Season, Seasonal_Snow_Total FROM climate.seasonally_"+site+" where Season = '" + season[i].upper() + "' AND Seasonal_Snow_Total != 'M' ORDER BY Case Seasonal_Snow_Total  WHEN 'T' THEN 0.0000001 else Seasonal_Snow_Total+0 END ASC, Year DESC;")
                cursor.execute(query)
                row = cursor.fetchone()
                top10.append(Header_LeastSnow)
                color_num = []
                color_value = []
                color_num = ["#26A4B6","#2DABBD","#33B0C2","#3AB5C7","#40BBCD","#47C0D1","#50C7D8","#5ACFDF","#64D5E5","#6EDBEB"]
                color_value = ["#9CF1FE","#A7F3FE","#ADF4FE","#B4F5FE","#BAF5FE","#C2F6FE","#C8F7FE","#D0F9FF","#D8F9FE","#DEF8FC"]
                
                for dcv in range(0,10):
                        #print(row_day)
                        year = str(row[0])
                        temp = str(row[2])
                        top10.append('<tr>' + '\n' +
                                                '<td bgcolor=' + color_num[dcv] + ' style="vertical-align: middle" align="center" colspan="1">' + '\n' +
                                                '<p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">' + str(dcv+1) + '<br />' +'\n'+
                                                '</p></td>')
                        top10.append('<td bgcolor=' + color_value[dcv] + ' style="vertical-align: middle" align="center" colspan="1">'
                                                '<p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;" >' + temp  + '<br />' +'\n'+
                                                '</p></td>' + '\n')
                        
                        top10.append('<td bgcolor=' + color_value[dcv] + ' style="vertical-align: middle" align="center" colspan="1">'
                                                '<p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;" >'  + year + '<br />' +'\n'+
                                                '</p></td></tr>' + '\n')
                        row = cursor.fetchone()    
                top10.append(Footer)
                
                top10.append( '<br /><br /><p style ="margin-top:1.8em;"></p>')

        ## Output files ##
        final = open(output_file,"w+")

        for j in range(0,len(top10)):
                text= top10[j]
                final.write(text)

        final.close()



        print('HTML file generated for '+site)
        print('Now creating pdf file for '+site)

        pdfkit.from_file( '../../PDFTxtFiles/Top10/Seasonally/' + site.upper() + '/seasonal.html', '../../PDFTxtFiles/Top10/Seasonally/' + site.upper() + '/seasonal.pdf')


print("Generating SEASONAL Top 10 files for NWS CLE")

for site in sites:
        htmlSite(site[0], site[1])

print(' Script completed and files genereated... ')

### End of main code ###
cursor.close()
cnx.close()