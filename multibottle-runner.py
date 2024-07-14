from bottle import Bottle

import bottle_merger

application = bottle_merger.mergeBottles()
application.run(debug=True)
