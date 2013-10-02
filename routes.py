#! /usr/bin/python3
# -*- coding: utf-8 -*-

from flask import Flask, abort, request, redirect, jsonify
import simplejson
import os

app = Flask(__name__)
app.config.update(Debug=True)

@app.route('/')
def home():
    return("Welcome to gobbelz, say something!")
    
@app.route('/say/', methods=['POST'])
def say():
    if request.headers['Content-Type'] == 'application/json':
        data = simplejson.loads(request.data)
        text = data['text']
        if len(text) <= 300:
            print("ohai")
            print(os.getcwd())
            os.system(os.getcwd() + '/gobbelz/naturalvoices.att ' + text + " &")
        else:
            return(jsonify(
                status='error',
                error='Your text exceeded the limit of 300 chars'))
        
        return(jsonify(
            status='success',
            text=data['text']))

    else:
        return(jsonify(
            status='error',
            error='Unknown Content-Type, please use "application/json"'))
        

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
