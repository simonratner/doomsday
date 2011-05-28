""" Record a few seconds of audio and save to a WAVE file. """

from collections import deque
import math
import signal
import struct
import pyaudio

abort = False

def handler(signum, frame):
  global abort
  abort = True
  print "* interrupted"
  signal.signal(signal.SIGINT, signal.SIG_DFL)

signal.signal(signal.SIGINT, handler)

rate = 44100
audio = pyaudio.PyAudio()
samples = deque(maxlen = 10 * rate)

stream = audio.open(input = True,
                    format = pyaudio.paInt16,
                    channels = 1,
                    rate = rate,
                    frames_per_buffer = 1024)
print "* listening"
while not abort:
  try:
    data = struct.unpack("%dh" % rate, stream.read(rate))
  except IOError:
    print "* warning: dropped frames"
  else:
    samples.extend(data)
    rms = math.sqrt(sum(n*n for n in samples) / len(samples))
    if rms > 20000:
      samples.clear()
      print "BOOM!"

stream.close()
audio.terminate()
