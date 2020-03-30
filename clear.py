import epd7in5

def main():
    epd = epd7in5.EPD()
    epd.init()
    epd.Clear()
    epd.sleep()
 
if __name__ == '__main__':
    main()
