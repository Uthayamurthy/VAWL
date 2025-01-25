"""
VAWL - Vosk As Wakeword Listener - A simple and powerful Wakeword Listener that requires zero training using Vosk
Copyright (C) 2025  R Uthaya Murthy
"""

import queue
import sys
import sounddevice as sd
import threading
import json
import setproctitle
import multiprocessing
from vosk import Model, KaldiRecognizer, SetLogLevel

class WakeWordListner:
    def __init__(self, device=None, model_name="en-in"):
        self.q = queue.Queue()
        self.result_queue = queue.Queue()

        self.device = device
        device_info = sd.query_devices(device, "input")
        self.samplerate = int(device_info["default_samplerate"])

        SetLogLevel(-1)
        self.model = Model(model_name)
        
        self.al = {} # Action List
        self.wakewords_list = [] # Wake Words in Python List.
        self.wakewords = '[]' # Wake Words in json string format.

        self.stop_listen = False
        self.stop_action = False

    def callback(self, indata, frames, time, status): # Puts the audio data from microphone into a queue
        """This is called (from a separate thread) for each audio block."""
        if status:
            print(status, file=sys.stderr)
        self.q.put(bytes(indata))

    def action_runner(self): # Runs the action of the wakeword, when it is detected. 
        setproctitle.setthreadtitle(threading.current_thread().name)
        while True:
            if self.stop_action:
                    break
            if self.result_queue.qsize != 0:  # Avoid Empty Queue
                word = self.result_queue.get()
                if word == '':
                    continue
                if word in self.wakewords_list:
                    print(f'Action Runner : Running function of {word}')
                    self.al[word]() # Run the action !!

    def register_wakeword(self, word, action):
        self.al[word] = action
        self.wakewords_list.append(word)
        self.wakewords = json.dumps(self.wakewords_list)
        print(f'Registered wakeword {word} !')

    def listener(self):
        setproctitle.setthreadtitle(threading.current_thread().name)
        with sd.RawInputStream(samplerate=self.samplerate, blocksize = 10000, device=self.device,
                    dtype="int16", channels=1, callback=self.callback):

            rec = KaldiRecognizer(self.model, self.samplerate, self.wakewords)
            while True:
                if self.stop_listen:
                    break
                data = self.q.get()
                if rec.AcceptWaveform(data):
                    result = rec.Result()
                    r = json.loads(result)
                    if r != '' or r != '':
                        self.result_queue.put(r['text'])
                # else:
                #     print(rec.PartialResult())

class WakeWordListnerProcess:
    def __init__(self, device=None, model_name="en-in"):
       self.wl = WakeWordListner(device=device, model_name=model_name)
    
    def register_wakeword(self, word, action):
        self.wl.register_wakeword(word, action)

    def start_action_runner(self):
        print('Starting Action Runner Thread ...')
        self.action_thread = threading.Thread(name="VAWL - Action Runner", target=self.wl.action_runner)
        self.action_thread.start()
        print('Action Runner thread is now running ...')

    def start_listening(self):
        print('Starting Listening for wakewords ...')
        self.listener_thread = threading.Thread(name="VAWL - Wakeword Listener", target=self.wl.listener)
        self.listener_thread.start()
        print('Wakeword listner is now running ...')
    
    def stop_listening(self):
        self.wl.stop_listen = True
    
    def stop_action_runner(self):
        self.wl.stop_action = True
    
    def start(self):
        setproctitle.setproctitle(multiprocessing.current_process().name)
        self.start_action_runner()
        self.start_listening()
        self.action_thread.join()
        self.listener_thread.join()

    def stop(self):
        self.stop_action_runner()
        self.stop_listening()