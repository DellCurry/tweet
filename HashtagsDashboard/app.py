from flask import Flask,jsonify,request
from flask import render_template
from flask import render_template, g, redirect, Response, url_for
from flask_apscheduler import APScheduler
from datetime import timedelta
import ast
import os,sys
from scraper import twitter_scraper
from twitter_trends import getHot
tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
stat_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
app = Flask(__name__,static_folder=stat_dir,template_folder=tmpl_dir)

app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(seconds=1)
labels = []
values = []
hot = []
top=[]
rec=[]

class Config(object): 
    JOBS = [  
        { 
            'id': 'job1',
            'func': '__main__:Hot', 
            'trigger': 'interval',
            'seconds': 300,
        }
    ]

def Hot():
    global hot
    try:
        hot = getHot()
    except:
        e = sys.exc_info()[0]
        print("Error: %s" % e)
    
    print("hot=",hot)
    return redirect("/")

app.config.from_object(Config())

@app.route("/")
def chart():
    return render_template('chart.html', values=values, labels=labels,hot=hot,top=top,rec=rec)


@app.route('/refreshData')
def refresh_graph_data():
    global labels, values,hot
    return jsonify(sLabel=labels, sData=values,sHot=hot)


@app.route('/updateData', methods=['POST'])
def update_data_post():
    global labels, values
    if not request.form or 'data' not in request.form:
        return "error",400
    labels = ast.literal_eval(request.form['label'])
    values = ast.literal_eval(request.form['data'])
    # print("labels received: " + str(labels))
    # print("data received: " + str(values))
    return "success",201

@app.route('/getTop',methods=['POST'])
def getTop():
    global rec,top
    if not request.form or 'topic' not in request.form:
        return "error",400
    topic = request.form['topic']
    top6 = twitter_scraper(topic)
    top = [top6[0]]
    rec = top6[1:]
    return redirect('/')

if __name__ == "__main__":
    Hot()
    scheduler=APScheduler()
    scheduler.init_app(app)
    scheduler.start()
    app.run(host='localhost', port=80,debug=True)

