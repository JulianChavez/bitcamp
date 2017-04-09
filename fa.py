from flask import Flask
from flask import request
from flask import render_template
from clarifai.client import ClarifaiApi
from clarifai.rest import Image as CImage
from clarifai.rest import ClarifaiApp
import json
import requests

parent = '58e9c2fbceb8abe24250c100'
child = '58e9c32bceb8abe24250c101'
apiKey = 'fdd31f3849d4c8ec03f2aaa1a7f499b3'


app = Flask(__name__)


c_app = ClarifaiApp()

@app.route('/')
def my_form():
    return render_template("pepper_inc.html")

@app.route('/', methods=['POST'])
def fune():
	pic = request.form['picture']
	model = c_app.models.get('food-items-v1.0')
	image = CImage(pic)
	result = model.predict([image])
	print(result['outputs'][0]['data']['concepts'])
	healthy = 1

	# Transfer money if food is healthy
	if healthy:

		url = 'http://api.reimaginebanking.com/accounts/{}/transfers?key={}'.format(parent,apiKey)
		payload = {			
		  "medium": "balance",
		  "payee_id": child,
		  "amount": 0.01,
		  "transaction_date": "2017-04-09",
		  "description": "Money transferred for healthy food"
		}

		response = requests.post( 
			url, 
			data=json.dumps(payload),
			headers={'content-type':'application/json'},
			)

		if response.status_code == 201:
			print('money transferred')


	return "yay"

if __name__ == '__main__':
	app.run()