import wave
import os

def rawToWav(filename):

    rawfile = filename + ".raw"
    if not os.path.isfile(rawfile):
        return

    outfile = wave.open(filename + ".wav", "wb")
    outfile.setframerate(48000)
    outfile.setnchannels(1)
    outfile.setsampwidth(2)

    f = open(rawfile, "rb")
    sample = f.read(4096)
    print 'writing file: ' + filename + '.wav'

    while sample != "":
        outfile.writeframes(sample)
        sample = f.read(4096)

    outfile.close()

    os.remove(rawfile)