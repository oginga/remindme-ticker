
from remindme import RemindmeRepository
from time import sleep
import logging
import os
from daemon import runner

def calculate_pixels_time(str_length):
        #FINDINGS
        #with font =('courier',18, 'bold')
        #dx=1
        # and time.sleep-->(0.015) 
        #for any given text,when pixel is set to the below values,the ticker stops at particular indices of the text
        #
        #px=100  index=8
        #px=200  index=15
        #px=300  index=22
        #px=400  index=29
        #
        #thus if n=(px/100) then the number of characters presented by the ticker is:
        #
        #      8n-n-1
        #
        #resuls--one character requires an average of 14px o display
        #
        #

        #     ***TIME**
        #a text of the below length took the seconds below to display on screen
        #len=131  t=30
        #len=103  t=23
        #len=20  t=5
        #len=63  t=14
        #
        #with an error of positive or negative 2
        #
        #reswults --> 4 xters req 1sec 
        #

        pixies=str_length*14
        #saa -->swahili for 'time'
        saa=(str_length/4)*1
        return saa,pixies


class App():
   
    def __init__(self):
        self.stdin_path = '/dev/null'
        self.stdout_path = '/dev/tty'
        self.stderr_path = '/dev/tty'
        self.pidfile_path =  '/var/run/testdaemon/tickerdaemon.pid'
        self.pidfile_timeout = 5
           
    def run(self):
        
        while True:
                try:
                        # Python2
                        import Tkinter as tk
                except ImportError:
                        # Python3
                        import tkinter as tk
                root = tk.Tk()
                #root.after(5000, lambda: root.destroy())
                canvas = tk.Canvas(root, height=30, width=1048, bg="cyan")
                canvas.pack()
                font =('courier',18, 'bold')
        
                text_width = 15

                #remindme
                repo=RemindmeRepository.RemindmeRepository(os.path.join(os.path.expanduser("~"), ".remindme.db"))
                reminders=repo.get_remindmes()

                titles = [r.get_title() for r in reminders]
                contents=[r.get_content() for r in reminders]
                num = len(titles)
                number = 0
                tw = ' ' * text_width
                display_content =tw+"REMINDERS "
                d=dict(zip(titles,contents))

                for k,v in d.items():
                        number += 1
                        display_content = '  #'.join([display_content, '%-2d [[(%s)-->%s]]' % (number, k,v)])

                new_dc=display_content.replace('\n',' ')
                print new_dc

                a_x=100 #tk window axis x
                a_y=1000 #tk window axis y
                # set UpperLeftCorner x, y position of root
                root.geometry("+%d+%d" % (a_x, a_y))

                x = 0
                y = 0
                text = canvas.create_text(x, y, anchor='nw', text=new_dc, font=font)
                dx = 1
                dy = 0 # use horizontal movement only

                # the pixel value depends on dx, font and length of text
                tyme,pixels =calculate_pixels_time(len(new_dc))
                root.after(tyme*1000, lambda: root.destroy())
        
                for p in range(pixels):
                # move text object by increments dx, dy
                # -dx --> right to left
                        try:
                                canvas.move(text, -dx, dy)
                                canvas.update()
                                # shorter delay --> faster movement
                                sleep(0.015)
                        except:
                                pass

                root.mainloop()
                #Note that logger level needs to be set to logging.DEBUG before this shows up in the logs
                logger.debug("Debug message")
                logger.info("Info message")
                logger.warn("Warning message")
                logger.error("Error message")
                time.sleep(60)

app = App()
logger = logging.getLogger("DaemonLog")
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler = logging.FileHandler("/var/log/testdaemon/tickerdaemon.log")
handler.setFormatter(formatter)
logger.addHandler(handler)

daemon_runner = runner.DaemonRunner(app)
#This ensures that the logger file handle does not get closed during daemonization
daemon_runner.daemon_context.files_preserve=[handler.stream]
daemon_runner.do_action()
