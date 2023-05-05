from flask import Flask, request
import os
import requests
import base64

app = Flask(__name__)

#test base
@app.route('/')
def run_script():
    return 'serverOn'
    

#get the upladed image
@app.route('/photo', methods=['POST'])
def register_new():
    photo = request.get_json()['photo']
    
    photo_data = base64.b64decode(photo)
    
    with open("req.png", "wb") as file:
        file.write(photo_data)
        
    #run the model
    os.system('python3 main.py ./req.png ./') 
        
    return 'done'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8000', debug=True)