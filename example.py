"""
This is an example of using VAWL.
"""

from vawl.wl import WakeWordListnerProcess

def hello():
    print("Hey There !")

def start():
    print("You just said Start")

def stop():
    print("You just said stop")

def left():
    print("You just said Left")

def right():
    print("You just said Right")

try:
    # device = None is the default, sets the microphone to system default. Default model_name is en-in, change it to your model files directory name.
    my_wl = WakeWordListnerProcess(device=None, model_name="en-in")
    # We are using not 1 but 6 wakewords !!!
    my_wl.register_wakeword('hello', hello)
    my_wl.register_wakeword('start', start)
    my_wl.register_wakeword('stop', stop)
    my_wl.register_wakeword("left", left) 
    my_wl.register_wakeword("right", right)
    def bye():
        print('Bye !')
        my_wl.stop() 
    my_wl.register_wakeword('bye', bye)
    my_wl.start()
except KeyboardInterrupt:
    my_wl.stop()