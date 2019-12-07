import os
import json
import datetime
import requests
from collections import Counter
from flask import Flask, Markup, render_template, request, redirect, flash, url_for
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = '/uploads'
ALLOWED_EXTENSIONS = {'json'}

app = Flask(__name__)
app.secret_key = "super secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
  return render_template('index.html')

# with open('MyActivity.json') as json_file:
#     data = json.load(json_file)

@app.route('/bar', methods = ['GET', 'POST'])
def bar():
	if request.method == 'POST':
		file = request.files['file']
		file_content = file.read()
		musicData = json.loads(file_content)
	artists = []
	labels = []
	values = []
	for i in musicData:
		if "Listened" in i["title"] and datetime.datetime.strptime(i["time"][:10], '%Y-%m-%d').year == 2019:
			artists += [i["description"]]
	countDict = Counter(artists)
	countDict = countDict.most_common(20)
	for i in countDict:
		labels += [i[0]]
		values += [i[1]]
	bar_labels = labels
	bar_values = values
	return render_template('bar_chart.html', title='Top Artists - 2019', labels=bar_labels, values=bar_values)

if __name__ == '__main__':
    app.run(host='127.0. 0.1', port=8080)