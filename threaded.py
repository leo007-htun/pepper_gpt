#-*- coding: utf-8 -*-

###########################################################

# Author: Sithu Ye Htun, LJMU
# Created: 29.8.23
# License: MIT
#
###########################################################
import socket

from raw_to_wav import rawToWav

NAO_IP = "10.24.63.72" # default, for running on Pepper
NAO_PORT = 9559

from optparse import OptionParser
import naoqi
import numpy as np
import time
import sys
import threading
from naoqi import ALProxy
from google import Recognizer, UnknownValueError, RequestError
from numpy import sqrt, mean, square
import traceback
import threading
import os 


RECORDING_DURATION = 15     # seconds, maximum recording time, also default value for startRecording(), Google Speech API only accepts up to about 10-15 seconds
LOOKAHEAD_DURATION = 1.0    # seconds, for auto-detect mode: amount of seconds before the threshold trigger that will be included in the request
IDLE_RELEASE_TIME = 1.5     # seconds, for auto-detect mode: idle time (RMS below threshold) after which we stop recording and recognize
HOLD_TIME = 1.5             # seconds, minimum recording time after we started recording (autodetection)
SAMPLE_RATE = 48000         # Hz, be careful changing this, both google and Naoqi have requirements!

CALIBRATION_DURATION = 4    # 3 seconds, timespan during which calibration is performed (summing up RMS values and calculating mean)
CALIBRATION_THRESHOLD_FACTOR = 1.5  # 2.15 factor the calculated mean RMS gets multiplied by to determine the auto detection threshold (after calibration)

DEFAULT_LANGUAGE = "en-GB"  # RFC5646 language tag, e.g. "en-us", "de-de", "fr-fr",... <http://stackoverflow.com/a/14302134>

WRITE_WAV_FILE = True     # write the recorded audio to "out.wav" before sending it to google. intended for debugging purposes
PRINT_RMS = True           # prints the calculated RMS value to the console, useful for setting the threshold

PREBUFFER_WHEN_STOP = False # Fills pre-buffer with last samples when stopping recording. WARNING: has performance issues!


