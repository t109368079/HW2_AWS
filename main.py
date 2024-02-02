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
            return redirect(url_for('display',usr=usr))
        else:
            user_info = {'pw':pw}
            data.update({usr:user_info})
            save_data(data)
            return redirect(url_for('user', usr=usr))
    else:
        return render_template('index.html')
    
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

@app.route('/display_<usr>')
def display(usr):
    data = load_data()
    user_info = data[usr]
    
    first_name = user_info['first_name']
    last_name = user_info['last_name']
    email = user_info['email']
    
    text = f"<h1>First Name: {first_name}<br>Last Name: {last_name}<br>Email: {email}</h1>"
                
    return text
           


if __name__ == '__main__':
    app.run()
    
