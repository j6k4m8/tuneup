'''
Ugly Hack by @j6m8

Formula for Halfstep-to-Hz:
    http://www.phy.mtu.edu/~suits/NoteFreqCalcs.html
PeakDetect.py by @sixtenbe (https://github.com/sixtenbe)
    https://gist.github.com/sixtenbe/1178136
synthComplex by @Nemeth, StackOverflow.com
    http://stackoverflow.com/questions/5173795/
    how-can-i-generate-a-note-or-chord-in-python
FFT and WAV-Import help from Roland:
    http://rsmith.home.xs4all.nl/miscellaneous/
    filtering-a-sound-recording.html
'''

import wave, math, struct, sys
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
import peakdetect

_FILE = 'music.wav'
_RATE = 44100
_CROP = [21, 30000]
_FREQ_TUNE = 440

def synthComplex(freq=[440],coef=[1], datasize=10000, fname="test.wav"):
    frate = _RATE 
    amp=8000.0 
    sine_list=[]
    for x in range(datasize):
        samp = 0
        for k in range(len(freq)):
            samp = samp + coef[k] * math.sin(2*math.pi*freq[k]*(x/frate))
        sine_list.append(samp)
    wav_file=wave.open(fname,"w")
    nchannels = 1
    sampwidth = 2
    framerate = int(frate)
    nframes=datasize
    comptype= "NONE"
    compname= "not compressed"
    wav_file.setparams((nchannels, sampwidth, framerate, nframes, comptype, compname))
    for s in sine_list:
        wav_file.writeframes(struct.pack('h', int(s*amp/2)))
    wav_file.close()

def get_hz_from_halfsteps_off_a4(halfsteps):
    return 440*(2.**(1./12.))**halfsteps

def get_tuned_a4_from_hz(hz):
    halfsteps = 100
    new_hz = hz
    while (percentage_off(new_hz, _FREQ_TUNE)[0] > 0.05):
        new_hz = hz*(2.**(1./12.))**halfsteps
        halfsteps-=1
    return new_hz

def percentage_off(a, b):
    return [abs((a - b)/b), a]

def find_diff_to_closest_freq_and_make_file(newfname, empirical):
    print _FREQ_TUNE
    tone = get_tuned_a4_from_hz(empirical)
    synthComplex(freq=[tone], datasize=1000000, fname=newfname)
    return tone


def run(__FILE=_FILE, __RATE=_RATE, __CROP=_CROP, __FREQ_TUNE=_FREQ_TUNE):
    global _FILE
    global _RATE
    global _CROP
    global _FREQ_TUNE

    _FILE=__FILE
    _RATE=__RATE
    _CROP=__CROP
    _FREQ_TUNE=__FREQ_TUNE
    
    print "-- Opening wav file."
    wav = wave.open(_FILE, 'r')
    print "-- File opened, compartmentalizing channels."
    full = np.fromstring(wav.readframes(_RATE), dtype=np.int16)
    left = full[0::2]
    right = full[1::2]

    print "-- Taking the FFT."
    l, r = np.fft.rfft(left), np.fft.rfft(right)
    l[:_CROP[0]] = 0
    r[:_CROP[0]] = 0
    print "-- Outputting tuning file. (This takes a while.)"
    print "-- Closest Freq to " + str(_FREQ_TUNE) + "Hz found at " +\
        str(find_diff_to_closest_freq_and_make_file(
        _FILE + "-tune.wav",
        peakdetect.peakdetect(l, delta=10000)[0][0][0]))

    wav.close()
    print "-- Done."


if len(sys.argv) == 2:
    run(__FILE=sys.argv[1])
elif len(sys.argv) == 3:
    run(__FILE=sys.argv[1], __FREQ_TUNE=int(sys.argv[2]))
elif len(sys.argv) == 6:
    run(__FILE=sys.argv[1],
        __RATE=int(sys.argv[2]),
        __CROP=[int(sys.argv[3]), int(sys.argv[4])],
        __FREQ_TUNE=int(sys.argv[5]))
