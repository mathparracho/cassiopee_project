from flask import Flask
import os

app = Flask(__name__)

@app.route('/')
def run_script():
    os.system('python3 main2.py /home/kali/Desktop/TSP/Mozart/testcases2/bumbum.png ./') 
    return 'hello'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8000', debug=True)