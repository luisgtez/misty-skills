
from mistyPy.Robot import Robot
from mistyPy.Events import Events
import json
import requests

#######################################Misty Record Query###################################################

def CaptureSpeech():
  print('START CaptureSpeech\n')
  misty.RegisterEvent("StartRecord", Events.VoiceRecord,debounce=10000, callback_function=GetFileName)
  misty.ChangeLED(0, 0, 255)
  misty.CaptureSpeech(silenceTimeout=1000, maxSpeechLength=5000)

def GetFileName(event):
  print('START GetFileName\n')
  file_name = event['message']['filename']
  data = misty.GetAudioFile(file_name, base64=True)
  base64_data = data.json()['result']['base64']
  GetAudioFile(base64_data)

#######################################Misty Heard GoogleAPI#############################################################

def GetAudioFile(base64_data):
  print('START _GetAudioFile\n')
  respuest = misty.SendExternalRequest(
      "POST",
      "https://speech.googleapis.com/v1p1beta1/speech:recognize?key=" + GTTS_Key,
      None,
      None,
      json.dumps({"audio": {'content': base64_data}, "config": {"enableAutomaticPunctuation": True,
                  "encoding": "LINEAR16", "languageCode": "es-ES", "model": "command_and_search"}})
  )
  _SendExternalRequest(respuest)

def _SendExternalRequest(data):
  print('START _SendExternalRequest\n')
  respuesta = data.json()['results'][0]['alternatives'][0]['transcript']
  Google_Dialog_Flow_API(respuesta)

#######################################Google Dialog Flow API###################################################

def Google_Dialog_Flow_API(query_tiempo):
  print('START Google_Dialog_Flow_API\n')
  reqUrl = "https://dialogflow.googleapis.com/v2/projects/misty-weather-mocr/agent/sessions/test1:detectIntent"

  headersList = {
  "Accept": "*/*",
  "User-Agent": "Thunder Client (https://www.thunderclient.com)",
  "Authorization": 'Bearer '+GDF_Token,
  "Content-Type": "application/json" 
  }

  payload = json.dumps({
    "queryInput": {
      "text": {
        "text": query_tiempo,
        "languageCode": "es"
      }
    }
  })

  response_gdf = requests.request("POST", reqUrl, data=payload,  headers=headersList)
  Extract_Data_From_GDF(response_gdf)

#######################################Extracting data from GDF API############################################

def Extract_Data_From_GDF(response_gdf):
  print('START Extract_Data_From_GDF\n')

  location = response_gdf.json()['queryResult']['outputContexts'][0]['parameters']['address']['city']
  date = response_gdf.json()['queryResult']['outputContexts'][0]['parameters']['date-time']
  
  weather_API(location, date)
#######################################Weather API#############################################################

def weather_API(location, date):
  print('START weather_API')
  reqUrl = "https://api.weatherapi.com/v1/forecast.json?key=50cd09d6fd3242ad944142452222507&q="+location+"&dt="+date

  headersList = {
  "Accept": "*/*",
  "User-Agent": "Thunder Client (https://www.thunderclient.com)" 
  }

  response_weather = requests.request("POST", reqUrl,  headers=headersList)
  
  print(type(response_weather.json()))
  with open('response_weather.json', 'w') as outfile:
    json.dump(response_weather, outfile)
  
  dia_weather = response_weather.json()['forecast']['forecastday'][0]['date']
  maxtemp_weather = response_weather.json()['forecast']['forecastday'][0]['day']['maxtemp_c']
  mintemp_weather = response_weather.json()['forecast']['forecastday'][0]['day']['mintemp_c']
  avghumidity_weather = response_weather.json()['forecast']['forecastday'][0]['day']['avghumidity']
  daily_chance_of_rain_weather = response_weather.json()['forecast']['forecastday'][0]['day']['daily_chance_of_rain']
  condition_weather = response_weather.json()['forecast']['forecastday'][0]['day']['condition']['text']
  
  datos_weather = {
                  'location':location,
                  'date':date,
                  'dia_weather': dia_weather, 
                  'maxtemp_weather': maxtemp_weather, 
                  'mintemp_weather': mintemp_weather, 
                  'avghumidity_weather': avghumidity_weather,
                  'daily_chance_of_rain_weather': daily_chance_of_rain_weather,
                  'condition_weather': condition_weather
                  }
  
  #Return_Weather(datos_weather)
  
  
#######################################Misty Speak#############################################################

def Return_Weather(datos_weather):
  misty.Speak("La temperatura máxima es de "+str(datos_weather['maxtemp_weather'])+
              " grados centígrados, la temperatura mínima es de "+str(datos_weather['mintemp_weather'])+
              " grados centígrados, la humedad promedio es de "+str(datos_weather['avghumidity_weather'])+
              " por ciento, el día "+str(datos_weather['dia_weather'])+
              " la probabilidad de lluvia es de "+str(datos_weather['daily_chance_of_rain_weather'])+
              " por ciento, y el estado actual es "+str(datos_weather['condition_weather']),voice="es-es-x-ana-local")
  
#######################################TestCode##########################################################


misty = Robot('192.168.128.86')
GDF_Token = "ya29.A0AVA9y1sAoWfwYThJXJs7_YKEiSI8J3RUESQn61b47816TWWORMQJs3jppNwdUqmBMDEg65nfN7a5MHEaPGHJkPjGl5nPXhnIyy-cF8aDFtPxSqhJgb6sex3FbutMGwEzfClCeyw_KLwTzMDf9-yi_7V9qtvAYUNnWUtBVEFTQVRBU0ZRRTY1ZHI4RC1zeEZVSWtjZkdJYWgzWktNanA4QQ0163"
GTTS_Key = 'AIzaSyB3ZjAuEvJYwwKVnRrgvymJqMe5kSBFYzk'
Google_Dialog_Flow_API("Que tiempo hace mañana en Gijon")
#CaptureSpeech()