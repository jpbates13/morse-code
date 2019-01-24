import RPi.GPIO as GPIO
import time
import sys
import os

from flask import Flask
from flask import render_template, request
app = Flask(__name__)

@app.route("/")
def hello():
    return render_template("index.html")


@app.route('/translate', methods=['POST', 'GET'])
def translate():
    error = None
    if request.method == 'POST':
	if 'text' in request.form:
    		print(request.form['text'])
		GPIO.setmode(GPIO.BCM)
		GPIO.setwarnings(False)
		GPIO.setup(21, GPIO.OUT)
		os.system('clear')
		inputString = request.form['text']
	
		morse = [".-", "-...", "-.-.", "-..", ".", "..-.", "--.", "....", "..", ".---", "-.-", ".-..", "--", "-.", "---", ".--.", "--.-", ".-.", "...", "-", "..-", "...-", ".--", "-..-", "-.--", "--..", " ", ".-.-.-", "--..--", "---...", "..--..", ".----.", "-....-", "-..-. ",".-..-.", "-...-"] 
		alpha = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", " ", ".", ",", ":", "?", "'", "-", "/",  "@", "="] 
		newString = []

		for char in inputString.lower():
			char = str(morse[alpha.index(char)])
			newString.append(char)

	
		print(newString)

		for i in range (len(newString)):
			if(newString[i][0] != " "):
				time.sleep(0.3)
			for j in range(len(newString[i])):
				if(newString[i][j] == "."):
					GPIO.output(21, GPIO.HIGH)
					time.sleep(0.1)
					GPIO.output(21, GPIO.LOW)
					time.sleep(0.1)
				elif(newString[i][j] == "-"):
					GPIO.output(21, GPIO.HIGH)
					time.sleep(0.3)
					GPIO.output(21, GPIO.LOW)
					time.sleep(0.1)
				elif(newString[i][j] == " "):
					time.sleep(0.7)
		cleanString = ""
		for i in range (len(newString)):
			cleanString = cleanString + newString[i]

	else:
    		error = 'Invalid text'
    	# the code below is executed if the request method
    	# was GET or the credentials were invalid
	return render_template('index.html', error=error, cleanString=cleanString)


if __name__ == "__main__":
    app.run(host="0.0.0.0", threaded = True)
