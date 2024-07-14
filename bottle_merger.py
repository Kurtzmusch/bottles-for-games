from bottle import Bottle

import feedback_server
import announce_server


def mergeBottles():
    rootApp = Bottle()
    rootApp.merge(feedback_server.app)
    rootApp.merge(announce_server.app)
    return rootApp

