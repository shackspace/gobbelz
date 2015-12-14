#! /usr/bin/env python2
# -*- coding: utf-8 -*-

from flask import Flask, abort, request, redirect, jsonify
import json 
import os
import subprocess
from urllib.request import urlopen
from mpd import MPDClient
from gtts import gTTS

# TODO: we will be owned by this


app = Flask(__name__)
app.config.update(Debug=True)

@app.route('/')
def home():
    return("Welcome to gobbelz, say something!")

@app.route('/mpd/status')
def mpd_status():
    client = MPDClient()
    client.timeout = 10
    client.idletimeout = None
    client.connect("lounge.mpd.shack", 6600)
    answer = client.currentsong()
    state = client.status()
    client.close()
    client.disconnect()
    if 'artist' in answer:
        return jsonify(artist = answer['artist'],
                   title = answer['title'],
                   status = state['state'],
                   stream = 'false')
    elif 'name' in answer:
        return jsonify(name=answer['name'],
                       title=answer['title'],
                       stream='true',
                       status = state['state'])
    elif 'file' in answer:
        return jsonify(title=answer['file'],
                       status = state['state'],
                       stream='undef')
    else:
        return jsonify(error='unknown playback type')
    return jsonify(error='unknown playback type')

@app.route('/btc')
def btc():
    apiURL = "https://btc-e.com/api/2/btc_usd/ticker"
    s = urlopen(apiURL)#, eparams)
    r = s.read()
    r = r.strip()
    jsondata = r
    data = json.loads(jsondata)
    return jsonify(btc = data['ticker']['last'],
                   high = data['ticker']['high'],
                   low = data['ticker']['low'])
    
@app.route('/mpd/play')
def play():
    client = MPDClient()
    client.timeout = 10
    client.idletimeout = None
    client.connect("lounge.mpd.shack", 6600)
    client.play()
    client.close()
    client.disconnect()
    return jsonify(status='success', action='play')

@app.route('/mpd/pause')
def pause():
    client = MPDClient()
    client.timeout = 10
    client.idletimeout = None
    client.connect("lounge.mpd.shack", 6600)
    client.pause()
    client.close()
    client.disconnect()
    return jsonify(status='success', action='pause')
    
@app.route('/say/', methods=['POST'])
def say():
    if request.headers['Content-Type'] == 'application/json':
        data = json.loads(request.data.decode())
        text = data['text']
        if len(text) <= 300:
            try:
                print(text)
                from os.path import join,exists
                cache_dir='/opt/gobbelz-cache'
                cache_file = join(cache_dir,text.replace('/','_')+".mp3")
                if not exists(cache_file):
                    print("adding to cache")
                    # after this worked
                    try:
                        tts = gTTS(text=text, lang="de")
                        tmp_file = "/tmp/gobbelz.mp3"
                        tts.save(tmp_file)
                    except:
                         raise
                         #return jsonify(status="error",error="could not retrieve tts from google")
                    import os
                    print("renaming")
                    os.rename(tmp_file,cache_file)
                else:
                   print("playing from cache")
                return_code = subprocess.check_call(["mpg123", cache_file])
            except:
                print("falling back to espeak ...")
                subprocess.check_call(['espeak', '-vde',text])
        else:
            return(jsonify(
                status='error',
                error='Your text exceeded the limit of 300 chars'))
        
        return(jsonify(
            status='success',
            text=data['text']))
    elif request.headers['Content-Type'] == 'text/plain':
        text = request.data.decode('utf-8')
        if len(text) <= 300:
            print(text)
            args = ['espeak', '-vde']
            args.append(text)
            p = subprocess.check_call(args)
        else:
            return "error: Your text exceeded the limit of 300 chars"
        
        return "success: {}".format(text)
  
    else:
        return(jsonify(
            status='error',
            error='Unknown Content-Type, please use "application/json"'))
        

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8081, debug=True)
