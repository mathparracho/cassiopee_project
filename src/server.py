from flask import Flask, request, send_file
from flask_cors import CORS, cross_origin
import os
import requests
import base64
from PIL import Image
from midi2audio import FluidSynth

import wave
from scipy.io import wavfile
import librosa, numpy as np


app = Flask(__name__)
CORS(app)
cors = CORS (app)

def compress(image_file):

    filepath = os.path.join(os.getcwd(), image_file)

    image = Image.open(filepath)
    
    width, height = image.size
    
    image = image.crop((5,height/2.5,width,1.6*height/2.5))
    #image = image.resize((1000,300))
    

    image.save("req.jpg",
                 "JPEG",
                 optimize = True,
                 quality = 10)
    return

#test base
@app.route('/')
def run_script():
    return 'serverOn'
    
@app.route('/getMid')
def getMid():
    return send_file('./changed.wav')
    
@app.route('/getGmn')
def getGmn():
    return send_file('./req.gmn')
    

#get the upladed image
@app.route('/photo', methods=['POST'])
def register_new():
    photo = request.get_json()['photo']
    tempo = request.get_json()['tempo']
    
    #format base64 input
    for index in range(len(photo)):
    	if photo[index] == ',':
    		indexComma = index
    		break
    photo = photo[indexComma+1::]
    print('received image!')
    
    #decoding the image
    photo_data = base64.b64decode(photo)
    with open("req.jpg", "wb") as file:
        file.write(photo_data)
        
        #compress("./req.jpg")
        
        #print("compressing")
        
    	#run the model
        os.system('python3 main.py ./req.jpg ./') 
        
        """
        #setting the tempo
        with open('gmn2midi.cfg', 'r') as file:
        	data = file.readlines()
        data[6].replace('100', str(tempo))
        with open('gmn2midi.cfg', 'w') as file:
        	file.writelines(data)
    	"""
    		     
        #convert to midi file
        print('converting to gmn...')
        os.system('mv req.txt req.gmn')
        print('converting to MIDI...')
        os.system('wine gmn2midi.exe req.gmn')
        print('converting to MP3...')
        fs = FluidSynth()
        fs.midi_to_audio('req.mid', 'req.wav')
        #os.system('midi2audio req.mid req.wav')
        
        """
        #setting the tempo back to default
        with open('gmn2midi.cfg', 'r') as file:
        	data = file.readlines()
        data[6].replace(str(tempo), '100')
        with open('gmn2midi.cfg', 'w') as file:
        	file.writelines(data)
        """	
        	
        song, fs = librosa.load("req.wav")
        song_2_times_faster = librosa.effects.time_stretch(song, rate = float(tempo)/100)
        wavfile.write("changed.wav", fs, song_2_times_faster)
        
        """
        CHANNELS = 1
        swidth = 2
        Change_RATE = float(tempo)/100
        
        spf = wave.open('req.wav', 'rb')
        RATE=spf.getframerate()
        signal = spf.readframes(-1)
        
        wf = wave.open('changed.wav', 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(swidth)
        wf.setframerate(RATE*Change_RATE)
        wf.writeframes(signal)
        wf.close()
        """
        
        return 'done'
        

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8000', debug=True)
