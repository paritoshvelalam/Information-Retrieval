from flask import Flask,request,render_template,jsonify
import json_to_trec

app = Flask(__name__)

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/process',methods= ['POST'])
def process():
  	query = request.form['search']
  	if query:
   		result = json_to_trec.functionName(query)
   		return jsonify({'output':result})
	return jsonify({'error' : 'Missing data!'})

#if __name__ == '__main__':
#	app.run()
