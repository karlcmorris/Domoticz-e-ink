import epd7in5  
epaper = epd7in5.EPD()
from PIL import Image
epaper.init()
EPD_WIDTH = 640
EPD_HEIGHT = 384
no_of_cycles = 3

white = Image.new('1', (EPD_WIDTH, EPD_HEIGHT), 'white')
black = Image.new('1', (EPD_WIDTH, EPD_HEIGHT), 'black')

print('----------Started calibration of E-Paper display----------')
for _ in range(no_of_cycles):
      print('Calibrating...')
      print('black...')
      epaper.display(epaper.getbuffer(black))
      print('white...')
      epaper.display(epaper.getbuffer(white)),
      print('Cycle {0} of {1} complete'.format(_+1, no_of_cycles))

print('-----------Calibration complete----------')
epaper.sleep()