class SpeechRecognitionModule(naoqi.ALModule):
    """
    Use this object to get call back from the ALMemory of the naoqi world.
    Your callback needs to be a method with two parameter (variable name, value).
    """

    def __init__( self, strModuleName, strNaoIp ):
        try:
            naoqi.ALModule.__init__(self, strModuleName )

            # is these 2 line necessary? what do they do?
            # just copied them from the examples...
            self.BIND_PYTHON( self.getName(),"callback" )
            self.strNaoIp = strNaoIp

            # declare event to ALMemory so other modules can subscribe
            self.memory = naoqi.ALProxy("ALMemory")
            self.memory.declareEvent("SpeechRecognition")
            self.behavior = naoqi.ALProxy("ALBehaviorManager")
	    self.music = naoqi.ALProxy("ALAudioPlayer")
	    self.audio = naoqi.ALProxy("ALAudioDevice")
	    self.tts = naoqi.ALProxy("ALTextToSpeech")
	    self.capture = naoqi.ALProxy("ALPhotoCapture")
            self.img_show = naoqi.ALProxy("ALTabletService")
	    self.img_show.showImageNoCache("http://198.18.0.1/apps/pepper_behaviors-f1daf1/suit.png") 


            # flag to indicate if subscribed to audio events
            self.isStarted = False

            # flag to indicate if we are currently recording audio
            self.isRecording = False
            self.startRecordingTimestamp = 0
            self.recordingDuration = RECORDING_DURATION

            # flag to indicate if auto speech detection is enabled
            self.isAutoDetectionEnabled = True
            self.autoDetectionThreshold = 0.5 #0.0001 adjust ambient noise lvl here, rmsMicFront receives value greater than self.autoDetectionThreshold it will start recording

            # flag to indicate if we are calibrating
            self.isCalibrating = True
            self.startCalibrationTimestamp = 0

            # RMS calculation variables
            self.framesCount = 0
            self.rmsSum = 0 # used to sum up rms results and calculate average
            self.lastTimeRMSPeak = 0

            # audio buffer
            self.buffer = []
            self.preBuffer = []
            self.preBufferLength = 0    # length in samples (len(self.preBuffer) just counts entries)

            # init parameters
            self.language = DEFAULT_LANGUAGE
            self.idleReleaseTime = IDLE_RELEASE_TIME
            self.holdTime = HOLD_TIME
            self.lookaheadBufferSize = LOOKAHEAD_DURATION * SAMPLE_RATE

            # counter for wav file output
            self.fileCounter = 0

        except BaseException, err:
            print( "ERR: SpeechRecognitionModule: loading error: %s" % str(err) )

    # __init__ - end
    def __del__( self ):
        print( "INF: SpeechRecognitionModule.__del__: cleaning everything" )
        self.stop()

    def start( self ):

        if(self.isStarted):
            print("INF: SpeechRecognitionModule.start: already running")
            return

        print("INF: SpeechRecognitionModule: starting!")

        self.isStarted = True

        audio = naoqi.ALProxy( "ALAudioDevice")
        nNbrChannelFlag = 0 # ALL_Channels: 0,  AL::LEFTCHANNEL: 1, AL::RIGHTCHANNEL: 2 AL::FRONTCHANNEL: 3  or AL::REARCHANNEL: 4.
        nDeinterleave = 0
        audio.setClientPreferences( self.getName(),  SAMPLE_RATE, nNbrChannelFlag, nDeinterleave ) # setting same as default generate a bug !?!
        audio.subscribe( self.getName() )
	#a = self.getName()
	#print('getName : ', a )

	        # Play the blip sound
        au = session.service("ALAudioPlayer")
        au.playFile("/home/nao/blip.mp3", 1, 0)

	

    def pause(self):
        print("INF: SpeechRecognitionModule.pause: stopping")
        if (self.isStarted == False):
            print("INF: SpeechRecognitionModule.stop: not running")
            return

        self.isStarted = False


        audio = naoqi.ALProxy("ALAudioDevice", self.strNaoIp, NAO_PORT)
        audio.unsubscribe(self.getName())

        print("INF: SpeechRecognitionModule: stopped!")

    def stop( self ):
        self.pause()

    def processRemote( self, nbOfChannels, nbrOfSamplesByChannel, aTimeStamp, buffer ):
       #print("INF: SpeechRecognitionModule: Processing '%s' channels" % nbOfChannels)

        # calculate a decimal seconds timestamp
        timestamp = float (str(aTimeStamp[0]) + "."  + str(aTimeStamp[1]))

        # put whole function in a try/except to be able to see the stracktrace
        try:

            aSoundDataInterlaced = np.fromstring( str(buffer), dtype=np.int16 )
            aSoundData = np.reshape( aSoundDataInterlaced, (nbOfChannels, nbrOfSamplesByChannel), 'F' )

            # compute RMS, handle autodetection and calibration
            if( self.isCalibrating or self.isAutoDetectionEnabled or self.isRecording):

                # compute the rms level on front mic
                rmsMicFront = self.calcRMSLevel(self.convertStr2SignedInt(aSoundData[0])) #UNCOMMENT

                if (rmsMicFront >= self.autoDetectionThreshold): #UNCOMMENT 
                    # save timestamp when we last had and RMS > threshold
                    self.lastTimeRMSPeak = timestamp

                    # start recording if we are not doing so already
                    if (self.isAutoDetectionEnabled and not self.isRecording and not self.isCalibrating):
                        self.startRecording()

                # perform calibration
                if( self.isCalibrating):

                    if(self.startCalibrationTimestamp <= 0):
                        # we are starting to calibrate, save timestamp
                        # to track how long we are doing this
                        self.startCalibrationTimestamp = timestamp

                    elif(timestamp - self.startCalibrationTimestamp >= CALIBRATION_DURATION):
                        # time's up, we're done!
                        self.stopCalibration()

                    # sum rms values of the frames
                    # keep track of how many frames we sum up
                    # to calculate mean afterwards
                    self.rmsSum += rmsMicFront
                    self.framesCount = self.framesCount + 1


                if(PRINT_RMS):
                    # for debug purposes
                    # also use it to find a good threshold value for auto detection
                    print 'Mic RMS: ' + str(rmsMicFront)

            if( False ):
                # compute average
                aAvgValue = np.mean( aSoundData, axis = 1 )
                print( "avg: %s" % aAvgValue )
            if( False ):
                # compute fft
                nBlockSize = nbrOfSamplesByChannel
                signal = aSoundData[0] * np.hanning( nBlockSize )
                aFft = ( np.fft.rfft(signal) / nBlockSize )
                print aFft
            if( False ):
                # compute peak
                aPeakValue = np.max( aSoundData )
                if( aPeakValue > 8000 ):#16000
                    print( "Peak: %s" % aPeakValue )

            if(not self.isCalibrating):
                if(self.isRecording):
                    # write to buffer
                    self.buffer.append(aSoundData)

                    if (self.startRecordingTimestamp <= 0):
                        # initialize timestamp when we start recording
                        self.startRecordingTimestamp = timestamp
                    elif ((timestamp - self.startRecordingTimestamp) > self.recordingDuration):
                        print('stop after max recording duration')
                        # check how long we are recording
                        self.stopRecordingAndRecognize()

                    # stop recording after idle time (and recording at least hold time)
                    # lastTimeRMSPeak is 0 if no peak occured
                    if (timestamp - self.lastTimeRMSPeak >= self.idleReleaseTime) and (
                            timestamp - self.startRecordingTimestamp >= self.holdTime):
                        print ('stopping after idle/hold time')
                        self.stopRecordingAndRecognize()
                else:
                    # constantly record into prebuffer for lookahead
                    self.preBuffer.append(aSoundData)
                    self.preBufferLength += len(aSoundData[0])

                    # remove first (oldest) item if the buffer gets bigger than required
                    # removes one block of samples as we store a list of lists...
                    overshoot = (self.preBufferLength - self.lookaheadBufferSize)

                    if((overshoot > 0) and (len(self.preBuffer) > 0)):
                        self.preBufferLength -= len(self.preBuffer.pop(0)[0])

        except:
            # i did this so i could see the stracktrace as the thread otherwise just silently failed
            traceback.print_exc()

    # processRemote - end

    def calcRMSLevel(self, data):
        rms = (sqrt(mean(square(data))))
        # TODO: maybe a log would be better for threshold?
        #rms = 20 * np.log10(np.sqrt(np.sum(np.power(data, 2) / len(data))))
        return rms

    def version( self ):
        return "1.1"


    # use this method to manually start recording (works with both autodetection enabled or disabled)
    # the recording will stop after the signal is below the threshold for IDLE_RELEASE_TIME seconds,
    # but will at least record for HOLD_TIME seconds
    def startRecording(self):
        if(self.isRecording):
            print("INF: SpeechRecognitionModule.startRecording: already recording")
            return

        print("INF: Starting to record audio")

        # start recording
        self.startRecordingTimestamp = 0
        self.lastTimeRMSPeak = 0
        self.buffer = self.preBuffer

        #self.preBuffer = []

        self.isRecording = True

        return

    def stopRecordingAndRecognize(self):
        if(self.isRecording == False):
            print("INF: SpeechRecognitionModule.stopRecordingAndRecognize: not recording")
            return

        print("INF: stopping recording and recognizing")

        # TODO: choose which mic channel to use
        # can we use the sound direction module for this?

        # buffer is a list of nparrays we now concat into one array
        # and the slice out the first mic channel
        slice = np.concatenate(self.buffer, axis=1)[0]

        # initialize preBuffer with last samples to fix cut off words
        # loop through buffer and count samples until prebuffer is full
        # TODO: performance issues!
        if (PREBUFFER_WHEN_STOP):
            sampleCounter = 0
            itemCounter = 0

            for i in reversed(self.preBuffer):
                sampleCounter += len(i[0])

                if(sampleCounter > self.lookaheadBufferSize):
                    break

                itemCounter += 1

            start = len(self.buffer) - itemCounter
            self.preBuffer = self.buffer[start:]
        else:
            # don't copy to prebuffer
            self.preBuffer = []

        # start new worker thread to do the http call and some processing
        # copy slice to be thread safe!
        # TODO: make a job queue so we don't start a new thread for each recognition
        threading.Thread(target=self.recognize, args=(slice.copy(), )).start()

        # reset flag
        self.isRecording = False

        return

    def calibrate(self):
        self.isCalibrating = True
        self.framesCount = 0
        self.startCalibrationTimestamp = 0

        print("INF: starting calibration")

        if(self.isStarted == False):
            self.start()

        return

    def stopCalibration(self):
        if(self.isCalibrating == False):
            print("INF: SpeechRecognitionModule.stopCalibration: not calibrating")
            return

        self.isCalibrating = False

        # calculate avg rms over self.framesCount
        self.threshold = CALIBRATION_THRESHOLD_FACTOR * (self.rmsSum / self.framesCount)
        print 'calibration done, RMS threshold is: ' + str(self.threshold)
        return

    def enableAutoDetection(self):
        self.isAutoDetectionEnabled = True
        print("INF: autoDetection enabled")
        return

    def disableAutoDetection(self):
        self.isAutoDetectionEnabled = False
        return

    def setLanguage(self, language = DEFAULT_LANGUAGE):
        self.language = language
        return

    # used for RMS calculation
    def convertStr2SignedInt(self, data):
        """
        This function takes a string containing 16 bits little endian sound
        samples as input and returns a vector containing the 16 bits sound
        samples values converted between -1 and 1.
        """

        # from the naoqi sample, but rewritten to use numpy methods instead of for loops

        lsb = data[0::2]
        msb = data[1::2]

        # don't remove the .0, otherwise overflow!
        rms_data = np.add(lsb, np.multiply(msb, 256.0))

        # gives and array that contains -65536 on every position where signedData is > 32768
        sign_correction = np.select([rms_data>=32768], [-65536])

        # add the two to get the correct signed values
        rms_data = np.add(rms_data, sign_correction)

        # normalize values to -1.0 ... +1.0
        rms_data = np.divide(rms_data, 32768.0)

        return rms_data

    def recognize(self, data):
        # print 'sending %d bytes' % len(data)

        if (WRITE_WAV_FILE):
            # write to file
            filename = "out" + str(self.fileCounter)
            #self.fileCounter += 1
            outfile = open(filename + ".raw", "wb")
            data.tofile(outfile)
            outfile.close()
            rawToWav(filename)

        buffer = np.getbuffer(data)

        r = Recognizer()
        #r.dynamic_energy_threshold = True  
        #r.pause_threshold = 2
	#r.energy_threshold = 4000 #higher to reduce ambient(non-speaking energy), so that while not speaking, it wont try to recognize
        try:
            result = r.recognize_google(audio_data=buffer, samplerate=SAMPLE_RATE, language=self.language)
            self.memory.raiseEvent("SpeechRecognition", result)
            print 'RESULT: ' + result

            if 'dance' in result.lower():
                print('Dancing ...')
		time.sleep(6)
                self.behavior.startBehavior('pepper_behaviors-f1daf1/jazz')
           

	    elif 'music' in result.lower() or 'song' in result.lower():
	        print('playing music ...')
		time.sleep(6)
		self.music.playFile("/home/nao/pepper_gpt/jingle.wav")

	    elif 'play' in result.lower() and 'game' in result.lower():
		self.tts.say("Let's play tic tac toe")
		self.img_show.showWebview("https://playtictactoe.org")

	    elif 'yes' in result.lower():
	        self.img_show.showImageNoCache("http://198.18.0.1/apps/pepper_behaviors-f1daf1/suit.png") 


	    elif 'take' in result.lower() and 'picture' in result.lower():

		self.img_show.hideImage()
		
	        self.tts.say("Please stand infront of me")
		print('taking picture ...')
		time.sleep(5)	
		self.capture.setResolution(2)
		self.capture.setPictureFormat("jpg")
		self.tts.say("Taking picture now, say cheese")
		self.capture.takePictures(1, "/home/nao/.local/share/PackageManager/apps/pepper_behaviors-f1daf1/html", "image", True)
		time.sleep(3)

		self.behavior.startBehavior('pepper_behaviors-f1daf1/capture')
		time.sleep(5)



		#self.capture.takePictures(1, "/home/nao/.local/share/PackageManager/apps/pepper_behaviors-f1daf1/html", "image", True)
		#self.behavior.startBehavior('pepper_behaviors-f1daf1/capture')
	        self.img_show.showImageNoCache("http://198.18.0.1/apps/pepper_behaviors-f1daf1/image.jpg")
		#time.sleep(10)
		self.audio.unsubscribe(self.getName())
		self.tts.say("Do you like your photo?, say 'yes' if you enjoy my photography skills")
		self.audio.subscribe(self.getName())
		
	   
		
		
	    return result
	
	except UnknownValueError:
            print 'ERR: Recognition error'
	    result = ''
	    print(result)
        except RequestError, e:
            print 'ERR: ' + str(e)
        except socket.timeout:
            print 'ERR: Socket timeout'
        except:
            print 'ERR: Unknown, probably timeout ' + str(sys.exc_info()[0])
	

    def setAutoDetectionThreshold(self, threshold):
        self.autoDetectionThreshold = threshold

    def setIdleReleaseTime(self, releaseTime):
        self.idleReleaseTime = releaseTime

    def setHoldTime(self, holdTime):
        self.holdTime = holdTime

    def setMaxRecordingDuration(self, duration):
        self.recordingDuration = duration

    def setLookaheadDuration(self, duration):
        self.lookaheadBufferSize = duration * SAMPLE_RATE
        self.preBuffer = []
        self.preBufferLength = 0

