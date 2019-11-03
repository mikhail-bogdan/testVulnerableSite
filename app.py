from flask import Flask
from flask import render_template
from flask import request
from random import uniform

app = Flask(__name__, static_folder='static')

stateOfSomething1 = 0
stateOfSomething2 = 0

@app.route('/')
def indexPage():
    return render_template('index.html')

@app.route('/settings')
def settingsPage():
    return render_template('settings.html')

@app.route('/about')
def aboutPage():
    return render_template('about.html')

@app.route('/api/getData')
def apiGetData():
    global stateOfSomething1
    global stateOfSomething2
    
    tempMin = -20.0
    tempMax = 35.0
    temp = uniform(tempMin, tempMax);
    tempLoad = (temp - tempMin) / (tempMax - tempMin) * 100.0;
    tempAlert = temp > 27.0
    
    lightMin = 0.0
    lightMax = 400.0
    light = uniform(lightMin, lightMax)
    lightLoad = (light - lightMin) / (lightMax - lightMin) * 100.0
    lightAlert = light > 300.0
    
    humidityMin = 0.0
    humidityMax = 100.0
    humidity = uniform(humidityMin, humidityMax)
    humidityLoad = (humidity - humidityMin) / (humidityMax - humidityMin) * 100.0
    humidityAlert = humidity > 95
    
    return {
        'temperature': {
            'value': '{:.1f}'.format(temp),
            'load': tempLoad,
            'alert': tempAlert,
            'unit': '\u2103'
        },
        'light': {
            'value': '{:.1f}'.format(light),
            'load': lightLoad,
            'alert': lightAlert,
            'unit': 'lux'
        },
        'humidity': {
            'value': '{:.1f}'.format(humidity),
            'load': humidityLoad,
            'alert': humidityAlert,
            'unit': 'hum'
        },
        'stateOfSomething1': {
            'state': stateOfSomething1,
            'name': 'light1'
        },
        'stateOfSomething2': {
            'state': stateOfSomething2,
            'name': 'light2'
        }
    }

@app.route('/api/changeStateOfSomething1', methods = ['GET'])
def apiChangeStateOfSomething1():
    global stateOfSomething1
    
    newState = request.args.get('newState')
    if newState in [0, 1, '0', '1']:
        stateOfSomething1 = newState
        return {'result': 1}
    else:
        return {'result': 0}

@app.route('/api/changeStateOfSomething2', methods = ['GET'])
def apiChangeStateOfSomething2():
    global stateOfSomething2
    
    newState = request.args.get('newState')
    if newState in [0, 1, '0', '1']:
        stateOfSomething2 = newState
        return {'result': 1}
    else:
        return {'result': 0}

@app.errorhandler(404)
def not_found(error):
    return render_template('error.html'), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port = 5000, debug = True)
