from mistyPy.Robot import Robot
from mistyPy.Events import Events
import json

###############################################AUDIO###################################################################

def AudioFunc():
    misty.RegisterEvent("Introduction", Events.TextToSpeechComplete, keep_alive=False, callback_function=CaptureSpeech)
    misty.Speak("Hi", utteranceId= 'tts-content')
    
    
def CaptureSpeech(event):
    misty.RegisterEvent("StartRecord", Events.VoiceRecord, debounce=10000,callback_function=GetFileName)
    misty.CaptureSpeech(silenceTimeout=1000)
    
def GetFileName(event):
    file_name = event['message']['filename']

# DownloadAudio doesnt currently work
#def DownloadAudio():
    #file_name = event['message']['filename']
    # url = 192.168.128.86/api/audio?FileName=test3_luis.wav
    #file_name = 'test3_luis.wav'
    #misty.GetAudioFile(file_name, 'ProcessAudioFile')
    
###############################################FACE#########################################################
    
def FaceFunc():
    misty.RegisterEvent(event_name='FaceRecog',event_type=Events.FaceRecognition,callback_function=FaceRecog)
    misty.StartFaceDetection()
    misty.StartFaceRecognition()
    
def FaceRecog(event):
    print(event)
    misty.StopFaceRecognition()
    misty.StopFaceDetection
    

###############################################SCRIPTS#########################################################

def GetAudioList():
    x = json.loads(misty.GetAudioList().text)['result']
    l = []
    for i in range(len(x)):
        if x[i]['systemAsset'] == False:
            l.append(x[i]['name'])
    return l

###############################################TEST-CODE#########################################################

ip_address = '192.168.128.86'
misty = Robot(ip_address)
