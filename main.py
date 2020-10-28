from os import path
from pathlib import Path
from flask import *
from flask import json as flaskjson
import json,os,sys
app = Flask(__name__,template_folder='.')
def addlang(name,url,*,fp="credit.json"):
    if not path.exists(fp):
        Path(fp).touch()
    f=open(fp,"r+")
    try:
        dat=json.load(f)
    except json.decoder.JSONDecodeError:
        dat={}
    f.close()
    try:
        dat['langs']
    except KeyError:
        dat.update({"langs":[]})
    try:
        dat['langs'].append({"name":name,"url":url})
    except AttributeError:
        dat['langs']=[{"name":name,"url":url}]
    f=open(fp,"w+")
    o=f.write(json.dumps(dat))
    f.close()
    return o
def addrepo(name,url,*,fp="credit.json"):
    if not path.exists(fp):
        Path(fp).touch()
    f=open(fp,"r+")
    try:
        dat=json.load(f)
    except json.decoder.JSONDecodeError:
        dat={}
    f.close()
    try:
        dat['repos']
    except KeyError:
        dat.update({"repos":[]})
    try:
        dat['repos'].append({"name":name,"url":url})
    except AttributeError:
        dat['repos']=[{"name":name,"url":url}]
    f=open(fp,"w+")
    o=f.write(json.dumps(dat))
    f.close()
    return o
def shutdown_server():
    func=request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
def addlib(name,url,lang,*,fp="credit.json"):
    if not path.exists(fp):
        Path(fp).touch()
    f=open(fp,"r+")
    try:
        dat=json.load(f)
    except json.decoder.JSONDecodeError:
        dat={}
    f.close()
    try:
        dat['libs']
    except KeyError:
        dat.update({"libs":[]})
    try:
        dat['libs'].append({"name":name,"url":url,"lang":lang})
    except AttributeError:
        dat['libs']=[{"name":name,"url":url,"lang":lang}]
    f=open(fp,"w+")
    o=f.write(json.dumps(dat))
    f.close()
    return o
def addmisc(name,details,*,fp="credit.json"):
    if not path.exists(fp):
        Path(fp).touch()
    f=open(fp,"r+")
    try:
        dat=json.load(f)
    except json.decoder.JSONDecodeError:
        dat={}
    f.close()
    try:
        dat['misc']
    except KeyError:
        dat.update({"misc":[]})
    if details.replace(" ","")=="":
        details=None
    try:
        dat['misc'].append({"name":name,"details":details})
    except AttributeError:
        dat['misc']=[{"name":name,"details":details}]
    f=open(fp,"w+")
    o=f.write(json.dumps(dat))
    f.close()
    return o
@app.route('/')
def index():
	return render_template('index.html')
@app.route("/lang")
def lang():
    name=request.args.get('name')
    url=request.args.get('url')
    addlang(name,url)
    return redirect(url_for('index'))
@app.route("/repo")
def repo():
    name=request.args.get('name')
    url=request.args.get('url')
    addrepo(name,url)
    return redirect(url_for('index'))
@app.route('/lib')
def lib():
    name=request.args.get('name')
    url=request.args.get('url')
    lang=request.args.get('lang')
    addlib(name,url,lang)
    return redirect(url_for('index'))
@app.route("/misc")
def misc():
    name=request.args.get('name')
    details=request.args.get('details')
    addmisc(name,details)
    return redirect(url_for('index'))
@app.route('/shutdown')
def shutdown():
    shutdown_server()
    return 'Server shutting down...'
app.run(host='0.0.0.0',port=3000)