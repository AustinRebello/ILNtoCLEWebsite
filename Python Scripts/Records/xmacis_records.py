# Name: Brian Haines
# Date: 8/11/2015
# Purpose: Create a script that requests record data from xmacis and makes html files
# Version/ update history:
#    1) 8-8-15: Script completed!

#######################################
#Import modules required by Acis
import urllib.request as urlL
import json
#######################################
#######################################
#Import plotting tools
#import matplotlib.pyplot as plt
#import matplotlib.dates as mdates
#import matplotlib.ticker as ticker
import datetime
import time
#import numpy as np
import math
import pdfkit
#######################################
#Set Acis data server
base_url = "http://data.rcc-acis.org/"
sites = ["CAK", "CLE", "ERI", "MFD", "TOL", "YNG"]
#######################################
#Acis WebServices functions
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
#M A I N
###################################################
def run_script(site):
    if __name__ == "__main__":
        ### Defined Constants ###
        degree_sign= u'\N{DEGREE SIGN}' # The symbol for degrees
        mydate = datetime.datetime.now()
        cm = mydate.strftime("%B") # Current month
        current_date = (time.strftime("%Y-%m-%d"))

        #Ouput files#
        output_file_cle_jan = '../../PDFTxtFiles/Records/'+site+'/climate_records_'+site+'_jan.html'
        output_file_cle_feb = '../../PDFTxtFiles/Records/'+site+'/climate_records_'+site+'_feb.html'
        output_file_cle_mar = '../../PDFTxtFiles/Records/'+site+'/climate_records_'+site+'_mar.html'
        output_file_cle_apr = '../../PDFTxtFiles/Records/'+site+'/climate_records_'+site+'_apr.html'
        output_file_cle_may = '../../PDFTxtFiles/Records/'+site+'/climate_records_'+site+'_may.html'
        output_file_cle_jun = '../../PDFTxtFiles/Records/'+site+'/climate_records_'+site+'_jun.html'
        output_file_cle_jul = '../../PDFTxtFiles/Records/'+site+'/climate_records_'+site+'_jul.html'
        output_file_cle_aug = '../../PDFTxtFiles/Records/'+site+'/climate_records_'+site+'_aug.html'
        output_file_cle_sep = '../../PDFTxtFiles/Records/'+site+'/climate_records_'+site+'_sep.html'
        output_file_cle_oct = '../../PDFTxtFiles/Records/'+site+'/climate_records_'+site+'_oct.html'
        output_file_cle_nov = '../../PDFTxtFiles/Records/'+site+'/climate_records_'+site+'_nov.html'
        output_file_cle_dec = '../../PDFTxtFiles/Records/'+site+'/climate_records_'+site+'_dec.html'
        
        #Set parameters for data request
        params_maxt_maxt = {"sid":site+"thr","sdate":"por","edate":"por","elems":[{"name":"maxt","interval":"dly","duration":"dly","smry":{"reduce":"max","add":"date"},"smry_only":1,"groupby":"year"}]}
        params_mint_mint = {"sid":site+"thr","sdate":"por","edate":"por","elems":[{"name":"mint","interval":"dly","duration":"dly","smry":{"reduce":"min","add":"date"},"smry_only":1,"groupby":"year"}]}
        params_maxt_mint = {"sid":site+"thr","sdate":"por","edate":"por","elems":[{"name":"maxt","interval":"dly","duration":"dly","smry":{"reduce":"min","add":"date"},"smry_only":1,"groupby":"year"}]}
        params_mint_maxt = {"sid":site+"thr","sdate":"por","edate":"por","elems":[{"name":"mint","interval":"dly","duration":"dly","smry":{"reduce":"max","add":"date"},"smry_only":1,"groupby":"year"}]}
        params_precip = {"sid":site+"thr","sdate":"por","edate":"por","elems":[{"name":"pcpn","interval":"dly","duration":"dly","smry":{"reduce":"max","add":"date"},"smry_only":1,"groupby":"year"}]}
        params_snow = {"sid":site+"thr","sdate":"por","edate":"por","elems":[{"name":"snow","interval":"dly","duration":"dly","smry":{"reduce":"max","add":"date"},"smry_only":1,"groupby":"year"}]}
    
        #Obtain data
        data_maxt_maxt = GridData(params_maxt_maxt)
        data_mint_mint = GridData(params_mint_mint)
        data_maxt_mint = GridData(params_maxt_mint)
        data_mint_maxt = GridData(params_mint_maxt)
        data_precip = GridData(params_precip)
        data_snow = GridData(params_snow)

        
        records_cle = [] # Set up cmh list
        records_cle.append([]) # Add 1st dimension to cmh list
        records_cle.append([]) # Add 2nd dimension to cmh list
        records_cle.append([]) # Add 3rd dimension to cmh list
        records_cle.append([]) # Add 4th dimension to cmh list
        records_cle.append([]) # Add 5th dimension to cmh list
        records_cle.append([]) # Add 6th dimension to cmh list
        records_cle.append([]) # Add 7th dimension to cmh list
        records_cle.append([]) # Add 8th dimension to cmh list
        records_cle.append([]) # Add 9th dimension to cmh list
        records_cle.append([]) # Add 10th dimension to cmh list
        records_cle.append([]) # Add 11th dimension to cmh list
        records_cle.append([]) # Add 12th dimension to cmh list
        records_cle.append([]) # Add 13th dimension to cmh list

        January_Header = ('Last Update: ' + current_date + '<br>' + '<table>' + '\n' + '<tr valign="middle" align="center">' + '\n' + '<td bgcolor="#ffffcf" align="center" colspan="13">' + '\n' +
                        '<p><font size="+1"><strong>January Records<br /></strong></font></p></td></tr>' + '\n' +
                        '<tr><td bgcolor="#A6BB7B" align="center" style="background-color: rgb(192, 192, 192)" colspan="1" rowspan="2"><font size="3"><strong>Date<br /></strong></font></td>' + '\n' +
                        '<td bgcolor="#D2DDBD" align="center" style="background-color: rgb(252, 128, 134)" colspan="2"><font size="3"><strong>High<br /></strong></font></td>' + '\n' +
                '<td bgcolor="#D2DDBD" align="center" style="background-color: rgb(85, 144, 247)" colspan="2"><font size="3"><strong>Low<br />' + '\n' +
                '</strong></font></td>' + '\n' + '<td bgcolor="#A6BB7B" align="center" style="background-color: rgb(76, 217, 215)" colspan="2"><font size="3"><strong>Min. High<br />' + '\n' +
                '</strong></font></td>' + '\n' + '<td bgcolor="#A6BB7B" align="center" style="background-color: rgb(233, 182, 72)" colspan="2"><font size="3"><strong>Max Low<br />' + '\n' +
                '</strong></font></td>' + '\n' + '<td bgcolor="#D2DDBD" align="center" style="background-color: rgb(105, 194, 91)" colspan="2"><font size="3"><strong>Precipitation<br />' + '\n' +
                '</strong></font></td>' + '\n' + '<td bgcolor="#A6BB7B" align="center" style="background-color: rgb(149, 197, 193)" colspan="2"><font size="3"><strong>Snow<br />' + '\n' +
                '</strong></font></td></tr>' + '\n' + '<tr><td bgcolor="#D2DDBD" align="center" style="background-color: rgb(252, 162, 166)" colspan="1"><font size="3"><strong>Value<br />' + '\n' +
                        '</strong></font></td>' + '\n' + '<td bgcolor="#D2DDBD" align="center" style="background-color: rgb(252, 162, 166)" colspan="1"><font size="3"><strong>Year<br />' + '\n' +
                '</strong></font></td>' + '\n' + '<td bgcolor="#A6BB7B" align="center" style="background-color: rgb(128, 171, 246)" colspan="1"><font size="3"><strong>Value<br />' + '\n' +
                '</strong></font></td>' + '\n' + '<td bgcolor="#A6BB7B" align="center" style="background-color: rgb(128, 171, 246)" colspan="1"><font size="3"><strong>Year<br />' + '\n' +
                '</strong></font></td>' + '\n' + '<td bgcolor="#D2DDBD" align="center" style="background-color: rgb(109, 248, 246)" colspan="1"><font size="3"><strong>Value<br />' + '\n' +
                '</strong></font></td>' + '\n' + '<td bgcolor="#A6BB7B" align="center" style="background-color: rgb(109, 248, 246)" colspan="1"><font size="3"><strong>Year<br />' + '\n' +
                '</strong></font></td>' + '\n' + '<td bgcolor="#D2DDBD" align="center" style="background-color: rgb(248, 204, 109)" colspan="1"><font size="3"><strong>Value<br />' + '\n' +
                '</strong></font></td>' + '\n' + '<td bgcolor="#A6BB7B" align="center" style="background-color: rgb(248, 204, 109)" colspan="1"><font size="3"><strong>Year<br />' + '\n' +
                '</strong></font></td>' + '\n' + '<td bgcolor="#D2DDBD" align="center" style="background-color: rgb(124, 228, 104)" colspan="1"><font size="3"><strong>Value<br />' + '\n' +
                '</strong></font></td>' + '\n' + '<td bgcolor="#A6BB7B" align="center" style="background-color: rgb(124, 228, 104)" colspan="1"><font size="3"><strong>Year<br />' + '\n' +
                '</strong></font></td>' + '\n' + '<td bgcolor="#D2DDBD" align="center" style="background-color: rgb(178, 215, 212)" colspan="1"><font size="3"><strong>Value<br />' + '\n' +
                '</strong></font></td>' + '\n' + '<td bgcolor="#A6BB7B" align="center" style="background-color: rgb(178, 215, 212)" colspan="1"><font size="3"><strong>Year<br />' + '\n' + '</strong></font></td></tr>')

        February_Header = ('Last Update: ' + current_date + '<br>' + '<table>' + '\n' + '<tr valign="middle" align="center">' + '\n' + '<td bgcolor="#ffffcf" align="center" colspan="13">' + '\n' +
                        '<p><font size="+1"><strong>February Records<br /></strong></font></p></td></tr>' + '\n' +
                        '<tr><td bgcolor="#A6BB7B" align="center" style="background-color: rgb(192, 192, 192)" colspan="1" rowspan="2"><font size="3"><strong>Date<br /></strong></font></td>' + '\n' +
                        '<td bgcolor="#D2DDBD" align="center" style="background-color: rgb(252, 128, 134)" colspan="2"><font size="3"><strong>High<br /></strong></font></td>' + '\n' +
                '<td bgcolor="#D2DDBD" align="center" style="background-color: rgb(85, 144, 247)" colspan="2"><font size="3"><strong>Low<br />' + '\n' +
                '</strong></font></td>' + '\n' + '<td bgcolor="#A6BB7B" align="center" style="background-color: rgb(76, 217, 215)" colspan="2"><font size="3"><strong>Min. High<br />' + '\n' +
                '</strong></font></td>' + '\n' + '<td bgcolor="#A6BB7B" align="center" style="background-color: rgb(233, 182, 72)" colspan="2"><font size="3"><strong>Max Low<br />' + '\n' +
                '</strong></font></td>' + '\n' + '<td bgcolor="#D2DDBD" align="center" style="background-color: rgb(105, 194, 91)" colspan="2"><font size="3"><strong>Precipitation<br />' + '\n' +
                '</strong></font></td>' + '\n' + '<td bgcolor="#A6BB7B" align="center" style="background-color: rgb(149, 197, 193)" colspan="2"><font size="3"><strong>Snow<br />' + '\n' +
                '</strong></font></td></tr>' + '\n' + '<tr><td bgcolor="#D2DDBD" align="center" style="background-color: rgb(252, 162, 166)" colspan="1"><font size="3"><strong>Value<br />' + '\n' +
                        '</strong></font></td>' + '\n' + '<td bgcolor="#D2DDBD" align="center" style="background-color: rgb(252, 162, 166)" colspan="1"><font size="3"><strong>Year<br />' + '\n' +
                '</strong></font></td>' + '\n' + '<td bgcolor="#A6BB7B" align="center" style="background-color: rgb(128, 171, 246)" colspan="1"><font size="3"><strong>Value<br />' + '\n' +
                '</strong></font></td>' + '\n' + '<td bgcolor="#A6BB7B" align="center" style="background-color: rgb(128, 171, 246)" colspan="1"><font size="3"><strong>Year<br />' + '\n' +
                '</strong></font></td>' + '\n' + '<td bgcolor="#D2DDBD" align="center" style="background-color: rgb(109, 248, 246)" colspan="1"><font size="3"><strong>Value<br />' + '\n' +
                '</strong></font></td>' + '\n' + '<td bgcolor="#A6BB7B" align="center" style="background-color: rgb(109, 248, 246)" colspan="1"><font size="3"><strong>Year<br />' + '\n' +
                '</strong></font></td>' + '\n' + '<td bgcolor="#D2DDBD" align="center" style="background-color: rgb(248, 204, 109)" colspan="1"><font size="3"><strong>Value<br />' + '\n' +
                '</strong></font></td>' + '\n' + '<td bgcolor="#A6BB7B" align="center" style="background-color: rgb(248, 204, 109)" colspan="1"><font size="3"><strong>Year<br />' + '\n' +
                '</strong></font></td>' + '\n' + '<td bgcolor="#D2DDBD" align="center" style="background-color: rgb(124, 228, 104)" colspan="1"><font size="3"><strong>Value<br />' + '\n' +
                '</strong></font></td>' + '\n' + '<td bgcolor="#A6BB7B" align="center" style="background-color: rgb(124, 228, 104)" colspan="1"><font size="3"><strong>Year<br />' + '\n' +
                '</strong></font></td>' + '\n' + '<td bgcolor="#D2DDBD" align="center" style="background-color: rgb(178, 215, 212)" colspan="1"><font size="3"><strong>Value<br />' + '\n' +
                '</strong></font></td>' + '\n' + '<td bgcolor="#A6BB7B" align="center" style="background-color: rgb(178, 215, 212)" colspan="1"><font size="3"><strong>Year<br />' + '\n' + '</strong></font></td></tr>')

        March_Header = ('Last Update: ' + current_date + '<br>' + '<table>' + '\n' + '<tr valign="middle" align="center">' + '\n' + '<td bgcolor="#ffffcf" align="center" colspan="13">' + '\n' +
                        '<p><font size="+1"><strong>March Records<br /></strong></font></p></td></tr>' + '\n' +
                        '<tr><td bgcolor="#A6BB7B" align="center" style="background-color: rgb(192, 192, 192)" colspan="1" rowspan="2"><font size="3"><strong>Date<br /></strong></font></td>' + '\n' +
                        '<td bgcolor="#D2DDBD" align="center" style="background-color: rgb(252, 128, 134)" colspan="2"><font size="3"><strong>High<br /></strong></font></td>' + '\n' +
                '<td bgcolor="#D2DDBD" align="center" style="background-color: rgb(85, 144, 247)" colspan="2"><font size="3"><strong>Low<br />' + '\n' +
                '</strong></font></td>' + '\n' + '<td bgcolor="#A6BB7B" align="center" style="background-color: rgb(76, 217, 215)" colspan="2"><font size="3"><strong>Min. High<br />' + '\n' +
                '</strong></font></td>' + '\n' + '<td bgcolor="#A6BB7B" align="center" style="background-color: rgb(233, 182, 72)" colspan="2"><font size="3"><strong>Max Low<br />' + '\n' +
                '</strong></font></td>' + '\n' + '<td bgcolor="#D2DDBD" align="center" style="background-color: rgb(105, 194, 91)" colspan="2"><font size="3"><strong>Precipitation<br />' + '\n' +
                '</strong></font></td>' + '\n' + '<td bgcolor="#A6BB7B" align="center" style="background-color: rgb(149, 197, 193)" colspan="2"><font size="3"><strong>Snow<br />' + '\n' +
                '</strong></font></td></tr>' + '\n' + '<tr><td bgcolor="#D2DDBD" align="center" style="background-color: rgb(252, 162, 166)" colspan="1"><font size="3"><strong>Value<br />' + '\n' +
                        '</strong></font></td>' + '\n' + '<td bgcolor="#D2DDBD" align="center" style="background-color: rgb(252, 162, 166)" colspan="1"><font size="3"><strong>Year<br />' + '\n' +
                '</strong></font></td>' + '\n' + '<td bgcolor="#A6BB7B" align="center" style="background-color: rgb(128, 171, 246)" colspan="1"><font size="3"><strong>Value<br />' + '\n' +
                '</strong></font></td>' + '\n' + '<td bgcolor="#A6BB7B" align="center" style="background-color: rgb(128, 171, 246)" colspan="1"><font size="3"><strong>Year<br />' + '\n' +
                '</strong></font></td>' + '\n' + '<td bgcolor="#D2DDBD" align="center" style="background-color: rgb(109, 248, 246)" colspan="1"><font size="3"><strong>Value<br />' + '\n' +
                '</strong></font></td>' + '\n' + '<td bgcolor="#A6BB7B" align="center" style="background-color: rgb(109, 248, 246)" colspan="1"><font size="3"><strong>Year<br />' + '\n' +
                '</strong></font></td>' + '\n' + '<td bgcolor="#D2DDBD" align="center" style="background-color: rgb(248, 204, 109)" colspan="1"><font size="3"><strong>Value<br />' + '\n' +
                '</strong></font></td>' + '\n' + '<td bgcolor="#A6BB7B" align="center" style="background-color: rgb(248, 204, 109)" colspan="1"><font size="3"><strong>Year<br />' + '\n' +
                '</strong></font></td>' + '\n' + '<td bgcolor="#D2DDBD" align="center" style="background-color: rgb(124, 228, 104)" colspan="1"><font size="3"><strong>Value<br />' + '\n' +
                '</strong></font></td>' + '\n' + '<td bgcolor="#A6BB7B" align="center" style="background-color: rgb(124, 228, 104)" colspan="1"><font size="3"><strong>Year<br />' + '\n' +
                '</strong></font></td>' + '\n' + '<td bgcolor="#D2DDBD" align="center" style="background-color: rgb(178, 215, 212)" colspan="1"><font size="3"><strong>Value<br />' + '\n' +
                '</strong></font></td>' + '\n' + '<td bgcolor="#A6BB7B" align="center" style="background-color: rgb(178, 215, 212)" colspan="1"><font size="3"><strong>Year<br />' + '\n' + '</strong></font></td></tr>')

        April_Header = ('Last Update: ' + current_date + '<br>' + '<table>' + '\n' + '<tr valign="middle" align="center">' + '\n' + '<td bgcolor="#ffffcf" align="center" colspan="13">' + '\n' +
                        '<p><font size="+1"><strong>April Records<br /></strong></font></p></td></tr>' + '\n' +
                        '<tr><td bgcolor="#A6BB7B" align="center" style="background-color: rgb(192, 192, 192)" colspan="1" rowspan="2"><font size="3"><strong>Date<br /></strong></font></td>' + '\n' +
                        '<td bgcolor="#D2DDBD" align="center" style="background-color: rgb(252, 128, 134)" colspan="2"><font size="3"><strong>High<br /></strong></font></td>' + '\n' +
                '<td bgcolor="#D2DDBD" align="center" style="background-color: rgb(85, 144, 247)" colspan="2"><font size="3"><strong>Low<br />' + '\n' +
                '</strong></font></td>' + '\n' + '<td bgcolor="#A6BB7B" align="center" style="background-color: rgb(76, 217, 215)" colspan="2"><font size="3"><strong>Min. High<br />' + '\n' +
                '</strong></font></td>' + '\n' + '<td bgcolor="#A6BB7B" align="center" style="background-color: rgb(233, 182, 72)" colspan="2"><font size="3"><strong>Max Low<br />' + '\n' +
                '</strong></font></td>' + '\n' + '<td bgcolor="#D2DDBD" align="center" style="background-color: rgb(105, 194, 91)" colspan="2"><font size="3"><strong>Precipitation<br />' + '\n' +
                '</strong></font></td>' + '\n' + '<td bgcolor="#A6BB7B" align="center" style="background-color: rgb(149, 197, 193)" colspan="2"><font size="3"><strong>Snow<br />' + '\n' +
                '</strong></font></td></tr>' + '\n' + '<tr><td bgcolor="#D2DDBD" align="center" style="background-color: rgb(252, 162, 166)" colspan="1"><font size="3"><strong>Value<br />' + '\n' +
                        '</strong></font></td>' + '\n' + '<td bgcolor="#D2DDBD" align="center" style="background-color: rgb(252, 162, 166)" colspan="1"><font size="3"><strong>Year<br />' + '\n' +
                '</strong></font></td>' + '\n' + '<td bgcolor="#A6BB7B" align="center" style="background-color: rgb(128, 171, 246)" colspan="1"><font size="3"><strong>Value<br />' + '\n' +
                '</strong></font></td>' + '\n' + '<td bgcolor="#A6BB7B" align="center" style="background-color: rgb(128, 171, 246)" colspan="1"><font size="3"><strong>Year<br />' + '\n' +
                '</strong></font></td>' + '\n' + '<td bgcolor="#D2DDBD" align="center" style="background-color: rgb(109, 248, 246)" colspan="1"><font size="3"><strong>Value<br />' + '\n' +
                '</strong></font></td>' + '\n' + '<td bgcolor="#A6BB7B" align="center" style="background-color: rgb(109, 248, 246)" colspan="1"><font size="3"><strong>Year<br />' + '\n' +
                '</strong></font></td>' + '\n' + '<td bgcolor="#D2DDBD" align="center" style="background-color: rgb(248, 204, 109)" colspan="1"><font size="3"><strong>Value<br />' + '\n' +
                '</strong></font></td>' + '\n' + '<td bgcolor="#A6BB7B" align="center" style="background-color: rgb(248, 204, 109)" colspan="1"><font size="3"><strong>Year<br />' + '\n' +
                '</strong></font></td>' + '\n' + '<td bgcolor="#D2DDBD" align="center" style="background-color: rgb(124, 228, 104)" colspan="1"><font size="3"><strong>Value<br />' + '\n' +
                '</strong></font></td>' + '\n' + '<td bgcolor="#A6BB7B" align="center" style="background-color: rgb(124, 228, 104)" colspan="1"><font size="3"><strong>Year<br />' + '\n' +
                '</strong></font></td>' + '\n' + '<td bgcolor="#D2DDBD" align="center" style="background-color: rgb(178, 215, 212)" colspan="1"><font size="3"><strong>Value<br />' + '\n' +
                '</strong></font></td>' + '\n' + '<td bgcolor="#A6BB7B" align="center" style="background-color: rgb(178, 215, 212)" colspan="1"><font size="3"><strong>Year<br />' + '\n' + '</strong></font></td></tr>')

        May_Header = ('Last Update: ' + current_date + '<br>' + '<table>' + '\n' + '<tr valign="middle" align="center">' + '\n' + '<td bgcolor="#ffffcf" align="center" colspan="13">' + '\n' +
                        '<p><font size="+1"><strong>May Records<br /></strong></font></p></td></tr>' + '\n' +
                        '<tr><td bgcolor="#A6BB7B" align="center" style="background-color: rgb(192, 192, 192)" colspan="1" rowspan="2"><font size="3"><strong>Date<br /></strong></font></td>' + '\n' +
                        '<td bgcolor="#D2DDBD" align="center" style="background-color: rgb(252, 128, 134)" colspan="2"><font size="3"><strong>High<br /></strong></font></td>' + '\n' +
                '<td bgcolor="#D2DDBD" align="center" style="background-color: rgb(85, 144, 247)" colspan="2"><font size="3"><strong>Low<br />' + '\n' +
                '</strong></font></td>' + '\n' + '<td bgcolor="#A6BB7B" align="center" style="background-color: rgb(76, 217, 215)" colspan="2"><font size="3"><strong>Min. High<br />' + '\n' +
                '</strong></font></td>' + '\n' + '<td bgcolor="#A6BB7B" align="center" style="background-color: rgb(233, 182, 72)" colspan="2"><font size="3"><strong>Max Low<br />' + '\n' +
                '</strong></font></td>' + '\n' + '<td bgcolor="#D2DDBD" align="center" style="background-color: rgb(105, 194, 91)" colspan="2"><font size="3"><strong>Precipitation<br />' + '\n' +
                '</strong></font></td>' + '\n' + '<td bgcolor="#A6BB7B" align="center" style="background-color: rgb(149, 197, 193)" colspan="2"><font size="3"><strong>Snow<br />' + '\n' +
                '</strong></font></td></tr>' + '\n' + '<tr><td bgcolor="#D2DDBD" align="center" style="background-color: rgb(252, 162, 166)" colspan="1"><font size="3"><strong>Value<br />' + '\n' +
                        '</strong></font></td>' + '\n' + '<td bgcolor="#D2DDBD" align="center" style="background-color: rgb(252, 162, 166)" colspan="1"><font size="3"><strong>Year<br />' + '\n' +
                '</strong></font></td>' + '\n' + '<td bgcolor="#A6BB7B" align="center" style="background-color: rgb(128, 171, 246)" colspan="1"><font size="3"><strong>Value<br />' + '\n' +
                '</strong></font></td>' + '\n' + '<td bgcolor="#A6BB7B" align="center" style="background-color: rgb(128, 171, 246)" colspan="1"><font size="3"><strong>Year<br />' + '\n' +
                '</strong></font></td>' + '\n' + '<td bgcolor="#D2DDBD" align="center" style="background-color: rgb(109, 248, 246)" colspan="1"><font size="3"><strong>Value<br />' + '\n' +
                '</strong></font></td>' + '\n' + '<td bgcolor="#A6BB7B" align="center" style="background-color: rgb(109, 248, 246)" colspan="1"><font size="3"><strong>Year<br />' + '\n' +
                '</strong></font></td>' + '\n' + '<td bgcolor="#D2DDBD" align="center" style="background-color: rgb(248, 204, 109)" colspan="1"><font size="3"><strong>Value<br />' + '\n' +
                '</strong></font></td>' + '\n' + '<td bgcolor="#A6BB7B" align="center" style="background-color: rgb(248, 204, 109)" colspan="1"><font size="3"><strong>Year<br />' + '\n' +
                '</strong></font></td>' + '\n' + '<td bgcolor="#D2DDBD" align="center" style="background-color: rgb(124, 228, 104)" colspan="1"><font size="3"><strong>Value<br />' + '\n' +
                '</strong></font></td>' + '\n' + '<td bgcolor="#A6BB7B" align="center" style="background-color: rgb(124, 228, 104)" colspan="1"><font size="3"><strong>Year<br />' + '\n' +
                '</strong></font></td>' + '\n' + '<td bgcolor="#D2DDBD" align="center" style="background-color: rgb(178, 215, 212)" colspan="1"><font size="3"><strong>Value<br />' + '\n' +
                '</strong></font></td>' + '\n' + '<td bgcolor="#A6BB7B" align="center" style="background-color: rgb(178, 215, 212)" colspan="1"><font size="3"><strong>Year<br />' + '\n' + '</strong></font></td></tr>')

        June_Header = ('Last Update: ' + current_date + '<br>' + '<table>' + '\n' + '<tr valign="middle" align="center">' + '\n' + '<td bgcolor="#ffffcf" align="center" colspan="13">' + '\n' +
                        '<p><font size="+1"><strong>June Records<br /></strong></font></p></td></tr>' + '\n' +
                        '<tr><td bgcolor="#A6BB7B" align="center" style="background-color: rgb(192, 192, 192)" colspan="1" rowspan="2"><font size="3"><strong>Date<br /></strong></font></td>' + '\n' +
                        '<td bgcolor="#D2DDBD" align="center" style="background-color: rgb(252, 128, 134)" colspan="2"><font size="3"><strong>High<br /></strong></font></td>' + '\n' +
                '<td bgcolor="#D2DDBD" align="center" style="background-color: rgb(85, 144, 247)" colspan="2"><font size="3"><strong>Low<br />' + '\n' +
                '</strong></font></td>' + '\n' + '<td bgcolor="#A6BB7B" align="center" style="background-color: rgb(76, 217, 215)" colspan="2"><font size="3"><strong>Min. High<br />' + '\n' +
                '</strong></font></td>' + '\n' + '<td bgcolor="#A6BB7B" align="center" style="background-color: rgb(233, 182, 72)" colspan="2"><font size="3"><strong>Max Low<br />' + '\n' +
                '</strong></font></td>' + '\n' + '<td bgcolor="#D2DDBD" align="center" style="background-color: rgb(105, 194, 91)" colspan="2"><font size="3"><strong>Precipitation<br />' + '\n' +
                '</strong></font></td>' + '\n' + '<td bgcolor="#A6BB7B" align="center" style="background-color: rgb(149, 197, 193)" colspan="2"><font size="3"><strong>Snow<br />' + '\n' +
                '</strong></font></td></tr>' + '\n' + '<tr><td bgcolor="#D2DDBD" align="center" style="background-color: rgb(252, 162, 166)" colspan="1"><font size="3"><strong>Value<br />' + '\n' +
                        '</strong></font></td>' + '\n' + '<td bgcolor="#D2DDBD" align="center" style="background-color: rgb(252, 162, 166)" colspan="1"><font size="3"><strong>Year<br />' + '\n' +
                '</strong></font></td>' + '\n' + '<td bgcolor="#A6BB7B" align="center" style="background-color: rgb(128, 171, 246)" colspan="1"><font size="3"><strong>Value<br />' + '\n' +
                '</strong></font></td>' + '\n' + '<td bgcolor="#A6BB7B" align="center" style="background-color: rgb(128, 171, 246)" colspan="1"><font size="3"><strong>Year<br />' + '\n' +
                '</strong></font></td>' + '\n' + '<td bgcolor="#D2DDBD" align="center" style="background-color: rgb(109, 248, 246)" colspan="1"><font size="3"><strong>Value<br />' + '\n' +
                '</strong></font></td>' + '\n' + '<td bgcolor="#A6BB7B" align="center" style="background-color: rgb(109, 248, 246)" colspan="1"><font size="3"><strong>Year<br />' + '\n' +
                '</strong></font></td>' + '\n' + '<td bgcolor="#D2DDBD" align="center" style="background-color: rgb(248, 204, 109)" colspan="1"><font size="3"><strong>Value<br />' + '\n' +
                '</strong></font></td>' + '\n' + '<td bgcolor="#A6BB7B" align="center" style="background-color: rgb(248, 204, 109)" colspan="1"><font size="3"><strong>Year<br />' + '\n' +
                '</strong></font></td>' + '\n' + '<td bgcolor="#D2DDBD" align="center" style="background-color: rgb(124, 228, 104)" colspan="1"><font size="3"><strong>Value<br />' + '\n' +
                '</strong></font></td>' + '\n' + '<td bgcolor="#A6BB7B" align="center" style="background-color: rgb(124, 228, 104)" colspan="1"><font size="3"><strong>Year<br />' + '\n' +
                '</strong></font></td>' + '\n' + '<td bgcolor="#D2DDBD" align="center" style="background-color: rgb(178, 215, 212)" colspan="1"><font size="3"><strong>Value<br />' + '\n' +
                '</strong></font></td>' + '\n' + '<td bgcolor="#A6BB7B" align="center" style="background-color: rgb(178, 215, 212)" colspan="1"><font size="3"><strong>Year<br />' + '\n' + '</strong></font></td></tr>')

        July_Header = ('Last Update: ' + current_date + '<br>' + '<table>' + '\n' + '<tr valign="middle" align="center">' + '\n' + '<td bgcolor="#ffffcf" align="center" colspan="13">' + '\n' +
                        '<p><font size="+1"><strong>July Records<br /></strong></font></p></td></tr>' + '\n' +
                        '<tr><td bgcolor="#A6BB7B" align="center" style="background-color: rgb(192, 192, 192)" colspan="1" rowspan="2"><font size="3"><strong>Date<br /></strong></font></td>' + '\n' +
                        '<td bgcolor="#D2DDBD" align="center" style="background-color: rgb(252, 128, 134)" colspan="2"><font size="3"><strong>High<br /></strong></font></td>' + '\n' +
                '<td bgcolor="#D2DDBD" align="center" style="background-color: rgb(85, 144, 247)" colspan="2"><font size="3"><strong>Low<br />' + '\n' +
                '</strong></font></td>' + '\n' + '<td bgcolor="#A6BB7B" align="center" style="background-color: rgb(76, 217, 215)" colspan="2"><font size="3"><strong>Min. High<br />' + '\n' +
                '</strong></font></td>' + '\n' + '<td bgcolor="#A6BB7B" align="center" style="background-color: rgb(233, 182, 72)" colspan="2"><font size="3"><strong>Max Low<br />' + '\n' +
                '</strong></font></td>' + '\n' + '<td bgcolor="#D2DDBD" align="center" style="background-color: rgb(105, 194, 91)" colspan="2"><font size="3"><strong>Precipitation<br />' + '\n' +
                '</strong></font></td>' + '\n' + '<td bgcolor="#A6BB7B" align="center" style="background-color: rgb(149, 197, 193)" colspan="2"><font size="3"><strong>Snow<br />' + '\n' +
                '</strong></font></td></tr>' + '\n' + '<tr><td bgcolor="#D2DDBD" align="center" style="background-color: rgb(252, 162, 166)" colspan="1"><font size="3"><strong>Value<br />' + '\n' +
                        '</strong></font></td>' + '\n' + '<td bgcolor="#D2DDBD" align="center" style="background-color: rgb(252, 162, 166)" colspan="1"><font size="3"><strong>Year<br />' + '\n' +
                '</strong></font></td>' + '\n' + '<td bgcolor="#A6BB7B" align="center" style="background-color: rgb(128, 171, 246)" colspan="1"><font size="3"><strong>Value<br />' + '\n' +
                '</strong></font></td>' + '\n' + '<td bgcolor="#A6BB7B" align="center" style="background-color: rgb(128, 171, 246)" colspan="1"><font size="3"><strong>Year<br />' + '\n' +
                '</strong></font></td>' + '\n' + '<td bgcolor="#D2DDBD" align="center" style="background-color: rgb(109, 248, 246)" colspan="1"><font size="3"><strong>Value<br />' + '\n' +
                '</strong></font></td>' + '\n' + '<td bgcolor="#A6BB7B" align="center" style="background-color: rgb(109, 248, 246)" colspan="1"><font size="3"><strong>Year<br />' + '\n' +
                '</strong></font></td>' + '\n' + '<td bgcolor="#D2DDBD" align="center" style="background-color: rgb(248, 204, 109)" colspan="1"><font size="3"><strong>Value<br />' + '\n' +
                '</strong></font></td>' + '\n' + '<td bgcolor="#A6BB7B" align="center" style="background-color: rgb(248, 204, 109)" colspan="1"><font size="3"><strong>Year<br />' + '\n' +
                '</strong></font></td>' + '\n' + '<td bgcolor="#D2DDBD" align="center" style="background-color: rgb(124, 228, 104)" colspan="1"><font size="3"><strong>Value<br />' + '\n' +
                '</strong></font></td>' + '\n' + '<td bgcolor="#A6BB7B" align="center" style="background-color: rgb(124, 228, 104)" colspan="1"><font size="3"><strong>Year<br />' + '\n' +
                '</strong></font></td>' + '\n' + '<td bgcolor="#D2DDBD" align="center" style="background-color: rgb(178, 215, 212)" colspan="1"><font size="3"><strong>Value<br />' + '\n' +
                '</strong></font></td>' + '\n' + '<td bgcolor="#A6BB7B" align="center" style="background-color: rgb(178, 215, 212)" colspan="1"><font size="3"><strong>Year<br />' + '\n' + '</strong></font></td></tr>')

        August_Header = ('Last Update: ' + current_date + '<br>' + '<table>' + '\n' + '<tr valign="middle" align="center">' + '\n' + '<td bgcolor="#ffffcf" align="center" colspan="13">' + '\n' +
                        '<p><font size="+1"><strong>August Records<br /></strong></font></p></td></tr>' + '\n' +
                        '<tr><td bgcolor="#A6BB7B" align="center" style="background-color: rgb(192, 192, 192)" colspan="1" rowspan="2"><font size="3"><strong>Date<br /></strong></font></td>' + '\n' +
                        '<td bgcolor="#D2DDBD" align="center" style="background-color: rgb(252, 128, 134)" colspan="2"><font size="3"><strong>High<br /></strong></font></td>' + '\n' +
                '<td bgcolor="#D2DDBD" align="center" style="background-color: rgb(85, 144, 247)" colspan="2"><font size="3"><strong>Low<br />' + '\n' +
                '</strong></font></td>' + '\n' + '<td bgcolor="#A6BB7B" align="center" style="background-color: rgb(76, 217, 215)" colspan="2"><font size="3"><strong>Min. High<br />' + '\n' +
                '</strong></font></td>' + '\n' + '<td bgcolor="#A6BB7B" align="center" style="background-color: rgb(233, 182, 72)" colspan="2"><font size="3"><strong>Max Low<br />' + '\n' +
                '</strong></font></td>' + '\n' + '<td bgcolor="#D2DDBD" align="center" style="background-color: rgb(105, 194, 91)" colspan="2"><font size="3"><strong>Precipitation<br />' + '\n' +
                '</strong></font></td>' + '\n' + '<td bgcolor="#A6BB7B" align="center" style="background-color: rgb(149, 197, 193)" colspan="2"><font size="3"><strong>Snow<br />' + '\n' +
                '</strong></font></td></tr>' + '\n' + '<tr><td bgcolor="#D2DDBD" align="center" style="background-color: rgb(252, 162, 166)" colspan="1"><font size="3"><strong>Value<br />' + '\n' +
                        '</strong></font></td>' + '\n' + '<td bgcolor="#D2DDBD" align="center" style="background-color: rgb(252, 162, 166)" colspan="1"><font size="3"><strong>Year<br />' + '\n' +
                '</strong></font></td>' + '\n' + '<td bgcolor="#A6BB7B" align="center" style="background-color: rgb(128, 171, 246)" colspan="1"><font size="3"><strong>Value<br />' + '\n' +
                '</strong></font></td>' + '\n' + '<td bgcolor="#A6BB7B" align="center" style="background-color: rgb(128, 171, 246)" colspan="1"><font size="3"><strong>Year<br />' + '\n' +
                '</strong></font></td>' + '\n' + '<td bgcolor="#D2DDBD" align="center" style="background-color: rgb(109, 248, 246)" colspan="1"><font size="3"><strong>Value<br />' + '\n' +
                '</strong></font></td>' + '\n' + '<td bgcolor="#A6BB7B" align="center" style="background-color: rgb(109, 248, 246)" colspan="1"><font size="3"><strong>Year<br />' + '\n' +
                '</strong></font></td>' + '\n' + '<td bgcolor="#D2DDBD" align="center" style="background-color: rgb(248, 204, 109)" colspan="1"><font size="3"><strong>Value<br />' + '\n' +
                '</strong></font></td>' + '\n' + '<td bgcolor="#A6BB7B" align="center" style="background-color: rgb(248, 204, 109)" colspan="1"><font size="3"><strong>Year<br />' + '\n' +
                '</strong></font></td>' + '\n' + '<td bgcolor="#D2DDBD" align="center" style="background-color: rgb(124, 228, 104)" colspan="1"><font size="3"><strong>Value<br />' + '\n' +
                '</strong></font></td>' + '\n' + '<td bgcolor="#A6BB7B" align="center" style="background-color: rgb(124, 228, 104)" colspan="1"><font size="3"><strong>Year<br />' + '\n' +
                '</strong></font></td>' + '\n' + '<td bgcolor="#D2DDBD" align="center" style="background-color: rgb(178, 215, 212)" colspan="1"><font size="3"><strong>Value<br />' + '\n' +
                '</strong></font></td>' + '\n' + '<td bgcolor="#A6BB7B" align="center" style="background-color: rgb(178, 215, 212)" colspan="1"><font size="3"><strong>Year<br />' + '\n' + '</strong></font></td></tr>')

        September_Header = ('Last Update: ' + current_date + '<br>' + '<table>' + '\n' + '<tr valign="middle" align="center">' + '\n' + '<td bgcolor="#ffffcf" align="center" colspan="13">' + '\n' +
                        '<p><font size="+1"><strong>September Records<br /></strong></font></p></td></tr>' + '\n' +
                        '<tr><td bgcolor="#A6BB7B" align="center" style="background-color: rgb(192, 192, 192)" colspan="1" rowspan="2"><font size="3"><strong>Date<br /></strong></font></td>' + '\n' +
                        '<td bgcolor="#D2DDBD" align="center" style="background-color: rgb(252, 128, 134)" colspan="2"><font size="3"><strong>High<br /></strong></font></td>' + '\n' +
                '<td bgcolor="#D2DDBD" align="center" style="background-color: rgb(85, 144, 247)" colspan="2"><font size="3"><strong>Low<br />' + '\n' +
                '</strong></font></td>' + '\n' + '<td bgcolor="#A6BB7B" align="center" style="background-color: rgb(76, 217, 215)" colspan="2"><font size="3"><strong>Min. High<br />' + '\n' +
                '</strong></font></td>' + '\n' + '<td bgcolor="#A6BB7B" align="center" style="background-color: rgb(233, 182, 72)" colspan="2"><font size="3"><strong>Max Low<br />' + '\n' +
                '</strong></font></td>' + '\n' + '<td bgcolor="#D2DDBD" align="center" style="background-color: rgb(105, 194, 91)" colspan="2"><font size="3"><strong>Precipitation<br />' + '\n' +
                '</strong></font></td>' + '\n' + '<td bgcolor="#A6BB7B" align="center" style="background-color: rgb(149, 197, 193)" colspan="2"><font size="3"><strong>Snow<br />' + '\n' +
                '</strong></font></td></tr>' + '\n' + '<tr><td bgcolor="#D2DDBD" align="center" style="background-color: rgb(252, 162, 166)" colspan="1"><font size="3"><strong>Value<br />' + '\n' +
                        '</strong></font></td>' + '\n' + '<td bgcolor="#D2DDBD" align="center" style="background-color: rgb(252, 162, 166)" colspan="1"><font size="3"><strong>Year<br />' + '\n' +
                '</strong></font></td>' + '\n' + '<td bgcolor="#A6BB7B" align="center" style="background-color: rgb(128, 171, 246)" colspan="1"><font size="3"><strong>Value<br />' + '\n' +
                '</strong></font></td>' + '\n' + '<td bgcolor="#A6BB7B" align="center" style="background-color: rgb(128, 171, 246)" colspan="1"><font size="3"><strong>Year<br />' + '\n' +
                '</strong></font></td>' + '\n' + '<td bgcolor="#D2DDBD" align="center" style="background-color: rgb(109, 248, 246)" colspan="1"><font size="3"><strong>Value<br />' + '\n' +
                '</strong></font></td>' + '\n' + '<td bgcolor="#A6BB7B" align="center" style="background-color: rgb(109, 248, 246)" colspan="1"><font size="3"><strong>Year<br />' + '\n' +
                '</strong></font></td>' + '\n' + '<td bgcolor="#D2DDBD" align="center" style="background-color: rgb(248, 204, 109)" colspan="1"><font size="3"><strong>Value<br />' + '\n' +
                '</strong></font></td>' + '\n' + '<td bgcolor="#A6BB7B" align="center" style="background-color: rgb(248, 204, 109)" colspan="1"><font size="3"><strong>Year<br />' + '\n' +
                '</strong></font></td>' + '\n' + '<td bgcolor="#D2DDBD" align="center" style="background-color: rgb(124, 228, 104)" colspan="1"><font size="3"><strong>Value<br />' + '\n' +
                '</strong></font></td>' + '\n' + '<td bgcolor="#A6BB7B" align="center" style="background-color: rgb(124, 228, 104)" colspan="1"><font size="3"><strong>Year<br />' + '\n' +
                '</strong></font></td>' + '\n' + '<td bgcolor="#D2DDBD" align="center" style="background-color: rgb(178, 215, 212)" colspan="1"><font size="3"><strong>Value<br />' + '\n' +
                '</strong></font></td>' + '\n' + '<td bgcolor="#A6BB7B" align="center" style="background-color: rgb(178, 215, 212)" colspan="1"><font size="3"><strong>Year<br />' + '\n' + '</strong></font></td></tr>')

        October_Header = ('Last Update: ' + current_date + '<br>' + '<table>' + '\n' + '<tr valign="middle" align="center">' + '\n' + '<td bgcolor="#ffffcf" align="center" colspan="13">' + '\n' +
                        '<p><font size="+1"><strong>October Records<br /></strong></font></p></td></tr>' + '\n' +
                        '<tr><td bgcolor="#A6BB7B" align="center" style="background-color: rgb(192, 192, 192)" colspan="1" rowspan="2"><font size="3"><strong>Date<br /></strong></font></td>' + '\n' +
                        '<td bgcolor="#D2DDBD" align="center" style="background-color: rgb(252, 128, 134)" colspan="2"><font size="3"><strong>High<br /></strong></font></td>' + '\n' +
                '<td bgcolor="#D2DDBD" align="center" style="background-color: rgb(85, 144, 247)" colspan="2"><font size="3"><strong>Low<br />' + '\n' +
                '</strong></font></td>' + '\n' + '<td bgcolor="#A6BB7B" align="center" style="background-color: rgb(76, 217, 215)" colspan="2"><font size="3"><strong>Min. High<br />' + '\n' +
                '</strong></font></td>' + '\n' + '<td bgcolor="#A6BB7B" align="center" style="background-color: rgb(233, 182, 72)" colspan="2"><font size="3"><strong>Max Low<br />' + '\n' +
                '</strong></font></td>' + '\n' + '<td bgcolor="#D2DDBD" align="center" style="background-color: rgb(105, 194, 91)" colspan="2"><font size="3"><strong>Precipitation<br />' + '\n' +
                '</strong></font></td>' + '\n' + '<td bgcolor="#A6BB7B" align="center" style="background-color: rgb(149, 197, 193)" colspan="2"><font size="3"><strong>Snow<br />' + '\n' +
                '</strong></font></td></tr>' + '\n' + '<tr><td bgcolor="#D2DDBD" align="center" style="background-color: rgb(252, 162, 166)" colspan="1"><font size="3"><strong>Value<br />' + '\n' +
                        '</strong></font></td>' + '\n' + '<td bgcolor="#D2DDBD" align="center" style="background-color: rgb(252, 162, 166)" colspan="1"><font size="3"><strong>Year<br />' + '\n' +
                '</strong></font></td>' + '\n' + '<td bgcolor="#A6BB7B" align="center" style="background-color: rgb(128, 171, 246)" colspan="1"><font size="3"><strong>Value<br />' + '\n' +
                '</strong></font></td>' + '\n' + '<td bgcolor="#A6BB7B" align="center" style="background-color: rgb(128, 171, 246)" colspan="1"><font size="3"><strong>Year<br />' + '\n' +
                '</strong></font></td>' + '\n' + '<td bgcolor="#D2DDBD" align="center" style="background-color: rgb(109, 248, 246)" colspan="1"><font size="3"><strong>Value<br />' + '\n' +
                '</strong></font></td>' + '\n' + '<td bgcolor="#A6BB7B" align="center" style="background-color: rgb(109, 248, 246)" colspan="1"><font size="3"><strong>Year<br />' + '\n' +
                '</strong></font></td>' + '\n' + '<td bgcolor="#D2DDBD" align="center" style="background-color: rgb(248, 204, 109)" colspan="1"><font size="3"><strong>Value<br />' + '\n' +
                '</strong></font></td>' + '\n' + '<td bgcolor="#A6BB7B" align="center" style="background-color: rgb(248, 204, 109)" colspan="1"><font size="3"><strong>Year<br />' + '\n' +
                '</strong></font></td>' + '\n' + '<td bgcolor="#D2DDBD" align="center" style="background-color: rgb(124, 228, 104)" colspan="1"><font size="3"><strong>Value<br />' + '\n' +
                '</strong></font></td>' + '\n' + '<td bgcolor="#A6BB7B" align="center" style="background-color: rgb(124, 228, 104)" colspan="1"><font size="3"><strong>Year<br />' + '\n' +
                '</strong></font></td>' + '\n' + '<td bgcolor="#D2DDBD" align="center" style="background-color: rgb(178, 215, 212)" colspan="1"><font size="3"><strong>Value<br />' + '\n' +
                '</strong></font></td>' + '\n' + '<td bgcolor="#A6BB7B" align="center" style="background-color: rgb(178, 215, 212)" colspan="1"><font size="3"><strong>Year<br />' + '\n' + '</strong></font></td></tr>')

        November_Header = ('Last Update: ' + current_date + '<br>' + '<table>' + '\n' + '<tr valign="middle" align="center">' + '\n' + '<td bgcolor="#ffffcf" align="center" colspan="13">' + '\n' +
                        '<p><font size="+1"><strong>November Records<br /></strong></font></p></td></tr>' + '\n' +
                        '<tr><td bgcolor="#A6BB7B" align="center" style="background-color: rgb(192, 192, 192)" colspan="1" rowspan="2"><font size="3"><strong>Date<br /></strong></font></td>' + '\n' +
                        '<td bgcolor="#D2DDBD" align="center" style="background-color: rgb(252, 128, 134)" colspan="2"><font size="3"><strong>High<br /></strong></font></td>' + '\n' +
                '<td bgcolor="#D2DDBD" align="center" style="background-color: rgb(85, 144, 247)" colspan="2"><font size="3"><strong>Low<br />' + '\n' +
                '</strong></font></td>' + '\n' + '<td bgcolor="#A6BB7B" align="center" style="background-color: rgb(76, 217, 215)" colspan="2"><font size="3"><strong>Min. High<br />' + '\n' +
                '</strong></font></td>' + '\n' + '<td bgcolor="#A6BB7B" align="center" style="background-color: rgb(233, 182, 72)" colspan="2"><font size="3"><strong>Max Low<br />' + '\n' +
                '</strong></font></td>' + '\n' + '<td bgcolor="#D2DDBD" align="center" style="background-color: rgb(105, 194, 91)" colspan="2"><font size="3"><strong>Precipitation<br />' + '\n' +
                '</strong></font></td>' + '\n' + '<td bgcolor="#A6BB7B" align="center" style="background-color: rgb(149, 197, 193)" colspan="2"><font size="3"><strong>Snow<br />' + '\n' +
                '</strong></font></td></tr>' + '\n' + '<tr><td bgcolor="#D2DDBD" align="center" style="background-color: rgb(252, 162, 166)" colspan="1"><font size="3"><strong>Value<br />' + '\n' +
                        '</strong></font></td>' + '\n' + '<td bgcolor="#D2DDBD" align="center" style="background-color: rgb(252, 162, 166)" colspan="1"><font size="3"><strong>Year<br />' + '\n' +
                '</strong></font></td>' + '\n' + '<td bgcolor="#A6BB7B" align="center" style="background-color: rgb(128, 171, 246)" colspan="1"><font size="3"><strong>Value<br />' + '\n' +
                '</strong></font></td>' + '\n' + '<td bgcolor="#A6BB7B" align="center" style="background-color: rgb(128, 171, 246)" colspan="1"><font size="3"><strong>Year<br />' + '\n' +
                '</strong></font></td>' + '\n' + '<td bgcolor="#D2DDBD" align="center" style="background-color: rgb(109, 248, 246)" colspan="1"><font size="3"><strong>Value<br />' + '\n' +
                '</strong></font></td>' + '\n' + '<td bgcolor="#A6BB7B" align="center" style="background-color: rgb(109, 248, 246)" colspan="1"><font size="3"><strong>Year<br />' + '\n' +
                '</strong></font></td>' + '\n' + '<td bgcolor="#D2DDBD" align="center" style="background-color: rgb(248, 204, 109)" colspan="1"><font size="3"><strong>Value<br />' + '\n' +
                '</strong></font></td>' + '\n' + '<td bgcolor="#A6BB7B" align="center" style="background-color: rgb(248, 204, 109)" colspan="1"><font size="3"><strong>Year<br />' + '\n' +
                '</strong></font></td>' + '\n' + '<td bgcolor="#D2DDBD" align="center" style="background-color: rgb(124, 228, 104)" colspan="1"><font size="3"><strong>Value<br />' + '\n' +
                '</strong></font></td>' + '\n' + '<td bgcolor="#A6BB7B" align="center" style="background-color: rgb(124, 228, 104)" colspan="1"><font size="3"><strong>Year<br />' + '\n' +
                '</strong></font></td>' + '\n' + '<td bgcolor="#D2DDBD" align="center" style="background-color: rgb(178, 215, 212)" colspan="1"><font size="3"><strong>Value<br />' + '\n' +
                '</strong></font></td>' + '\n' + '<td bgcolor="#A6BB7B" align="center" style="background-color: rgb(178, 215, 212)" colspan="1"><font size="3"><strong>Year<br />' + '\n' + '</strong></font></td></tr>')

        December_Header = ('Last Update: ' + current_date + '<br>' + '<table>' + '\n' + '<tr valign="middle" align="center">' + '\n' + '<td bgcolor="#ffffcf" align="center" colspan="13">' + '\n' +
                        '<p><font size="+1"><strong>December Records<br /></strong></font></p></td></tr>' + '\n' +
                        '<tr><td bgcolor="#A6BB7B" align="center" style="background-color: rgb(192, 192, 192)" colspan="1" rowspan="2"><font size="3"><strong>Date<br /></strong></font></td>' + '\n' +
                        '<td bgcolor="#D2DDBD" align="center" style="background-color: rgb(252, 128, 134)" colspan="2"><font size="3"><strong>High<br /></strong></font></td>' + '\n' +
                '<td bgcolor="#D2DDBD" align="center" style="background-color: rgb(85, 144, 247)" colspan="2"><font size="3"><strong>Low<br />' + '\n' +
                '</strong></font></td>' + '\n' + '<td bgcolor="#A6BB7B" align="center" style="background-color: rgb(76, 217, 215)" colspan="2"><font size="3"><strong>Min. High<br />' + '\n' +
                '</strong></font></td>' + '\n' + '<td bgcolor="#A6BB7B" align="center" style="background-color: rgb(233, 182, 72)" colspan="2"><font size="3"><strong>Max Low<br />' + '\n' +
                '</strong></font></td>' + '\n' + '<td bgcolor="#D2DDBD" align="center" style="background-color: rgb(105, 194, 91)" colspan="2"><font size="3"><strong>Precipitation<br />' + '\n' +
                '</strong></font></td>' + '\n' + '<td bgcolor="#A6BB7B" align="center" style="background-color: rgb(149, 197, 193)" colspan="2"><font size="3"><strong>Snow<br />' + '\n' +
                '</strong></font></td></tr>' + '\n' + '<tr><td bgcolor="#D2DDBD" align="center" style="background-color: rgb(252, 162, 166)" colspan="1"><font size="3"><strong>Value<br />' + '\n' +
                        '</strong></font></td>' + '\n' + '<td bgcolor="#D2DDBD" align="center" style="background-color: rgb(252, 162, 166)" colspan="1"><font size="3"><strong>Year<br />' + '\n' +
                '</strong></font></td>' + '\n' + '<td bgcolor="#A6BB7B" align="center" style="background-color: rgb(128, 171, 246)" colspan="1"><font size="3"><strong>Value<br />' + '\n' +
                '</strong></font></td>' + '\n' + '<td bgcolor="#A6BB7B" align="center" style="background-color: rgb(128, 171, 246)" colspan="1"><font size="3"><strong>Year<br />' + '\n' +
                '</strong></font></td>' + '\n' + '<td bgcolor="#D2DDBD" align="center" style="background-color: rgb(109, 248, 246)" colspan="1"><font size="3"><strong>Value<br />' + '\n' +
                '</strong></font></td>' + '\n' + '<td bgcolor="#A6BB7B" align="center" style="background-color: rgb(109, 248, 246)" colspan="1"><font size="3"><strong>Year<br />' + '\n' +
                '</strong></font></td>' + '\n' + '<td bgcolor="#D2DDBD" align="center" style="background-color: rgb(248, 204, 109)" colspan="1"><font size="3"><strong>Value<br />' + '\n' +
                '</strong></font></td>' + '\n' + '<td bgcolor="#A6BB7B" align="center" style="background-color: rgb(248, 204, 109)" colspan="1"><font size="3"><strong>Year<br />' + '\n' +
                '</strong></font></td>' + '\n' + '<td bgcolor="#D2DDBD" align="center" style="background-color: rgb(124, 228, 104)" colspan="1"><font size="3"><strong>Value<br />' + '\n' +
                '</strong></font></td>' + '\n' + '<td bgcolor="#A6BB7B" align="center" style="background-color: rgb(124, 228, 104)" colspan="1"><font size="3"><strong>Year<br />' + '\n' +
                '</strong></font></td>' + '\n' + '<td bgcolor="#D2DDBD" align="center" style="background-color: rgb(178, 215, 212)" colspan="1"><font size="3"><strong>Value<br />' + '\n' +
                '</strong></font></td>' + '\n' + '<td bgcolor="#A6BB7B" align="center" style="background-color: rgb(178, 215, 212)" colspan="1"><font size="3"><strong>Year<br />' + '\n' + '</strong></font></td></tr>')


        January_Footer = ('\n' + '</table>')
        
        #a=data_maxt_maxt.items()
        #records_cle[0].append(January_Header)
        for d in data_maxt_maxt['smry']:
            for i in range(0, len(d)):
                splitline=str(d[i]).split(',')
                if (int(splitline[1][10:12]) < 10):
                    if (i == 0):
                        records_cle[0].append(January_Header + '<tr><td align="center" style="background-color:rgb(232,232,232)">' + splitline[1][10:12].strip("0") + '</td>')
                        records_cle[1].append('<td bgcolor="#D2DDBD" align="center" style="background-color:rgb(250,195,197)"><font size="3"><strong>' + splitline[0][2:4] + '<br></strong></font></td>')
                        records_cle[2].append('<td bgcolor="#D2DDBD" align="center" style="background-color:rgb(250,195,197)"><font size="3"><strong>' + splitline[1][2:6] + '<br></strong></font></td>')
                        #break
                    elif ( i == 31  ):
                        records_cle[0].append(February_Header + '<tr><td align="center" style="background-color:rgb(232,232,232)">' + splitline[1][10:12].strip("0") + '</td>')
                        records_cle[1].append('<td bgcolor="#D2DDBD" align="center" style="background-color:rgb(250,195,197)"><font size="3"><strong>' + splitline[0][2:4] + '<br></strong></font></td>')
                        records_cle[2].append('<td bgcolor="#D2DDBD" align="center" style="background-color:rgb(250,195,197)"><font size="3"><strong>' + splitline[1][2:6] + '<br></strong></font></td>')
                    elif ( i == 60  ):
                        records_cle[0].append(March_Header + '<tr><td align="center" style="background-color:rgb(232,232,232)">' + splitline[1][10:12].strip("0") + '</td>')
                        records_cle[1].append('<td bgcolor="#D2DDBD" align="center" style="background-color:rgb(250,195,197)"><font size="3"><strong>' + splitline[0][2:4] + '<br></strong></font></td>')
                        records_cle[2].append('<td bgcolor="#D2DDBD" align="center" style="background-color:rgb(250,195,197)"><font size="3"><strong>' + splitline[1][2:6] + '<br></strong></font></td>')
                    elif ( i == 91  ):
                        records_cle[0].append(April_Header + '<tr><td align="center" style="background-color:rgb(232,232,232)">' + splitline[1][10:12].strip("0") + '</td>')
                        records_cle[1].append('<td bgcolor="#D2DDBD" align="center" style="background-color:rgb(250,195,197)"><font size="3"><strong>' + splitline[0][2:4] + '<br></strong></font></td>')
                        records_cle[2].append('<td bgcolor="#D2DDBD" align="center" style="background-color:rgb(250,195,197)"><font size="3"><strong>' + splitline[1][2:6] + '<br></strong></font></td>')
                    elif ( i == 121  ):
                        records_cle[0].append(May_Header + '<tr><td align="center" style="background-color:rgb(232,232,232)">' + splitline[1][10:12].strip("0") + '</td>')
                        records_cle[1].append('<td bgcolor="#D2DDBD" align="center" style="background-color:rgb(250,195,197)"><font size="3"><strong>' + splitline[0][2:4] + '<br></strong></font></td>')
                        records_cle[2].append('<td bgcolor="#D2DDBD" align="center" style="background-color:rgb(250,195,197)"><font size="3"><strong>' + splitline[1][2:6] + '<br></strong></font></td>')
                    elif ( i == 152  ):
                        records_cle[0].append(June_Header + '<tr><td align="center" style="background-color:rgb(232,232,232)">' + splitline[1][10:12].strip("0") + '</td>')
                        records_cle[1].append('<td bgcolor="#D2DDBD" align="center" style="background-color:rgb(250,195,197)"><font size="3"><strong>' + splitline[0][2:5].strip("'") + '<br></strong></font></td>')
                        records_cle[2].append('<td bgcolor="#D2DDBD" align="center" style="background-color:rgb(250,195,197)"><font size="3"><strong>' + splitline[1][2:6] + '<br></strong></font></td>')
                    elif ( i == 182  ):
                        records_cle[0].append(July_Header + '<tr><td align="center" style="background-color:rgb(232,232,232)">' + splitline[1][10:12].strip("0") + '</td>')
                        records_cle[1].append('<td bgcolor="#D2DDBD" align="center" style="background-color:rgb(250,195,197)"><font size="3"><strong>' + splitline[0][2:5].strip("'") + '<br></strong></font></td>')
                        records_cle[2].append('<td bgcolor="#D2DDBD" align="center" style="background-color:rgb(250,195,197)"><font size="3"><strong>' + splitline[1][2:6] + '<br></strong></font></td>')
                    elif ( i == 213  ):
                        records_cle[0].append(August_Header + '<tr><td align="center" style="background-color:rgb(232,232,232)">' + splitline[1][10:12].strip("0") + '</td>')
                        records_cle[1].append('<td bgcolor="#D2DDBD" align="center" style="background-color:rgb(250,195,197)"><font size="3"><strong>' + splitline[0][2:5].strip("'") + '<br></strong></font></td>')
                        records_cle[2].append('<td bgcolor="#D2DDBD" align="center" style="background-color:rgb(250,195,197)"><font size="3"><strong>' + splitline[1][2:6] + '<br></strong></font></td>')
                    elif ( i == 244  ):
                        records_cle[0].append(September_Header + '<tr><td align="center" style="background-color:rgb(232,232,232)">' + splitline[1][10:12].strip("0") + '</td>')
                        records_cle[1].append('<td bgcolor="#D2DDBD" align="center" style="background-color:rgb(250,195,197)"><font size="3"><strong>' + splitline[0][2:5].strip("'") + '<br></strong></font></td>')
                        records_cle[2].append('<td bgcolor="#D2DDBD" align="center" style="background-color:rgb(250,195,197)"><font size="3"><strong>' + splitline[1][2:6] + '<br></strong></font></td>')
                    elif ( i == 274  ):
                        records_cle[0].append(October_Header + '<tr><td align="center" style="background-color:rgb(232,232,232)">' + splitline[1][10:12].strip("0") + '</td>')
                        records_cle[1].append('<td bgcolor="#D2DDBD" align="center" style="background-color:rgb(250,195,197)"><font size="3"><strong>' + splitline[0][2:5].strip("'") + '<br></strong></font></td>')
                        records_cle[2].append('<td bgcolor="#D2DDBD" align="center" style="background-color:rgb(250,195,197)"><font size="3"><strong>' + splitline[1][2:6] + '<br></strong></font></td>')
                    elif ( i == 305  ):
                        records_cle[0].append(November_Header + '<tr><td align="center" style="background-color:rgb(232,232,232)">' + splitline[1][10:12].strip("0") + '</td>')
                        records_cle[1].append('<td bgcolor="#D2DDBD" align="center" style="background-color:rgb(250,195,197)"><font size="3"><strong>' + splitline[0][2:5].strip("'") + '<br></strong></font></td>')
                        records_cle[2].append('<td bgcolor="#D2DDBD" align="center" style="background-color:rgb(250,195,197)"><font size="3"><strong>' + splitline[1][2:6] + '<br></strong></font></td>')
                    elif ( i == 335  ):
                        records_cle[0].append(December_Header + '<tr><td align="center" style="background-color:rgb(232,232,232)">' + splitline[1][10:12].strip("0") + '</td>')
                        records_cle[1].append('<td bgcolor="#D2DDBD" align="center" style="background-color:rgb(250,195,197)"><font size="3"><strong>' + splitline[0][2:5].strip("'") + '<br></strong></font></td>')
                        records_cle[2].append('<td bgcolor="#D2DDBD" align="center" style="background-color:rgb(250,195,197)"><font size="3"><strong>' + splitline[1][2:6] + '<br></strong></font></td>')
                                        
                                                        
                    else:
                        records_cle[0].append('<tr><td align="center" style="background-color:rgb(232,232,232)">' + splitline[1][10:12].strip("0") + '</td>')
                        records_cle[1].append('<td bgcolor="#D2DDBD" align="center" style="background-color:rgb(250,195,197)"><font size="3"><strong>' + splitline[0][2:5].strip("'") + '<br></strong></font></td>')
                        records_cle[2].append('<td bgcolor="#D2DDBD" align="center" style="background-color:rgb(250,195,197)"><font size="3"><strong>' + splitline[1][2:6] + '<br></strong></font></td>')
                        #break
                elif (int(splitline[1][10:12]) >= 10):
                    records_cle[0].append('<tr><td align="center" style="background-color:rgb(232,232,232)">' + splitline[1][10:12] + '</td>')
                    records_cle[1].append('<td bgcolor="#D2DDBD" align="center" style="background-color:rgb(250,195,197)"><font size="3"><strong>' + splitline[0][2:5].strip("'") + '<br></strong></font></td>')
                    records_cle[2].append('<td bgcolor="#D2DDBD" align="center" style="background-color:rgb(250,195,197)"><font size="3"><strong>' + splitline[1][2:6] + '<br></strong></font></td>')

        for d1 in data_mint_mint['smry']:
            for i1 in range(0, len(d1)):
                splitline=str(d1[i1]).split(',')
                records_cle[3].append('<td bgcolor="#D2DDBD" align="center" style="background-color:rgb(186,207,243)"><font size="3"><strong>' + splitline[0][2:5].strip("'") + '<br></strong></font></td>')
                records_cle[4].append('<td bgcolor="#D2DDBD" align="center" style="background-color:rgb(186,207,243)"><font size="3"><strong>' + splitline[1][2:6] + '<br></strong></font></td>')

        for d2 in data_maxt_mint['smry']:
            for i2 in range(0, len(d2)):
                splitline=str(d2[i2]).split(',')
                records_cle[5].append('<td bgcolor="#D2DDBD" align="center" style="background-color:rgb(199, 242, 243)"><font size="3"><strong>' + splitline[0][2:4].strip("'") + '<br></strong></font></td>')
                records_cle[6].append('<td bgcolor="#D2DDBD" align="center" style="background-color:rgb(199, 242, 243)"><font size="3"><strong>' + splitline[1][2:6] + '<br></strong></font></td>')

        for d3 in data_mint_maxt['smry']:
            for i3 in range(0, len(d3)):
                splitline=str(d3[i3]).split(',')
                records_cle[7].append('<td bgcolor="#D2DDBD" align="center" style="background-color:rgb(242, 224, 185)"><font size="3"><strong>' + splitline[0][2:4] + '<br></strong></font></td>')
                records_cle[8].append('<td bgcolor="#D2DDBD" align="center" style="background-color:rgb(242, 224, 185)"><font size="3"><strong>' + splitline[1][2:6] + '<br></strong></font></td>')

        for d4 in data_precip['smry']:
            for i4 in range(0, len(d4)):
                splitline=str(d4[i4]).split(',')
                records_cle[9].append('<td bgcolor="#D2DDBD" align="center" style="background-color:rgb(193, 242, 183)"><font size="3"><strong>' + splitline[0][2:6] + '<br></strong></font></td>')
                records_cle[10].append('<td bgcolor="#D2DDBD" align="center" style="background-color:rgb(193, 242, 183)"><font size="3"><strong>' + splitline[1][2:6] + '<br></strong></font></td>')

        for d5 in data_snow['smry']:
            for i5 in range(0, len(d5)):
                splitline=str(d5[i5]).split(',')
                if (int(splitline[1][10:12]) == 31):
                    records_cle[11].append('<td bgcolor="#D2DDBD" align="center" style="background-color:rgb(211, 239, 237)"><font size="3"><strong>' + splitline[0][2:6].strip("'") + '<br></strong></font></td>')
                    records_cle[12].append('<td bgcolor="#D2DDBD" align="center" style="background-color:rgb(211, 239, 237)"><font size="3"><strong>' + splitline[1][2:6] + '<br></strong></font></td></tr>' + January_Footer + '\n')
                elif ( i5 == 59 ):
                    records_cle[11].append('<td bgcolor="#D2DDBD" align="center" style="background-color:rgb(211, 239, 237)"><font size="3"><strong>' + splitline[0][2:6].strip("'") + '<br></strong></font></td>')
                    records_cle[12].append('<td bgcolor="#D2DDBD" align="center" style="background-color:rgb(211, 239, 237)"><font size="3"><strong>' + splitline[1][2:6] + '<br></strong></font></td></tr>' + January_Footer + '\n')
                elif ( i5 == 90 ):
                    records_cle[11].append('<td bgcolor="#D2DDBD" align="center" style="background-color:rgb(211, 239, 237)"><font size="3"><strong>' + splitline[0][2:6].strip("'") + '<br></strong></font></td>')
                    records_cle[12].append('<td bgcolor="#D2DDBD" align="center" style="background-color:rgb(211, 239, 237)"><font size="3"><strong>' + splitline[1][2:6] + '<br></strong></font></td></tr>' + January_Footer + '\n')
                elif ( i5 == 120 ):
                    records_cle[11].append('<td bgcolor="#D2DDBD" align="center" style="background-color:rgb(211, 239, 237)"><font size="3"><strong>' + splitline[0][2:6].strip("'") + '<br></strong></font></td>')
                    records_cle[12].append('<td bgcolor="#D2DDBD" align="center" style="background-color:rgb(211, 239, 237)"><font size="3"><strong>' + splitline[1][2:6] + '<br></strong></font></td></tr>' + January_Footer + '\n')
                elif ( i5 == 120 ):
                    records_cle[11].append('<td bgcolor="#D2DDBD" align="center" style="background-color:rgb(211, 239, 237)"><font size="3"><strong>' + splitline[0][2:6].strip("'") + '<br></strong></font></td>')
                    records_cle[12].append('<td bgcolor="#D2DDBD" align="center" style="background-color:rgb(211, 239, 237)"><font size="3"><strong>' + splitline[1][2:6] + '<br></strong></font></td></tr>' + January_Footer + '\n')
                elif ( i5 == 151 ):
                    records_cle[11].append('<td bgcolor="#D2DDBD" align="center" style="background-color:rgb(211, 239, 237)"><font size="3"><strong>' + splitline[0][2:6].strip("'") + '<br></strong></font></td>')
                    records_cle[12].append('<td bgcolor="#D2DDBD" align="center" style="background-color:rgb(211, 239, 237)"><font size="3"><strong>' + splitline[1][2:6] + '<br></strong></font></td></tr>' + January_Footer + '\n')
                elif ( i5 == 181 ):
                    records_cle[11].append('<td bgcolor="#D2DDBD" align="center" style="background-color:rgb(211, 239, 237)"><font size="3"><strong>' + splitline[0][2:6].strip("'") + '<br></strong></font></td>')
                    records_cle[12].append('<td bgcolor="#D2DDBD" align="center" style="background-color:rgb(211, 239, 237)"><font size="3"><strong>' + splitline[1][2:6] + '<br></strong></font></td></tr>' + January_Footer + '\n')
                elif ( i5 == 212 ):
                    records_cle[11].append('<td bgcolor="#D2DDBD" align="center" style="background-color:rgb(211, 239, 237)"><font size="3"><strong>' + splitline[0][2:6].strip("'") + '<br></strong></font></td>')
                    records_cle[12].append('<td bgcolor="#D2DDBD" align="center" style="background-color:rgb(211, 239, 237)"><font size="3"><strong>' + splitline[1][2:6] + '<br></strong></font></td></tr>' + January_Footer + '\n')
                elif ( i5 == 243 ):
                    records_cle[11].append('<td bgcolor="#D2DDBD" align="center" style="background-color:rgb(211, 239, 237)"><font size="3"><strong>' + splitline[0][2:6].strip("'") + '<br></strong></font></td>')
                    records_cle[12].append('<td bgcolor="#D2DDBD" align="center" style="background-color:rgb(211, 239, 237)"><font size="3"><strong>' + splitline[1][2:6] + '<br></strong></font></td></tr>' + January_Footer + '\n')
                elif ( i5 == 273 ):
                    records_cle[11].append('<td bgcolor="#D2DDBD" align="center" style="background-color:rgb(211, 239, 237)"><font size="3"><strong>' + splitline[0][2:6].strip("'") + '<br></strong></font></td>')
                    records_cle[12].append('<td bgcolor="#D2DDBD" align="center" style="background-color:rgb(211, 239, 237)"><font size="3"><strong>' + splitline[1][2:6] + '<br></strong></font></td></tr>' + January_Footer + '\n')
                elif ( i5 == 304 ):
                    records_cle[11].append('<td bgcolor="#D2DDBD" align="center" style="background-color:rgb(211, 239, 237)"><font size="3"><strong>' + splitline[0][2:6].strip("'") + '<br></strong></font></td>')
                    records_cle[12].append('<td bgcolor="#D2DDBD" align="center" style="background-color:rgb(211, 239, 237)"><font size="3"><strong>' + splitline[1][2:6] + '<br></strong></font></td></tr>' + January_Footer + '\n')
                elif ( i5 == 334 ):
                    records_cle[11].append('<td bgcolor="#D2DDBD" align="center" style="background-color:rgb(211, 239, 237)"><font size="3"><strong>' + splitline[0][2:6].strip("'") + '<br></strong></font></td>')
                    records_cle[12].append('<td bgcolor="#D2DDBD" align="center" style="background-color:rgb(211, 239, 237)"><font size="3"><strong>' + splitline[1][2:6] + '<br></strong></font></td></tr>' + January_Footer + '\n')
            
                else:
                    records_cle[11].append('<td bgcolor="#D2DDBD" align="center" style="background-color:rgb(211, 239, 237)"><font size="3"><strong>' + splitline[0][2:6].strip("'") + '<br></strong></font></td>')
                    records_cle[12].append('<td bgcolor="#D2DDBD" align="center" style="background-color:rgb(211, 239, 237)"><font size="3"><strong>' + splitline[1][2:6] + '<br></strong></font></td></tr>' + '\n')


    
    ### Step 3: Export file as .txt ###
    print(' Writing data to files... ')

    #Jan output files#
    final_jan_cle = open(output_file_cle_jan,"w+")
    #Feb output files#
    final_feb_cle = open(output_file_cle_feb,"w+")
    #Mar output files#
    final_mar_cle = open(output_file_cle_mar,"w+")
    #Apr output files#
    final_apr_cle = open(output_file_cle_apr,"w+")
    #May output files#
    final_may_cle = open(output_file_cle_may,"w+")
    #Jun output files#
    final_jun_cle = open(output_file_cle_jun,"w+")
    #Jul output files#
    final_jul_cle = open(output_file_cle_jul,"w+")
    #Aug output files#
    final_aug_cle = open(output_file_cle_aug,"w+")
    #Sep output files#
    final_sep_cle = open(output_file_cle_sep,"w+")
    #Oct output files#
    final_oct_cle = open(output_file_cle_oct,"w+")
    #Nov output files#
    final_nov_cle = open(output_file_cle_nov,"w+")
    #Dec output files#
    final_dec_cle = open(output_file_cle_dec,"w+")

    # For loop that goes through all the lines the list normals_xxx and get the text out then writes it to the file
    for j in range(0,366):
        text_cle='\n'.join(listitem_cle[j] for listitem_cle in records_cle)
        #print(text)
        if j<=30:
            if j == 0:
                final_jan_cle.write(text_cle)
            if j > 0:
                final_jan_cle.write(text_cle)
        if (j>=31 and j<=59):
            final_feb_cle.write(text_cle)
        if (j>=60 and j<=90):
            final_mar_cle.write(text_cle)
        if (j>=91 and j<=120):
            final_apr_cle.write(text_cle)
        if (j>=121 and j<=151):
            final_may_cle.write(text_cle)
        if (j>=152 and j<=181):
            final_jun_cle.write(text_cle)
        if (j>=182 and j<=212):
            final_jul_cle.write(text_cle)
        if (j>=213 and j<=243):
            final_aug_cle.write(text_cle)
        if (j>=244 and j<=273):
            final_sep_cle.write(text_cle)
        if (j>=274 and j<=304):
            final_oct_cle.write(text_cle)
        if (j>=305 and j<=334):
            final_nov_cle.write(text_cle)
        if (j>=335 and j<=366):
            final_dec_cle.write(text_cle)

    #Close all the open files#
    final_jan_cle.close()
    final_feb_cle.close()
    final_mar_cle.close()
    final_apr_cle.close()
    final_may_cle.close()
    final_jun_cle.close()
    final_jul_cle.close()
    final_aug_cle.close()
    final_sep_cle.close()
    final_oct_cle.close()
    final_nov_cle.close()
    final_dec_cle.close()

    print(' Now creating pdf files')
    pdfkit.from_file('../../PDFTxtFiles/Records/'+site+'/climate_records_'+site+'_jan.html', '../../PDFTxtFiles/Records/'+site+'/climate_records_'+site+'_jan.pdf')
    pdfkit.from_file('../../PDFTxtFiles/Records/'+site+'/climate_records_'+site+'_feb.html', '../../PDFTxtFiles/Records/'+site+'/climate_records_'+site+'_feb.pdf')
    pdfkit.from_file('../../PDFTxtFiles/Records/'+site+'/climate_records_'+site+'_mar.html', '../../PDFTxtFiles/Records/'+site+'/climate_records_'+site+'_mar.pdf')
    pdfkit.from_file('../../PDFTxtFiles/Records/'+site+'/climate_records_'+site+'_apr.html', '../../PDFTxtFiles/Records/'+site+'/climate_records_'+site+'_apr.pdf')
    pdfkit.from_file('../../PDFTxtFiles/Records/'+site+'/climate_records_'+site+'_may.html', '../../PDFTxtFiles/Records/'+site+'/climate_records_'+site+'_may.pdf')
    pdfkit.from_file('../../PDFTxtFiles/Records/'+site+'/climate_records_'+site+'_jun.html', '../../PDFTxtFiles/Records/'+site+'/climate_records_'+site+'_jun.pdf')
    pdfkit.from_file('../../PDFTxtFiles/Records/'+site+'/climate_records_'+site+'_jul.html', '../../PDFTxtFiles/Records/'+site+'/climate_records_'+site+'_jul.pdf')
    pdfkit.from_file('../../PDFTxtFiles/Records/'+site+'/climate_records_'+site+'_aug.html', '../../PDFTxtFiles/Records/'+site+'/climate_records_'+site+'_aug.pdf')
    pdfkit.from_file('../../PDFTxtFiles/Records/'+site+'/climate_records_'+site+'_sep.html', '../../PDFTxtFiles/Records/'+site+'/climate_records_'+site+'_sep.pdf')
    pdfkit.from_file('../../PDFTxtFiles/Records/'+site+'/climate_records_'+site+'_oct.html', '../../PDFTxtFiles/Records/'+site+'/climate_records_'+site+'_oct.pdf')
    pdfkit.from_file('../../PDFTxtFiles/Records/'+site+'/climate_records_'+site+'_nov.html', '../../PDFTxtFiles/Records/'+site+'/climate_records_'+site+'_nov.pdf')
    pdfkit.from_file('../../PDFTxtFiles/Records/'+site+'/climate_records_'+site+'_dec.html', '../../PDFTxtFiles/Records/'+site+'/climate_records_'+site+'_dec.pdf')

    print(' Script completed and files genereated... ')


for site in sites:
    run_script(site)