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
month = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'] #Used for Title in HTML
month_nm = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sept', 'oct', 'nov', 'dec'] #Naming html file
sites = [["cak", 1887],["cle", 1871],["eri", 1873],["mfd", 1899],["tol", 1871],["yng", 1896]]

### --- ###

### Main Code ###
def htmlSite(site, porStart):
        ## Intialize python lists to hold data ##
        cvg_top10 = []
        
        cvg_top10.append(
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
        output_file_cvg = '../../PDFTxtFiles/Top10/Monthly/'+site.upper()+'/monthly.html'
        ## -- ##
        
        for i in range(0,len(month)): # Main for loop to go through and create all data for each month
                Header_Warm_CVG = (
                                        '<table width="80%" cellpadding="3" align="center">' + '\n' + '<tr bgcolor="#000000">' + '\n' +
                                        '<td colspan="2">' + '\n' +
                                        '<p style="font-size: 16px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">'+ '\n' +
                                        site.upper()+' ' + month[i] + ' Top 10 Lists' + ' ('+str(porStart)+' - ' + current_year + ') ' + '</p></td>' + '\n' +
                                        '</tr>' + '\n' +
                                        '</table>' + '\n' +
                                        '<br />'+ '\n' +
                                        '<table cellspacing="0" cellpadding="3" border="1" align = "center" style="display:inline-block;margin:0em;">' + '\n' +
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

                Header_Cold = ('<table align="center" border="1" cellpadding="3" cellspacing="0" class="images" style="display:inline-block;margin:0em;">' + '\n' +
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

                Header_Wet = ('<table align="center" border="1" cellpadding="3" cellspacing="0" class="images" style="display:inline-block;margin:0em;">' + '\n' +
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

                Header_Dry = ('<table align="center" border="1" cellpadding="3" cellspacing="0" class="images" style="display:inline-block;margin:0em;">' + '\n' +
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

                Header_Snow = ('<table align="center" border="1" cellpadding="3" cellspacing="0" class="images" style="display:inline-block;margin:0em;">' + '\n' +
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
                Header_LeastSnow = ('<table align="center" border="1" cellpadding="3" cellspacing="0" class="images" style="display:inline-block;margin:0em;">' + '\n' +
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
                query_cvg = ("SELECT Year, Month, Monthly_Temp_Avg FROM climate.monthly_"+site+" where Month = " + str(i+1) + " AND Monthly_Temp_Avg != 'M' ORDER BY Monthly_Temp_Avg+0 DESC, Year DESC;")
                cursor.execute(query_cvg)
                row_cvg = cursor.fetchone()
                cvg_top10.append(Header_Warm_CVG)
                color_cvg_num = []
                color_cvg_value = []
                color_cvg_num = ["#A51B13","#AF231A","#B82D24","#C4372E","#CF4239","#D94E45","#E0564D","#E86057","#F06A61","#F7736A"]
                color_cvg_value = ["#FCB1AB","#FDBDB7","#FDC5C0","#FECECA","#FDD5D1","#FEDCD8","#FEE2DE","#FEE9E5","#FDEEEC","#FDF5F4"]

                for dcv in range(0,10):
                        #print(row_cvg)
                        year_cvg = str(row_cvg[0])
                        temp_cvg = str(row_cvg[2])
                        cvg_top10.append('<tr>' + '\n' +
                                                '<td bgcolor=' + color_cvg_num[dcv] + ' style="vertical-align: middle" align="center" colspan="1">' + '\n' +
                                                '<p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">' + str(dcv+1) + '<br />' +'\n'+
                                                '</p></td>')
                        cvg_top10.append('<td bgcolor=' + color_cvg_value[dcv] + ' style="vertical-align: middle" align="center" colspan="1">'
                                                '<p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;" >' + temp_cvg + '| ' + year_cvg + '<br />' +'\n'+
                                                '</p></td></tr>' + '\n')
                        row_cvg = cursor.fetchone()    
                cvg_top10.append(Footer)

                ## Get Top 10 coldest ##
                #CVG
                query_cvg = ("SELECT Year, Month, Monthly_Temp_Avg FROM climate.monthly_"+site+" where Month = " + str(i+1) + " AND Monthly_Temp_Avg != 'M' ORDER BY Monthly_Temp_Avg+0, Year DESC;")
                cursor.execute(query_cvg)
                row_cvg = cursor.fetchone()
                cvg_top10.append(Header_Cold)
                color_cvg_num = []
                color_cvg_value = []
                color_cvg_num = ["#3239C2","#3C43CA","#454CD1","#4E55D6","#555CDA","#6066DF","#6A70E5","#747AE9","#8187EF","#9095F5"]
                color_cvg_value = ["#9FA3FC","#A6AAFE","#ADB0FF","#B3B6FD","#BBBEFE","#C3C6FE","#C9CCFE","#D1D3FE","#D8DAFE","#E0E2FE"]

                for dcv in range(0,10):
                        #print(row_cvg)
                        year_cvg = str(row_cvg[0])
                        temp_cvg = str(row_cvg[2])
                        cvg_top10.append('<tr>' + '\n' +
                                                '<td bgcolor=' + color_cvg_num[dcv] + ' style="vertical-align: middle" align="center" colspan="1">' + '\n' +
                                                '<p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">' + str(dcv) + '<br />' +'\n'+
                                                '</p></td>')
                        cvg_top10.append('<td bgcolor=' + color_cvg_value[dcv] + ' style="vertical-align: middle" align="center" colspan="1">'
                                                '<p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;" >' + temp_cvg + '| ' + year_cvg + '<br />' +'\n'+
                                                '</p></td></tr>' + '\n')
                        row_cvg = cursor.fetchone()    
                cvg_top10.append(Footer)

                ## Get Top 10 wettest ##
                #CVG
                query_cvg = ("SELECT Year, Month, Monthly_Precip_Total FROM climate.monthly_"+site+" where Month = " + str(i+1) + " AND Monthly_Precip_Total != 'M' ORDER BY Monthly_Precip_Total+0 DESC, Year DESC;")
                cursor.execute(query_cvg)
                row_cvg = cursor.fetchone()
                cvg_top10.append(Header_Wet)
                color_cvg_num = []
                color_cvg_value = []
                color_cvg_num = ["#27AF17","#2EB71D","#35BD24","#3CC32B","#44CB33","#4BD13A","#52D641","#58DA48","#5FDF4F","#68E459"]
                color_cvg_value = ["#91FD84","#98FE8C","#9DFE91","#A2FE97","#AAFEA0","#B0FFA6","#B7FEAE","#BDFDB5","#C6FEBF","#CDFDC7"]

                for dcv in range(0,10):
                        #print(row_cvg)
                        year_cvg = str(row_cvg[0])
                        temp_cvg = str(row_cvg[2])
                        cvg_top10.append('<tr>' + '\n' +
                                                '<td bgcolor=' + color_cvg_num[dcv] + ' style="vertical-align: middle" align="center" colspan="1">' + '\n' +
                                                '<p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">' + str(dcv+1) + '<br />' +'\n'+
                                                '</p></td>')
                        cvg_top10.append('<td bgcolor=' + color_cvg_value[dcv] + ' style="vertical-align: middle" align="center" colspan="1">'
                                                '<p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;" >' + temp_cvg + '| ' + year_cvg + '<br />' +'\n'+
                                                '</p></td></tr>' + '\n')
                        row_cvg = cursor.fetchone()    
                cvg_top10.append(Footer)

                ## Get Top 10 driest ##
                #CVG
                query_cvg = ("SELECT Year, Month, Monthly_Precip_Total FROM climate.monthly_"+site+" where Month = " + str(i+1) + " AND Monthly_Precip_Total != 'M' ORDER BY Monthly_Precip_Total+0, Year DESC;")
                cursor.execute(query_cvg)
                row_cvg = cursor.fetchone()
                cvg_top10.append(Header_Dry)
                color_cvg_num = []
                color_cvg_value = []
                color_cvg_num = ["#BD9027","#C2952D","#C69A33","#CBA03A","#D1A641","#D8AD49","#DEB352","#E3B95A","#E8BF63","#EEC66D"]
                color_cvg_value = ["#FEDE96","#FEE09C","#FEE2A3","#FEE4AA","#FEE6B2","#FEE9B9","#FEEBBF","#FEEDC6","#FEEFCD","#FEF1D5"]

                for dcv in range(0,10):
                        #print(row_cvg)
                        year_cvg = str(row_cvg[0])
                        temp_cvg = str(row_cvg[2])
                        cvg_top10.append('<tr>' + '\n' +
                                                '<td bgcolor=' + color_cvg_num[dcv] + ' style="vertical-align: middle" align="center" colspan="1">' + '\n' +
                                                '<p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">' + str(dcv+1) + '<br />' +'\n'+
                                                '</p></td>')
                        cvg_top10.append('<td bgcolor=' + color_cvg_value[dcv] + ' style="vertical-align: middle" align="center" colspan="1">'
                                                '<p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;" >' + temp_cvg + '| ' + year_cvg + '<br />' +'\n'+
                                                '</p></td></tr>' + '\n')
                        row_cvg = cursor.fetchone()    
                cvg_top10.append(Footer)

                ## Get Top 10 snowiest ##
                #CVG
                query_cvg = ("SELECT Year, Month, Monthly_Snow_Total FROM climate.monthly_"+site+" where Month = " + str(i+1) + " AND Monthly_Snow_Total != 'M' AND Monthly_Snow_Total != 'T' ORDER BY Monthly_Snow_Total+0 DESC, Year DESC;")
                cursor.execute(query_cvg)
                row_cvg = cursor.fetchone()
                cvg_top10.append(Header_Snow)
                color_cvg_num = []
                color_cvg_value = []
                color_cvg_num = ["#26A4B6","#2DABBD","#33B0C2","#3AB5C7","#40BBCD","#47C0D1","#50C7D8","#5ACFDF","#64D5E5","#6EDBEB"]
                color_cvg_value = ["#9CF1FE","#A7F3FE","#ADF4FE","#B4F5FE","#BAF5FE","#C2F6FE","#C8F7FE","#D0F9FF","#D8F9FE","#DEF8FC"]
                
                for dcv in range(0,10):
                        #print(row_day)
                        year_cvg = str(row_cvg[0])
                        temp_cvg = str(row_cvg[2])
                        cvg_top10.append('<tr>' + '\n' +
                                                '<td bgcolor=' + color_cvg_num[dcv] + ' style="vertical-align: middle" align="center" colspan="1">' + '\n' +
                                                '<p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">' + str(dcv+1) + '<br />' +'\n'+
                                                '</p></td>')
                        cvg_top10.append('<td bgcolor=' + color_cvg_value[dcv] + ' style="vertical-align: middle" align="center" colspan="1">'
                                                '<p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;" >' + temp_cvg + '| ' + year_cvg + '<br />' +'\n'+
                                                '</p></td></tr>' + '\n')
                        row_cvg = cursor.fetchone()    
                cvg_top10.append(Footer)


                ## Get Top 10 least snowiest ##
                #CVG
                query_cvg = ("SELECT Year, Month, Monthly_Snow_Total FROM climate.monthly_"+site+" where Month = " + str(i+1) + " AND Monthly_Snow_Total != 'M' AND Monthly_Snow_Total != 'T' ORDER BY Monthly_Snow_Total+0 ASC, Year DESC;")
                cursor.execute(query_cvg)
                row_cvg = cursor.fetchone()
                cvg_top10.append(Header_LeastSnow)
                color_cvg_num = []
                color_cvg_value = []
                color_cvg_num = ["#26A4B6","#2DABBD","#33B0C2","#3AB5C7","#40BBCD","#47C0D1","#50C7D8","#5ACFDF","#64D5E5","#6EDBEB"]
                color_cvg_value = ["#9CF1FE","#A7F3FE","#ADF4FE","#B4F5FE","#BAF5FE","#C2F6FE","#C8F7FE","#D0F9FF","#D8F9FE","#DEF8FC"]
                
                for dcv in range(0,10):
                        #print(row_day)
                        year_cvg = str(row_cvg[0])
                        temp_cvg = str(row_cvg[2])
                        cvg_top10.append('<tr>' + '\n' +
                                                '<td bgcolor=' + color_cvg_num[dcv] + ' style="vertical-align: middle" align="center" colspan="1">' + '\n' +
                                                '<p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: white;font-weight: bold;vertical-align: middle;">' + str(dcv+1) + '<br />' +'\n'+
                                                '</p></td>')
                        cvg_top10.append('<td bgcolor=' + color_cvg_value[dcv] + ' style="vertical-align: middle" align="center" colspan="1">'
                                                '<p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;" >' + temp_cvg + '| ' + year_cvg + '<br />' +'\n'+
                                                '</p></td></tr>' + '\n')
                        row_cvg = cursor.fetchone()    
                cvg_top10.append(Footer)
                
                cvg_top10.append( '<br /><br /><p style ="margin-top:1.8em;"></p>')

        ## Output files ##
        final_cvg = open(output_file_cvg,"w+")

        for j in range(0,len(cvg_top10)):
                text_cvg= cvg_top10[j]
                final_cvg.write(text_cvg)

        final_cvg.close()




        print(' Now creating pdf files ')

        pdfkit.from_file( '../../PDFTxtFiles/Top10/Monthly/' + site.upper() + '/monthly.html', '../../PDFTxtFiles/Top10/Monthly/' + site.upper() + '/monthly.pdf')

print(' Script completed and files genereated... ')


for site in sites:
        htmlSite(site[0], site[1])


### End of main code ###
cursor.close()
cnx.close()