# SpeechRecognition - end


    def getAudioDuration(self):
        return len(self.audio_data)/48000.0

class RobotNavigation:
    def __init__(self, robotIP, PORT):
        self.navigationProxy = naoqi.ALProxy("ALNavigation", robotIP, PORT)
        self.faceProxy = naoqi.ALProxy("ALFaceDetection", robotIP, PORT)
	self.follow = naoqi.ALProxy("ALMotion",robotIP, PORT)
        self.tracker_service = ALProxy("ALTracker", robotIP, PORT)	

    def navigate(self):

        # Add target to track.
        targetName = "Face"
        faceWidth = 0.1
        self.tracker_service.registerTarget(targetName, faceWidth)

        self.faceProxy.subscribe("Test_Face", 300, 0.0)
        self.tracker_service.track(targetName)

        target = self.tracker_service.isTargetLost()

        if target == False:
            #print(target, 'Target in sight ...')
            time.sleep(1)
            self.tracker_service.stopTracker()
           #print('\nmoving Xaxis')
            theta = 0.1 #math.pi/24
            self.follow.moveTo(5.0, 0.0, theta) # Returns:True if the moveTo terminated successfully, False if it was interrupted.

        elif target == True:
            #print(target, 'Target lost ... Navigating ...')
            self.navigationProxy.navigateTo(0.5, 0.2, [["SpeedFactor", 0.6]])
            

