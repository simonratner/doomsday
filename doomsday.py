""" Monitor microphone for noise. """

from collections import deque
import math
import struct

import pyaudio

from threading import Thread, Event
import win32api
import win32event
import win32service
import win32serviceutil
import servicemanager

def listen(signal, terminate):
  rate = 44100
  audio = pyaudio.PyAudio()
  samples = deque(maxlen = 10 * rate)

  stream = audio.open(input = True,
                      format = pyaudio.paInt16,
                      channels = 1,
                      rate = rate,
                      frames_per_buffer = 1024)
  while not terminate.is_set():
    try:
      data = struct.unpack("%dh" % rate, stream.read(rate))
    except IOError:
      pass
    else:
      samples.extend(data)
      rms = math.sqrt(sum(n*n for n in samples) / len(samples))
      if rms > 20000:
        samples.clear()
        signal.set()
  stream.close()
  audio.terminate()

class DoomsdayDevice(win32serviceutil.ServiceFramework):
  _svc_name_ = "DoomsdayDevice"
  _svc_display_name_ = "Doomsday Device"

  def __init__(self, args):
    win32serviceutil.ServiceFramework.__init__(self, args)
    self.terminate = Event()
    self.signal = Event()
    self.cmd = " ".join(args[1:])

  def log(self, msg):
    servicemanager.LogInfoMsg(msg)

  def warn(self, msg):
    servicemanager.LogWarningMsg(msg)

  def error(self, msg):
    servicemanager.LogErrorMsg(msg)

  def SvcStop(self):
    self.terminate.set()

  def SvcDoRun(self):
    worker = Thread(target = listen, args = (self.signal, self.terminate))
    worker.start()
    while not self.terminate.is_set():
      if self.signal.wait(1):
        self.signal.clear()
        self.log("Triggered (command=%s)" % self.cmd)
        if self.cmd:
          win32api.WinExec(self.cmd)
    worker.join()

if __name__=='__main__':
  win32api.SetConsoleCtrlHandler(lambda event: True, True)  # keep running when logged off
  win32serviceutil.HandleCommandLine(DoomsdayDevice)
