from bottle import static_file, route, run, template, request, post, get, hook, HTTPResponse, default_app, Bottle
import os
from os import listdir, path
import time

app = Bottle()

@app.route('/getfeedbacks/<game>')
def getFeedbacks(game):
    treatedGameName = game.replace('.','')
    treatedGameName = treatedGameName.replace('/','')
    treatedGameName = treatedGameName.replace('\\','')
    gamepath = './feedback/'+treatedGameName

    if not path.isdir(gamepath): return

    
    fileNames = listdir('./feedback/'+game)
    returnString = ''
    for fName in fileNames:
        f = open(gamepath+'/'+fName, 'rt')

        fileAsString = f.read()
        f.close()
        returnString += '<br><br>'
        fileAsString = fileAsString.replace('\n','<br>')
        returnString = returnString + '<p>'
        returnString = returnString + fileAsString
        returnString = returnString + '</p>'

        f.close()
    
    return returnString

@app.route('/feedback/<game>', method='POST')
def feedback(game):
    treatedGameName = game.replace('.','')
    treatedGameName = treatedGameName.replace('/','')
    treatedGameName = treatedGameName.replace('\\','')
    maxFeedbackLength = 1024*16
    if len(request.body.getvalue()) > maxFeedbackLength: return

    if not path.isdir('./feedback/'+treatedGameName): return

    address = request.environ.get('HTTP_X_FORWARDED_FOR')
    if not address:
        address = request.environ.get('REMOTE_ADDR')
    feedbackString = request.body.getvalue().decode('utf-8')
    feedbackString = feedbackString.replace('<', "&lt;").replace('>', "&gt;")
    feedbackString = '\n'+feedbackString

    filepath = "./feedback/"+treatedGameName+'/'+address
    if path.exists(filepath):
        if os.path.getsize(filepath) > 1024*16*4:
            return
    oFile = open(filepath, "at")
    oFile.write(feedbackString)
    oFile.close()
    return
    
#application = default_app()
