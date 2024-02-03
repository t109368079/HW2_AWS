# -*- coding: utf-8 -*-
"""
Created on Sat Jan 27 18:22:25 2024

@author: User
"""
import pickle
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)

def load_data():
    with open('data.pkl', 'rb') as f:
        data = pickle.load(f)
    return data

def save_data(data):
    with open('data.pkl', 'wb') as f:
        pickle.dump(data, f)
    return 

@app.route('/', methods=['POST', 'GET'])
def home():
    if request.method == 'POST':
        data = load_data()
        usr = request.form['username']
        pw = request.form['password']
        
        if usr in data.keys():
            usr_pw = data[usr]['pw']
            if pw == usr_pw:
                return redirect(url_for('display',usr=usr))
            else:
                message = 'Incorrect username or password. Please try again.'
                return render_template('index.html', warning_message=message)
        else:
            user_info = {'pw':pw}
            data.update({usr:user_info})
            save_data(data)
            return redirect(url_for('user', usr=usr))
    else:
        return render_template('index.html', warning_message=None)
    
@app.route('/user_<usr>', methods=['POST', 'GET'])
def user(usr):
    if request.method == 'POST':
        data = load_data()
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        
        data[usr].update({'first_name': first_name, 'last_name':last_name, 'email':email})
        save_data(data)
        return redirect(url_for('display',usr=usr))
    else:
        return render_template('user_detail.html')

@app.route('/display_<usr>',methods=['POST', 'GET'])
def display(usr):
    
    if request.method == 'POST':
        return redirect(url_for('home'))
    else:
        data = load_data()
        user_info = data[usr]
        
        first_name = user_info['first_name']
        last_name = user_info['last_name']
        email = user_info['email']

        return render_template('display.html', first_name=first_name, last_name=last_name, email=email)
           


if __name__ == '__main__':
    app.run()
    
