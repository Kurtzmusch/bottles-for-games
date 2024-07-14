from bottle import static_file, route, run, template, request, post, get, hook, HTTPResponse, default_app, Bottle
import os
from os import listdir, path
import time

app = Bottle()

servers = {}
keepAliveDeltaSeconds = 12

def updateList():
    global servers
    global keepAliveDeltaSeconds
    serversExpired = []
    for fullAddress, serverMeta in servers.items():
        if time.time() - serverMeta['lastTouch'] > keepAliveDeltaSeconds:
            serversExpired.append(fullAddress)
    for fullAddress in serversExpired:
        servers.pop(fullAddress)
            

def keepAlive(serverAddress):
    global servers
    return False

@app.route('/announce/<port>/<servername>')
def announce(port, servername):
    global servers
    serverAddress = request.environ.get('HTTP_X_FORWARDED_FOR')
    if not serverAddress:
        serverAddress = request.environ.get('REMOTE_ADDR')
    treatedPort = port.replace('<', "&lt;").replace('>', "&gt;")
    treatedName = servername.replace('<', "&lt;").replace('>', "&gt;")

    fullAddress = serverAddress+':'+treatedPort
    servers[fullAddress] = {
        'name': treatedName,
        'lastTouch': time.time()
    }
    return 'announced'

@app.route('/unannounce/<port>')
def unanounce(port):
    global servers
    serverAddress = request.environ.get('HTTP_X_FORWARDED_FOR')
    if not serverAddress:
        serverAddress = request.environ.get('REMOTE_ADDR')

    fullAddress = serverAddress+':'+port
    servers.pop(fullAddress)
    return 'unannounced'

@app.route('/getservers')
def getServers():
    global servers
    updateList()
    responseString = ''
    for fullAddress, serverMeta in servers.items():
        responseString = responseString+fullAddress+':'+serverMeta['name']+'\n'
    return responseString

#application = default_app()