def main():
    """ Main entry point

    """
    parser = OptionParser()
    parser.add_option("--pip",
        help="Parent broker port. The IP address or your robot",
        dest="pip")
    parser.add_option("--pport",
        help="Parent broker port. The port NAOqi is listening to",
        dest="pport",
        type="int")
    parser.set_defaults(
        pip=NAO_IP,
        pport=NAO_PORT)

    (opts, args_) = parser.parse_args()
    pip   = opts.pip
    pport = opts.pport

    # We need this broker to be able to construct
    # NAOqi modules and subscribe to other modules
    # The broker must stay alive until the program exists
    myBroker = naoqi.ALBroker("myBroker",
       "0.0.0.0",   # listen to anyone
       0,           # find a free port and use it
       pip,         # parent broker IP
       pport)       # parent broker port

    try:
        p = ALProxy("SpeechRecognition")
        p.exit()  # kill previous instance, useful for developing ;)
    except:
        pass

    # Reinstantiate module

    # Warning: SpeechRecognition must be a global variable
    # The name given to the constructor must be the name of the
    # variable
    global SpeechRecognition
    SpeechRecognition = SpeechRecognitionModule("SpeechRecognition", pip)
    Robotnav = RobotNavigation(NAO_IP,NAO_PORT)

    def Robotnav_loop():                                                                                                  
        while True:                                                                    
            try:                                                        
                Robotnav.navigate()                                  
            except KeyboardInterrupt:                                                               
                break 

    # uncomment for debug purposes
    # usually a subscribing client will call start() from ALProxy
    #SpeechRecognition.start()
    #SpeechRecognition.startRecording()
    #SpeechRecognition.calibrate()
    #SpeechRecognition.enableAutoDetection()
    #SpeechRecognition.startRecording()

    # creating threads
    # creating threads
    t = threading.Thread(target=Robotnav_loop)

    # start threads
    t.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print
        print "Interrupted by user, shutting down"
        Robotnav.stop()  # Stop the Robotnav thread
        myBroker.shutdown()
        sys.exit(0)

if __name__ == "__main__":
    main()
