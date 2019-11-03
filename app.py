from flask import Flask
from flask import render_template
from flask import request
from flask import session
from flask import redirect
from flask import url_for
from random import uniform
from config import CFG

app = Flask(__name__, static_folder='static')

stateOfSomething1 = 0
stateOfSomething2 = 0

@app.route('/')
def mainPage():
    if 'login' not in session:
        return redirect('/auth')
    
    return render_template('main.html')

@app.route('/auth', methods = ['GET', 'POST'])
def authPage():
    if 'login' in session:
        return redirect('/')
    
    login = request.values.get('login')
    password = request.values.get('password')
    
    d = {}
    
    if login != None and password != None:
        if login in CFG['users']:
            if CFG['users'][login]['password'] == password:
                session['login'] = login
                print('User {} logged in'.format(login))
                return redirect('/')
            else:
                d['errorMessage'] = 'Incorrect login or/and password';
        else:
            d['errorMessage'] = 'Incorrect login or/and password';
    
    return render_template('auth.html', **d)

@app.route('/logout')
def logoutPage():
    if 'login' in session:
        print('User {} logged out'.format(session['login']))
        session.pop('login')
        
    return redirect('/auth')

@app.route('/settings')
def settingsPage():
    if 'login' not in session:
        return redirect('/auth')
    
    return render_template('settings.html')

@app.route('/about')
def aboutPage():
    if 'login' not in session:
        return redirect('/auth')
    
    return render_template('about.html')

@app.route('/api/getData')
def apiGetData():
    if 'login' not in session:
        return {}
    
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
    if 'login' not in session:
        return {}
    
    global stateOfSomething1
    
    newState = request.args.get('newState')
    if newState in [0, 1, '0', '1']:
        stateOfSomething1 = newState
        return {'result': 1}
    else:
        return {'result': 0}

@app.route('/api/changeStateOfSomething2', methods = ['GET'])
def apiChangeStateOfSomething2():
    if 'login' not in session:
        return {}
    
    global stateOfSomething2
    
    newState = request.args.get('newState')
    if newState in [0, 1, '0', '1']:
        stateOfSomething2 = newState
        return {'result': 1}
    else:
        return {'result': 0}

@app.errorhandler(404)
def notFoundPage(error):
    if 'login' in session:
        return render_template('error_with_menu.html'), 404
    else:
        return render_template('error.html'), 404

if __name__ == '__main__':
    app.secret_key = CFG['secret_key']
    app.run(host='0.0.0.0', port = CFG['port'], debug = CFG['debug'])
