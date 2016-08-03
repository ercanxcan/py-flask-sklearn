__author__ = 'ercan.can'

import numpy as np
from os import abort
from flask import Flask,json,jsonify,request, make_response
from functools import wraps
from linear_regression import lr
from logistic_regression import lg
from naive_bayes import nb
import requests
import json

app = Flask(__name__)

def check_auth(username, password):
    return username == 'ercan' and password == '123456'

def authenticate():
    message = {'message': "Authenticate."}
    resp = jsonify(message)

    resp.status_code = 401
    resp.headers['WWW-Authenticate'] = 'Basic realm="Example"'

    return resp

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth:
            return authenticate()

        elif not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)

    return decorated

@app.route('/')
def hello_world():
    return 'Welcome to IOT Rest Client!'


# curl http://127.0.0.1:8000/hello?name=ercan
@app.route('/hello')
def api_hello():
    if 'name' in request.args:
        return 'Hello ' + request.args['name']
    else:
        return 'Ercan Can'

@app.route('/path/<string:name>', methods=['GET'])
def path_variable(name):
    return name

#curl -H "Content-type: application/json" -X POST http://127.0.0.1:8000/messages -d '{"msg":"test json data"}'
#curl -H "Content-type: application/octet-stream" -X POST http://127.0.0.1:8000/messages --data-binary @CYCLES_TEST~15.sql
@app.route('/messages', methods = ['POST'])
def api_message():

    if request.headers['Content-Type'] == 'text/plain':
        return "Text Message: " + request.data

    elif request.headers['Content-Type'] == 'application/json':
        return "JSON Message: " + json.dumps(request.json)

    elif request.headers['Content-Type'] == 'application/octet-stream':
        f = open('./binary', 'wb')
        f.write(request.data)
        f.close()
        return "Binary message written!"

    else:
        return "415 Unsupported Media Type ;)"


#curl -v -u "ercan:123456" http://127.0.0.1:8000/secrets
@app.route('/secrets')
@requires_auth
def get_secret_method():
    return "Secret method..."


# curl -H "Content-type: application/json" -X POST http://127.0.0.1:8000/postString -d '{"msg":"test json data"}'
@app.route('/postString', methods=["POST"])
def postString():
    f = request.get_data()
    return "Your posted data is : " + f


# curl -v http://127.0.0.1:8000/doc/test
@app.route('/doc/test')
def getDocument():
    return app.send_static_file('test.dat')

#curl -v -u "ercan:123456" http://127.0.0.1:8000/predict/lr/100.3
@app.route('/predict/lr/<float:input1>')
def prediction_lr(input1):
    prediction = lr.get_lr(input1)
    output = json.dumps({'prediction':json.dumps(set(prediction), cls=SetEncoder)})
    # addlog('LinearRegression',request.base_url,np.array_str(prediction))
    return output

#curl -v -u "ercan:123456" http://127.0.0.1:8000/predict/lg/0.76868572/3.16466081/1.30319059/0.45436659/0.61572467
@app.route('/predict/lg/<float:input1>/<float:input2>/<float:input3>/<float:input4>/<float:input5>')
# @requires_auth
def prediction_lg(input1,input2,input3,input4,input5):
    prediction = lg.get_lg(input1,input2,input3,input4,input5)
    output = json.dumps({'prediction': np.array_str(prediction)})
    # addlog('LogisticRegression',request.base_url,np.array_str(prediction))
    return output

#curl -v -u "ercan:123456"

@app.route('/predict/ng/<float:input1>/<float:input2>/<float:input3>/<float:input4>/<float:input5>/<float:input6>/<float:input7>/<float:input8>')
@requires_auth
def prediction_ng(input1,input2,input3,input4,input5,input6,input7,input8):
    prediction = nb.get_nb(input1,input2,input3,input4,input5,input6,input7,input8)
    output = json.dumps({'prediction':json.dumps(set(prediction), cls=SetEncoder)})
    # addlog('NaiveBayes',request.base_url,np.array_str(prediction))
    return output

@app.route('/addlog')
def addlogtest():
    return addlog('code','input','output')

def addlog(code,input,output):
    url = 'http://localhost:8080/dashboard/addlog'
    data = {'code':code,'algorithmInput':input,'algorithmOutput':output}
    headers = {'Content-Type': 'application/json'}
    r = requests.post(url, data=json.dumps(data), headers=headers)
    return r.text

#curl -v http://127.0.0.1:8000/sensor/55.0/1.7/2.2/2.3/4.5
@app.route('/sensor/<float:sensor1>/<float:sensor2>/<float:sensor3>/<float:sensor4>/<float:sensor5>')
def sensor_status(sensor1,sensor2,sensor3,sensor4,sensor5):
    return json.dumps({'sensor1':sensor1,'sensor2':sensor2,'sensor3':sensor3,'sensor4':sensor4,'sensor5':sensor5})

tasks = [
    {
        'id': 1,
        'title': u'Title1',
        'description': u'desc1,desc2,desc3',
        'done': False
    },
    {
        'id': 2,
        'title': u'Title2',
        'description': u'desc1,desc2,desc3',
        'done': False
    }
]
@app.route('/todo/api/v1.0/tasks', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': tasks})

@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    return jsonify({'task': task[0]})

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

#curl -i -H "Content-Type: application/json" -X POST -d '{"title":"Read a book"}' http://localhost:5000/todo/api/v1.0/tasks
@app.route('/todo/api/v1.0/tasks', methods=['POST'])
def create_task():
    if not request.json or not 'title' in request.json:
        abort(400)
    task = {
        'id': tasks[-1]['id'] + 1,
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        'done': False
    }
    tasks.append(task)
    return jsonify({'task': task}), 201

@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'title' in request.json and type(request.json['title']) != unicode:
        abort(400)
    if 'description' in request.json and type(request.json['description']) is not unicode:
        abort(400)
    if 'done' in request.json and type(request.json['done']) is not bool:
        abort(400)
    task[0]['title'] = request.json.get('title', task[0]['title'])
    task[0]['description'] = request.json.get('description', task[0]['description'])
    task[0]['done'] = request.json.get('done', task[0]['done'])
    return jsonify({'task': task[0]})

@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    tasks.remove(task[0])
    return jsonify({'result': True})


class SetEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        return json.JSONEncoder.default(self, obj)

if __name__ == '__main__':
    '''
    # app.run() default port 8000
    # app.run(debug=True,port=8000)
    # (debug=True,port=8000) debug=True when file is change auto deploy to server
    # app.run("0.0.0.0", 8000)
    '''
    app.run(debug=True,port=8000)
