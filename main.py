import epd7in5
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from datetime import datetime
import requests
import json
import sys
import os

#import imageda
EPD_WIDTH = 640
EPD_HEIGHT = 384
now = datetime.now()
print (now)
current_date = now.strftime("%A %d %B")
current_time = now.strftime("%H:%M:%S")

def suffix(day):
  suffix = ""
  if 4 <= day <= 20 or 24 <= day <= 30:
    suffix = "th"
  else:
    suffix = ["st", "nd", "rd"][day % 10 - 1]
  return suffix
my_date = now.strftime("%A %d" + suffix(now.day) +" %B")

font1 = ImageFont.truetype('/usr/share/fonts/truetype/google/OpenSans-Bold.ttf', 34)
font2 = ImageFont.truetype('/usr/share/fonts/truetype/google/OpenSans-Regular.ttf', 60)
font3 = ImageFont.truetype('/usr/share/fonts/truetype/google/OpenSans-Bold.ttf', 20)
font4 = ImageFont.truetype('/usr/share/fonts/truetype/google/OpenSans-Light.ttf', 12)
font5 = ImageFont.truetype('/usr/share/fonts/truetype/google/OpenSans-Regular.ttf', 48)
url1 = 'http://192.168.1.2:8080/json.htm?type=devices&rid=25' # Pool Temp
url2 = 'http://192.168.1.2:8080/json.htm?type=devices&rid=271' # Outside Temp/humid
#url3 = 'http://192.168.1.2:8080/json.htm?type=devices&rid=118'
url4 = 'http://192.168.1.44/cm?cmnd=status%208' # House Power
url5 = 'http://192.168.1.50/cm?cmnd=status%208' # Solar Power
url6 = 'http://192.168.1.36/cm?cmnd=status%200' # Pool Pump
url7 = 'http://192.168.1.39/cm?cmnd=status%200' # Pool Heater
# http://api.openweathermap.org/data/2.5/forecast?q=sydney,NSW,AU&appid=956e5fb3d6065c802a7aabf0e075d607
data1 = requests.get(url1, timeout=5).json()
data2 = requests.get(url2, timeout=5).json()
#data3 = requests.get(url3, timeout=5).json()
data4 = requests.get(url4, timeout=5).json()
data5 = requests.get(url5, timeout=5).json()
data6 = requests.get(url6, timeout=5).json()
data7 = requests.get(url7, timeout=5).json()

swim = Image.open(os.path.join('/home/pi/km/python/icons/swim-48.bmp'))
temp = Image.open(os.path.join('/home/pi/km/python/icons/temp-48.bmp'))
house = Image.open(os.path.join('/home/pi/km/python/icons/house-48.bmp'))
sun = Image.open(os.path.join('/home/pi/km/python/icons/sun-48.bmp'))
paige = Image.open(os.path.join('/home/pi/km/python/icons/paige.bmp'))
tashouse = (data4['StatusSNS']['ENERGY']['Power'])
tassolar = (data5['StatusSNS']['ENERGY']['Power'])
tassolartoday = round((data5['StatusSNS']['ENERGY']['Today']), 2)
tassolarYesterday = round((data5['StatusSNS']['ENERGY']['Yesterday']), 2)
poolpumpbinary = (data6['Status']['Power'])
poolheatbinary = (data7['Status']['Power'])

if poolheatbinary == 1: 
    poolheatpower = "On"
else:
    poolheatpower = "Off"

if poolpumpbinary == 1: 
    poolpumppower = "On"
else:
    poolpumppower = "Off"

if tassolar <= 5:
	tassolar = 0

if tassolar > tashouse:
    face = Image.open(os.path.join('/home/pi/km/python/icons/happy-48.bmp'))
    thumb = Image.open(os.path.join('/home/pi/km/python/icons/thumb-up-128.bmp')) 
    
if tassolar < tashouse:
    face = Image.open(os.path.join('/home/pi/km/python/icons/sad-48.bmp'))
    thumb = Image.open(os.path.join('/home/pi/km/python/icons/thumb-down-128.bmp'))

if tassolar == tashouse:
    face = Image.open(os.path.join('/home/pi/km/python/icons/medium-48.bmp'))
    thumb = Image.open(os.path.join('/home/pi/km/python/icons/thumb-up-128.bmp'))    
    
solardelta = tassolar - tashouse

if tassolar > tashouse:
    dollar = ((solardelta / 1000) * 12)
    dollar = round(dollar / 100, 2)
    dollar = "Makes $" + str(dollar) + " p/h"

if tassolar < tashouse:
    dollar = abs(((solardelta / 1000) * 28))
    dollar = round(dollar / 100, 2)
    dollar = "Costs $" + str(dollar) + " p/h"	

for scrape  in  data1['result']:
#    print (scrape['Data'])
    pooltemp = (scrape['Data'])
    timestamp = (scrape['LastUpdate'])

for scrape  in  data2['result']:
#    print (scrape['Data'])
    outsidetemp = (scrape['Data'])

#for scrape  in  data3['result']:
#    print (scrape['Data'])
#    gainwatts = (scrape['Data'])
#    print (scrape)

def main():
    epd = epd7in5.EPD()
    epd.init()
#    epd.Clear()

    # For simplicity, the arguments are explicit numerical coordinates
 
    image = Image.new('1', (EPD_WIDTH, EPD_HEIGHT), 255)    # 1: clear the frame
    image.paste(face, (420,150))
    image.paste(swim, (260,17))
    image.paste(temp, (260,75))
    image.paste(house, (12,150))
    image.paste(sun, (225,150))
    image.paste(paige, (15,230))
#    image.paste(thumb, (40,230))
#    image.paste(month, (12,300))
    draw = ImageDraw.Draw(image)
    draw.rectangle((10, 10, 630, 374), outline = 0) # outside
    draw.rectangle((10, 10, 250, 70), outline = 0)
    draw.rectangle((250, 10, 630, 70), outline = 0)
    draw.rectangle((250, 70, 630, 130), outline = 0)
    draw.rectangle((10, 70, 250, 130), outline = 0)
    draw.rectangle((10, 130, 630, 210), outline = 0) # house sun face
    draw.text((300, 140),"%s" % tassolar, font = font5, fill = 0) # House Solar
    draw.text((90, 140), "%s" % tashouse, font = font5, fill = 0) # House Watts
    draw.text((490, 140), "%s" % solardelta, font = font5, fill = 0) # Gain
    draw.text((12, 11), "Stamp: %s" % current_time, font = font4, fill = 0)
    draw.text((12, 25), "Solar Today       : %s" % tassolartoday, font = font3, fill = 0) # solar today
    draw.text((12, 45), "Solar Yesterday: %s" % tassolarYesterday, font = font3, fill = 0) # solar Yesterday
    draw.text((320, 15), "%s" % pooltemp, font = font1, fill = 0)
    draw.text((320, 75), "%s" % outsidetemp, font = font1, fill = 0)
    draw.text((12, 70), "%s" % dollar , font = font3, fill = 0)
    draw.text((260, 220), "%s" % my_date , font = font1, fill = 0)
    draw.text((260, 270), "Pool Pump is %s" % poolpumppower , font = font1, fill = 0)
    draw.text((260, 320), "Pool Heater is %s" % poolheatpower , font = font1, fill = 0)
    epd.display(epd.getbuffer(image))
    epd.sleep()

if __name__ == '__main__':
    main()
