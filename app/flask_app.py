'''
A flask application for controlled experiment on
the attention on clickbait healdines
'''

# imports
from flask import Flask, render_template, url_for, redirect, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date, timedelta
import random , string
import json
import datetime
import requests

# initializing the App and database
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///store.db'
db = SQLAlchemy(app)

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

# class Recall(db.Model):
#   u_id = db.Column(db.String, primary_key=True)
#   article_1 = db.Column(db.String)
#   score_1 = db.Column(db.Integer)
#   article_2 = db.Column(db.String)
#   score_2 = db.Column(db.Integer)
#   article_3 = db.Column(db.String)
#   score_3 = db.Column(db.Integer)

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
  global news_objects
  news_objects = []
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
    news_objects.append({
      'headline':headline,
      'paragraphs':paragraphs,
      'article_id':article_id
    })
  random.shuffle(news_objects)
  return

# read data json file
with open('data.json') as file:
  json_file = file.read()
  json_data = json.loads(json_file)

# read questions json file
# with open('questions.json') as file:
#   json_file = file.read()
#   json_questions = json.loads(json_file)

recall_items = []
articles_visited = []
#-------------------------------------------------

# PAGE 1
# app route : root
@app.route('/')
def index():
  global sequence
  sequence = 0
  global u_id
  u_id = generate_random_string(10)
  return render_template('index.html')

# PAGE 2
# app route : launch
@app.route('/launch')
def launch():
  generate_news_objects()
  return render_template('launch.html')

# PAGE 3
# app route : headlines
@app.route('/headlines')
def headlines():
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
  global position
  global time_spent
  global article_id
  global transaction_id
  global articles_visited
  
  # generate transaction id
  transaction_id = generate_random_string(15)
  # position of news link on web matrix
  position = request.args.get('position')
  # time spent on page before clicking on news link
  time_spent = request.args.get('time_spent')
  news_piece = news_objects[int(position)]
  article_id = news_piece['article_id']
  headline = news_piece['headline']
  paragraphs = news_piece['paragraphs']
  # add article id to visited array, for recall test
  articles_visited.append(article_id)
  return render_template('article.html', headline=headline, paragraphs=paragraphs)

# PAGE 5
# app route : log_transactions
@app.route('/log_transaction')
def log_transaction():
  global sequence
  sequence+=1
  ts = datetime.datetime.now().timestamp()
  read_time = request.args.get('read_time')
  ip = request.remote_addr
  new_transaction = Transactions(timestamp=ts,ip=ip,tran_id=transaction_id,u_id=u_id,article_id=article_id,\
  position=position,time_before_click=time_spent,time_on_page=read_time, sequence=sequence)
  db.session.add(new_transaction)
  db.session.commit()
  print(sequence)
  if sequence == 3:
    sequence = 0
    # return redirect('/recall_test')
    return redirect('/details')
  else:
    return redirect('/headlines')

#---------------------------------------

#########################################
# CODE NOT BEING USED STARTING FROM HERE
#########################################

# # app route : recall_test
# @app.route('/recall_test')
# def recall_test():

#   global articles_visited
#   global questions
#   global recall_items

#   questions = []
#   questions_list = []

#   for i in articles_visited:
#     if i == '00' or i == '01':
#       recall_items.append('train')
#     elif i == '10' or i == '11':
#       recall_items.append('law')
#     elif i == '20' or i == '21':
#       recall_items.append('justice')
#     elif i == '30' or i == '31':
#       recall_items.append('apple')
#     elif i == '40' or i == '41':
#       recall_items.append('volcano')
#     elif i == '50' or i == '51':
#       recall_items.append('delhi')
  
#   for i in recall_items:
#     questions_list.append({'id': i, 'questions': json_questions[i]})
#   for i in questions_list:
#     for j in range(0,4):
#       questions.append({'id':i['id']+str(j),'question':i['questions'][j]['question'],\
#        'options':i['questions'][j]['options'],'correct':i['questions'][j]['correct']})
#   random.shuffle(questions)
#   for i in questions:
#     random.shuffle(i['options'])
#   return render_template('recall.html', questions=questions, articles=recall_items)


# # save recall data to log
# @app.route('/save_to_log')
# def save_to_log():
#   global u_id
#   incoming_ids = []
#   score = [0 for i in range(0,len(recall_items))]
#   for i in recall_items:
#     for j in range(0,4):
#       incoming_ids.append(i+str(j))
#   responses = []
#   for i in incoming_ids:
#     responses.append(request.args.get(i))
#   for i in range (len(recall_items)):
#     for j in range (len(incoming_ids)):
#       if recall_items[i] in incoming_ids[j] and responses[j] == '0':
#         score[i]+=1

#   new_recall = Recall(u_id=u_id,article_1=recall_items[0],\
#   score_1=score[0],article_2=recall_items[1],score_2=score[1],\
#    article_3 = recall_items[2], score_3 = score[2])
#   db.session.add(new_recall)
#   db.session.commit()
#   return redirect('/details')

#########################################
# CODE NOT BEING USED UP UNTIL HERE
#########################################

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
  global u_id
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