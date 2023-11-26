### Header ###
# Name: Brian Haines
# Date: 10/20/2015
# Purpose: Create a script that converts the LCD txt file to a pdf
# Version/ update history:
#    1) 10-20-15: Created script that converts all of the old CF6s to pdf files on the new webpage
#    2) 10-25-15: Script will now automatically convert current cf6 file to pdf and push it up to
#       the web via piggy back off of cliamte webpage cron on Todds computer
#    3) 02-02-16: Last day of month was being produced but was being overwritten by the next day. This
#       was due to on the 1st of the month the CF6 is for LAST month. Updated code to subtract 1 day so
#       file is on the 1st of the month is written with the month name of previous.

### Import modules ###
from fpdf import FPDF
from datetime import date, timedelta
import time
import glob

### Define date and times ###
current_month = ((date.today() - timedelta(days=1)).strftime("%b")).lower() # Display the current month minus a day in words
#print current_month
current_year = ((date.today() - timedelta(days=1)).strftime("%y")) # Display the current year minus a day
#print current_year
current_date = ((date.today() - timedelta(days=1)).strftime("%m%d"))
#print current_date
month_current = time.strftime("%Y/%m%d/") # Keep current month without subtracting a day so looks for correct CF6
#month_current = "2015/1101/"
#print month_current

### Define Constants ###
sites_cap = ['CMH', 'CVG', 'DAY']
sites_low = ['cmh', 'cvg', 'day']
day_input = 0 # Set to 0 and change only when CF6 file can be found
cmh_input = 0
cvg_input = 0
# DAY #
path_part_day = 'X:/Intranet/Archive/Prods/' + month_current + '*CLECF6DAY*'
for afile in glob.iglob(path_part_day):
    day_input = afile # If CF6 file found define it here

# CMH #
#path_part_cmh = '/data/ldad/data/'+ month_current + '*CLECF6CMH*'
path_part_cmh = 'X:/Intranet/Archive/Prods/' + month_current + '*CLECF6CMH*'
for afile in glob.iglob(path_part_cmh):
    cmh_input = afile

# CVG #
path_part_cvg = 'X:/Intranet/Archive/Prods/' + month_current + '*CLECF6CVG*'
for afile in glob.iglob(path_part_cvg):
    cvg_input = afile

### Convert new CF6 files and send to web ###
for y in range(len(sites_cap)):

    if sites_cap[y] == 'CMH':
        txt_file = cmh_input

    if sites_cap[y] == 'CVG':
        txt_file = cvg_input

    if sites_cap[y] == 'DAY':
        txt_file = day_input


    file_content = []

    ### Main ###
    file = open(txt_file)

    pdf=FPDF(unit='in',format=[10,11]) # Format the pdf document in the desired unit (width x length)
    pdf.add_page() # Add a page to the pdf document
    pdf.set_font('Courier','',12) # Set font to Arial in Bold with 12 point font

    for line in file:
        #print line
        splitline = line.split(' ')
        #print splitline
        #file_content.append([line])
        pdf.write(0.2,line) # Write the pdf file with the day output

    print ("Making file:" + str(current_month.lower()) + str(current_year))
    pdf.output('X:/Users/brian.haines/Projects/ClimateWebpage/PDFTxtFiles/LCDArchive/cms_media+climo_webpage+lcd_archive+' + sites_low[y] + '_lcd_'+ str(current_month) + str(current_year)+'.pdf','F') # Write 
	##
	## All "O:/" entries replaced with "X:/Apps/WinSCP/ldad_upload/data_ldad_public_nwswwas/"
	## in preparation for LDAD SAMBA deactivation.
	## 01/30/2017 - CTS
	##
    pdf.output('X:/Apps/WinSCP/ldad_upload/data_ldad_public_nwswwas/cms_media+climo_webpage+lcd_archive+' + sites_low[y] + '_lcd_'+ str(current_month) + str(current_year)+'.pdf','F')



############ Old section of code that converted all of the old CF6s
### Import modules ###
##from fpdf import FPDF
##
##site = "CMH"
##site1 = "cmh"
##
##month=["jan","feb","mar","apr","may","jun","jul","aug","sep","oct","nov","dec"]
##year=["96","97","98","99","00","01","02","03","04","05","06","07","08","09","10","11","12","13","14","15"]
##
##for y in range(len(year)):
##    for x in range(len(month)):
##
##        txt_file="X:/Users/brian.haines/Projects/ClimateWebpage/TxtFiles/LCDArchive/" + site + "/" + site1 + str(month[x]) + str(year[y])
##        file_content = []
##
##        ### Main ###
##        file = open(txt_file)
##
##        pdf=FPDF(unit='in',format=[10,11]) # Format the pdf document in the desired unit (width x length)
##        pdf.add_page() # Add a page to the pdf document
##        pdf.set_font('Courier','',12) # Set font to Arial in Bold with 12 point font
##
##        for line in file:
##            #print line
##            splitline = line.split(' ')
##            #print splitline
##            #file_content.append([line])
##            pdf.write(0.2,line) # Write the pdf file with the day output
##
##        print ("Making file:" + str(month[x]) + str(year[y]))
##        pdf.output('X:/Users/brian.haines/Projects/ClimateWebpage/PDFTxtFiles/LCDArchive/cms_media+climo_webpage+lcd_archive+' + site1 + '_lcd_'+ str(month[x]) + str(year[y])+'.pdf','F') # Write 
##        pdf.output('O:/cms_media+climo_webpage+lcd_archive+' + site1 + '_lcd_'+ str(month[x]) + str(year[y])+'.pdf','F')

