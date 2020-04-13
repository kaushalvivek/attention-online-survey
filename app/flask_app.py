'''
A flask application for controlled experiment on
the attention on clickbait healdines
'''

# imports
from flask import Flask, render_template, url_for, redirect, request, jsonify, session
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date, timedelta
import random , string
import json
import datetime
import requests
# import os

# initializing the App and database
app = Flask(__name__)
SESSION_TYPE = 'filesystem'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///store.db'
db = SQLAlchemy(app)

app.config.from_object(__name__)
Session(app)
# app.secret_key= os.urandom(24)

#-------------------------------------------------
# model for storage of page transactions
class Transactions(db.Model):
  timestamp = db.Column(db.String)
  ip=db.Column(db.String)
  tran_id = db.Column(db.String, primary_key=True)
  u_id = db.Column(db.String)
  article_id = db.Column(db.String)
  position = db.Column(db.Integer)
  time_before_click = db.Column(db.String)
  time_on_page = db.Column(db.String)
  sequence = db.Column(db.Integer)

class Users(db.Model):
  timestamp = db.Column(db.String)
  u_id = db.Column(db.String, primary_key=True)
  age = db.Column(db.String)
  gender = db.Column(db.String)
  residence = db.Column(db.String)
  edu_level = db.Column(db.String)
  edu_stream = db.Column(db.String)
  news_source = db.Column(db.String)
  news_interest = db.Column(db.String)
#-------------------------------------------------

# function for generation of random string
def generate_random_string(stringLength=10):
  letters = string.ascii_lowercase
  return ''.join(random.choice(letters) for i in range(stringLength))

# to generate 6 news objects
def generate_news_objects():
  news = []
  choices = [0,0,0,1,1,1]
  random.shuffle(choices)
  for i in range(0,6):
    if(choices[i] == 0) :
      headline = json_data['articles'][i]['cb_headline']
      article_id = str(i)+'0'
    else:
      headline = json_data['articles'][i]['ncb_headline']
      article_id = str(i)+'1'
    paragraphs = json_data['articles'][i]['paragraphs']
    news.append({
      'headline':headline,
      'paragraphs':paragraphs,
      'article_id':article_id
    })
  random.shuffle(news)
  return news

# read data json file
with open('data.json') as file:
  json_file = file.read()
  json_data = json.loads(json_file)

#-------------------------------------------------

# PAGE 1
# app route : root
@app.route('/')
def index():
  session['articles_visited'] = []
  session['sequence'] = 0
  session['u_id'] = generate_random_string(10)
  return render_template('index.html')

# PAGE 2
# app route : launch
@app.route('/launch')
def launch():
  session['news_objects'] = generate_news_objects()
  return render_template('launch.html')

# PAGE 3
# app route : headlines
@app.route('/headlines')
def headlines():
  news_objects = session.get('news_objects')
  sequence = session.get('sequence')
  h0 = news_objects[0]['headline']
  h1 = news_objects[1]['headline']
  h2 = news_objects[2]['headline']
  h3 = news_objects[3]['headline']
  h4 = news_objects[4]['headline']
  h5 = news_objects[5]['headline']
  return render_template('headlines.html', h0=h0, h1=h1, h2=h2, h3=h3, h4=h4, h5=h5, sequence=sequence)

# PAGE 4
# app route : article
@app.route('/article')
def article():
  news_objects = session.get('news_objects')
  # generate transaction id
  session['transaction_id'] = generate_random_string(15)
  # position of news link on web matrix
  session['position'] = request.args.get('position')
  # time spent on page before clicking on news link
  session['time_spent'] = request.args.get('time_spent')
  news_piece = news_objects[int(session.get('position'))]
  session['article_id'] = news_piece['article_id']
  headline = news_piece['headline']
  paragraphs = news_piece['paragraphs']
  # add article id to visited array, for recall test
  session['articles_visited'].append(session.get('article_id'))
  return render_template('article.html', headline=headline, paragraphs=paragraphs)

# PAGE 5
# app route : log_transactions
@app.route('/log_transaction')
def log_transaction():
  u_id = session.get('u_id')
  sequence = session.get('sequence')
  position = session.get('position')
  time_spent = session.get('time_spent')
  article_id = session.get('article_id')
  transaction_id = session.get('transaction_id')
  session['sequence'] = sequence + 1
  sequence = sequence = session.get('sequence')
  ts = datetime.datetime.now().timestamp()
  read_time = request.args.get('read_time')
  ip = request.remote_addr
  new_transaction = Transactions(timestamp=ts,ip=ip,tran_id=transaction_id,u_id=u_id,article_id=article_id,\
  position=position,time_before_click=time_spent,time_on_page=read_time, sequence=sequence)
  db.session.add(new_transaction)
  db.session.commit()
  if sequence == 3:
    sequence = 0
    # return redirect('/recall_test')
    return redirect('/details')
  else:
    return redirect('/headlines')

# app route : end
@app.route('/end')
def end():
  return render_template('end.html')

@app.route('/details')
def details():
  return render_template('details.html')

# save demographic form data submission
@app.route('/form_data', methods=['GET', 'POST'])
def form_data():
  u_id = session.get('u_id')
  age = request.args.get('age')
  gender = request.args.get('gender')
  residence = request.args.get('residence')
  edu_level = request.args.get('education_level')
  edu_stream = request.args.get('education_stream')
  news_source = request.args.get('newsSource')
  news_interest = request.args.get('newsInterest')
  ts = datetime.datetime.now().timestamp()
  new_user = Users(timestamp=ts,u_id=u_id,age=age,gender=gender,residence=residence, edu_level=edu_level, edu_stream=edu_stream,news_source=news_source, news_interest=news_interest)
  db.session.add(new_user)
  db.session.commit()
  return redirect('/end')

# ---------------------------------------

if __name__ == "__main__":
  app.run(debug=True)
