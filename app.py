import os
import json
import datetime
import requests
from bs4 import BeautifulSoup
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

# @app.route('/bar', methods = ['GET', 'POST'])
# def bar():
# 	if request.method == 'POST':
# 		file = request.files['file']
# 		file_content = file.read()
# 		musicData = json.loads(file_content)
# 	artists = []
# 	labels = []
# 	values = []
# 	for i in musicData:
# 		if "Listened" in i["title"] and datetime.datetime.strptime(i["time"][:10], '%Y-%m-%d').year == 2019:
# 			artists += [i["description"]]
# 	countDict = Counter(artists)
# 	countDict = countDict.most_common(20)
# 	for i in countDict:
# 		labels += [i[0]]
# 		values += [i[1]]
# 	bar_labels = labels
# 	bar_values = values
# 	return render_template('bar_chart.html', title='Total Artist Plays - 2019', labels=bar_labels, values=bar_values)

@app.route('/img', methods = ['GET', 'POST'])
def img():
	if request.method == 'POST':
		file = request.files['file']
		file_content = file.read()
		musicData = json.loads(file_content)
	artists = []
	searches =[]
	labels = []
	for i in musicData:
		if "Listened" in i["title"] and datetime.datetime.strptime(i["time"][:10], '%Y-%m-%d').year == 2019:
			artists += [i["description"]]
	countDict = Counter(artists)
	countDict = countDict.most_common(5)
	for i in countDict:
		labels += [i[0]]
		searches += [i[0]+' artist band rapper']
	src_list = []
	parameters = []
	for i in searches:
		parameters += [{"tbm" : "isch", "q" : i}]
	def srcGetter(x):
		URL = "https://www.google.com/search"
		r = requests.get(URL, params = x) 
		soup = BeautifulSoup(r.content, 'html5lib') 
		table = soup.find('table', attrs = {'class':'images_table'})
		img = table.find('img')
		src = img.get('src')
		return src
	for i in parameters:
		src_list += [srcGetter(i)]
	return render_template('img.html', title='Top Artists - 2019', src_list=src_list, labels=labels)
	
if __name__ == '__main__':
    app.run(host='127.0. 0.1', port=8080)