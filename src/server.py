from flask import Flask, request, send_file
from flask_cors import CORS, cross_origin
import os
import requests
import base64
from PIL import Image

app = Flask(__name__)
CORS(app)
cors = CORS (app)

#test base
@app.route('/')
def run_script():
    return 'serverOn'
    
@app.route('/getTxt')
def getTxt():
    return send_file('./req.txt')
    

#get the upladed image
@app.route('/photo', methods=['POST'])
def register_new():
    photo = request.get_json()['photo']
    
    #format base64 input
    for index in range(len(photo)):
    	if photo[index] == ',':
    		indexComma = index
    		break
    		
    photo = photo[indexComma+1::]

    print(photo)
    photo_data = base64.b64decode(photo)
   
    with open("req.jpg", "wb") as file:
        file.write(photo_data)
        
    	#run the model
        os.system('python3 main.py ./req.jpg ./') 
        
        return send_file('./req.txt')
        

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8000', debug=True)
