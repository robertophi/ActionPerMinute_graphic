from pynput.keyboard import Key, Listener
import pynput.mouse

import numpy as np
import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation

#Time window = from how many seconds is the average action per minute calculated
TIME_WINDOW = 30
#X axis is the amount of time shown in the graph, Y axis is the minimum Y size of the graph
X_AXIS_SIZE = 60
Y_AXIS_SIZE = 50

#Scale controls the frames/second flow of the grap
SCALE = 5
data = [0]*SCALE*X_AXIS_SIZE

class controlFunctions:
    def __init__(self):
        self.monitor = Listener(on_release=self.on_release)
        self.controler = pynput.mouse.Listener(on_click=self.on_click)
        self.keyLog = [0]*60
    def on_click(self,x,y,button,pressed):
        if not(pressed):
            self.keyLog.append(time.time())
        ctime=time.time()
        for i in range(0,len(self.keyLog)):
            if (ctime-self.keyLog(i))<TIME_WINDOW:
                self.keyLog=self.keyLog[i:]
                break
    def on_release(self,key):
        self.keyLog.append(time.time())
        ctime=time.time()
        for i in range(0,len(self.keyLog)):
            if (ctime-self.keyLog(i))<TIME_WINDOW:
                self.keyLog=self.keyLog[i:]
                break
def animate(i,keyLog,line):
    global data,ax
    total = 0
    ctime = time.time()
    for item in keyLog:
        if (ctime-item)<TIME_WINDOW:
            total+=1
    total = total*(60/TIME_WINDOW)
    data.append(total)
    data = data[1:]
    plt.ylim(0,max(Y_AXIS_SIZE,max(data)))
    line.set_ydata(data)
    return line,

def main():
        Fctrl = controlFunctions()
        Fctrl.monitor.start()
        Fctrl.controler.start()
        fig, ax = plt.subplots()
        x = np.arange(0, X_AXIS_SIZE, 1/SCALE)
        line, = ax.plot(x, [0]*len(x))

        plt.xlim(0,X_AXIS_SIZE)
        plt.ylim(0,Y_AXIS_SIZE)
        plt.title("Actions/minuto")
        plt.ylabel("APM")
        plt.xlabel("Time")
        animation_func = animation.FuncAnimation(fig,animate,
                                                 frames=None,
                                                 fargs=(Fctrl.keyLog,line),
                                                 interval=1000/SCALE,
                                                 blit = False)
        plt.show()

if __name__ == "__main__":
    main()


