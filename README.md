tuneup
======

Helps you tune your instrument to the tuning used in a music file. More information can be found [here](http://j6m8.wordpress.com/2014/03/09/its-not-always-440/).

## Use Case
- You play an instrument and wish to play along with a pre-recorded sample.
- The recorded sample does not tune to 440Hz.
- You don't want to be out of tune the whole time.

## Usage
Run `tuning_up.py`. You have a few options:

Run with all defaults.

    python tuning_up.py your_wav_file_here.wav

Run with tuning pitch:

    python tuning_up.py your_wav_file_here.wav 440
    
Run with all settings:

    #                     filename   bitrate   crop (lo Hz)   crop (hi Hz)   tuning
    python tuning_up.py   sample.wav 44100     0              30000          440
    
Or, concisely:

    python tuning_up.py sample.wav 44100 0 30000 440
    
Defaults:
    
    _FILE = 'music.wav'     # File to read (tuning file will be this plus '-tune'
    _RATE = 44100
    _CROP = [21, 30000]     # Useful for eliminating peaks at 60Hz due to bad insulation.
    _FREQ_TUNE = 440
    
## To-Do:
- Allow 'muting' certain frequencies (like ignoring 60Hz noise)
- Noise minimization
- Rewrite borrowed `synthComplex()` to be more efficient
- User-selection of FFT peak to use
    
