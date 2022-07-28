from mistyPy.Robot import Robot
from mistyPy.Events import Events
import json
from time import time
import google.oauth2.credentials


###############################################FACE RECOGNITION###################################################################


def Start_Face_Recognition():
    print('\nSTART FACE RECOGNITION FUNCTION')
    misty.RegisterEvent("Face", Events.FaceRecognition, callback_function=FaceDetect)
    misty.StartFaceDetection()
    misty.StartFaceRecognition()


def FaceDetect(event):
    hora = time()
    print('\nSTART FACE DETECT FUNCTION')
    misty.StopFaceRecognition()
    misty.StopFaceDetection()
    Name = event['message']['personName']
    if Name == 'unknown person':
        misty.ChangeLED(148, 0, 211)
        misty.DisplayImage("e_Contempt.jpg")
        misty.Speak("Hello human, welcome to La Pipa! What's your name?")
        CaptureSpeech()
        Wait(hora,7)
        ReturnToNormal()
    else:
        misty.ChangeLED(0, 0, 111)
        misty.DisplayImage("e_Joy2.jpg")
        string = 'Hi ' + Name + ' we have met before'
        misty.Speak(string)
        misty.MoveArm("both", -26, 100)
        misty.Stop(1000)
        misty.MoveArm("both", 90, 100)
        Wait(hora,7)
        hora = time()
        ReturnToNormal()
        
                

###############################################AUDIO###################################################################


def CaptureSpeech():
    print('\nSTART CAPTURE SPEECH FUNCTION')
    misty.ChangeLED(0, 0, 255)
    misty.RegisterEvent("StartRecord", Events.VoiceRecord,
                        debounce=10000, callback_function=GetFileName)
    misty.CaptureSpeech(silenceTimeout=1000, maxSpeechLength=5000)


def GetFileName(event):
    print('\nSTART GET FILE NAME FUNCTION')
    file_name = event['message']['filename']
    data = misty.GetAudioFile(file_name, base64=True)
    base64 = data.json()['result']['base64']
    _GetAudioFile(data)

##############################################GOOGLE API#########################################################


def _GetAudioFile(data):
    print('\nSTART GET AUDIO FILE FUNCTION')
    base64 = data.json()['result']['base64']
    respuest = misty.SendExternalRequest(
        "POST",
        "https://speech.googleapis.com/v1p1beta1/speech:recognize?key=" + apikey,
        None,
        None,
        json.dumps({"audio": {'content': base64}, "config": {"enableAutomaticPunctuation": True,
                   "encoding": "LINEAR16", "languageCode": "es-ES", "model": "command_and_search"}})
    )
    _SendExternalRequest(respuest)


def _SendExternalRequest(data):
    print('\nSTART SEND EXTERNAL REQUEST FUNCTION')
    respuesta = data.json()['results'][0]['alternatives'][0]['transcript']
    print('Misty heard: ' + respuesta)
    if not respuesta:
        misty.Speak("I'm sorry I couldn't hear you well.")
    else:
        misty.Speak("Please stand still for a second")
        misty.StartFaceTraining(respuesta)

##############################################SCRIPTS#########################################################

def Wait(hora,seconds):
    vuelve =True
    while vuelve:
        if time()-hora > seconds:
            vuelve=False

def ReturnToNormal():
    misty.DisplayImage('e_DefaultContent.jpg')
    misty.ChangeLED(0, 0, 0)

###############################################TEST-CODE#########################################################


ip_address = '192.168.128.86'
misty = Robot(ip_address)
apikey = 'YOUR APIKEY'

misty.MoveHead(-5, 0, 0)
misty.DisplayImage('e_DefaultContent.jpg')
misty.ChangeLED(0, 0, 0)
