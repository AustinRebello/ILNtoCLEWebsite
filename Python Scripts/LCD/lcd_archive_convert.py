### Header ###
# Name: Austin Rebello
# Date: 11/26/2023
# Purpose: Create a script that converts the LCD txt file to a html and pdf file
# Version/ update history:
#    1) 11-26-2023 Full script written and completed

### Import modules ###
from datetime import date, timedelta
import time
from bs4 import BeautifulSoup as Soup
import requests
import pdfkit


def scrapeMonthYear(data):
    #Scrapes the month and year out of the archive to be used in file naming conventions
    monthIndex = data.find("MONTH")
    yearIndex = data.find("YEAR")
    month = data[monthIndex+11:monthIndex+23]
    month = month.strip(" \n")
    year = data[yearIndex+11:yearIndex+15]
    
    return month, year

def htmlSite(site):
    # Step 1: Create the URL and execute the request, then parse the data to grab the archive
    url = start_url + site + end_url
    html = requests.get(url).text
    soup = Soup(html, features="html.parser")
    data = str(soup.find("pre", class_= "glossaryProduct"))
    
    # Step 2: Prepare the HTML to write to file
    header = ('<table align="center" border="0" cellpadding="1" cellspacing="1" style="width: 750px;">'+ '\n' + '<tbody>'+ '\n' + '<tr>'+ '\n' + '<td style="vertical-align: middle" align="center" colspan="3"><p style="font-size: 14px;font-family: Tahoma, Geneva, sans-serif;TEXT-ALIGN: center;color: black;font-weight: bold;vertical-align: middle;">'+ '\n' +
                'Last Update: ' + current_date+ '\n' + '<br />'+ '\n' + '<br />'+ '\n' +
			    '</p></td>'+ '\n' +
                        '</tr>'+ '\n' +
                    '</tbody>'+ '\n' +
                        '</table>'+ '\n')
 
    ### Step 3: Export file as .html ###
    print(' Writing data to files... ')

    # Open output files for writing #
    month, year = scrapeMonthYear(data)
    output_file = '../../PDFTxtFiles/LCD/LCD_'+site+'_'+month+'_'+year+'.html'
    final_lcd = open(output_file,"w+") # Open cvg file for writing
    # - #
    
    final_lcd.write(header)
    final_lcd.write(data)
    final_lcd.write("<style> pre {text-align:center;}</style>")
    # - #
    ### --- ###

    ### Step 4: Close all the open files and generate pdf files ###
    final_lcd.close()

    # Create pdf files #
    print(' Now creating pdf files')
    pdfkit.from_file('../../PDFTxtFiles/LCD/LCD_'+site+'_'+month+'_'+year+'.html', '../../PDFTxtFiles/LCD/LCD_'+site+'_'+month+'_'+year+'.pdf')
 
 


current_date = (time.strftime("%Y-%m-%d")) # Current date
start_url = "https://forecast.weather.gov/product.php?site=CLE&issuedby="
end_url = "&product=CF6&format=CI&version=2&glossary=0"
sites = ["cak","cle","eri","mfd","tol","yng"]

for site in sites:
    htmlSite(site)