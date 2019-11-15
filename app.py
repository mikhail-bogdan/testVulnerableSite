from flask import Flask
from flask import render_template
from flask import request
from flask import session
from flask import redirect
from flask import url_for
from random import uniform
from config import CFG
from projectTypes import *

app = Flask(__name__, static_folder='static')

stateOfSomething1 = 0
stateOfSomething2 = 0


@app.route('/')
def mainPage():
    if 'login' not in session:
        return redirect('/auth')

    d = {}
    d['firstname'] = getUser(session['login']).firstname

    return render_template('main.html', **d)


@app.route('/myprofile')
def myProfile():
    if 'login' not in session:
        return redirect('/auth')
    user = getUser(session['login'])
    if (user == None):
        return redirect('/logout')
    d = {}

    d['login'] = user.username
    d['password'] = user.password
    d['firstname'] = user.firstname
    d['lastname'] = user.lastname
    d['age'] = user.age

    return render_template('myprofile.html', **d)


@app.route('/register', methods=['GET', 'POST'])
def registerPage():
    if 'login' in session:
        return redirect('/myprofile')

    d = {}

    username = request.values.get('login')
    password = request.values.get('password')
    firstname = request.values.get('firstname')
    lastname = request.values.get('lastname')
    age = request.values.get('age')
    if (request.method == 'POST'):
        if username != None and password != None:
            error = addUser(username, password, firstname, lastname, age);
            if error == None:
                session['login'] = username
                print('User {} registered'.format(username))
                return redirect('/myprofile')
            else:
                d['errorMessage'] = error;
        else:
            d['errorMessage'] = 'Wrong data'
    return render_template('register.html', **d)


@app.route('/auth', methods=['GET', 'POST'])
def authPage():
    if 'login' in session:
        return redirect('/myprofile')

    login = request.values.get('login')
    password = request.values.get('password')

    d = {}

    if (request.method == 'POST'):
        if login != None and password != None:
            if isUserRegistered(login):
                if isUserPasswordMatch(login, password):
                    session['login'] = login
                    print('User {} logged in'.format(login))
                    return redirect('/')
                else:
                    d['errorMessage'] = 'Incorrect login or/and password';
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


@app.route('/api/changeStateOfSomething1', methods=['GET'])
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


@app.route('/api/changeStateOfSomething2', methods=['GET'])
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


def isUserPasswordMatch(username, password):
    for user in users:
        if user.username == username and user.password == password:
            return True
    return False


def isUserRegistered(username):
    for user in users:
        if user.username == username:
            return True
    return False


def getUser(username):
    for user in users:
        if user.username == username:
            return user
    return None


def addUser(username, password, firstName, lastName, age):
    if isUserRegistered(username):
        return "Username is taken"
    newUser = User(username, password, firstName, lastName, age)
    users.append(newUser);
    return None


if __name__ == '__main__':
    pass
app.secret_key = CFG['secret_key']
app.run(host='0.0.0.0', port=CFG['port'], debug=CFG['debug'])
