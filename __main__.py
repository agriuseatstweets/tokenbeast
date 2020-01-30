from gevent.pywsgi import WSGIServer
from auth import app
import logging, os

logging.basicConfig(level = logging.DEBUG)

http_server = WSGIServer(('', int(os.environ.get('PORT', 5000))), app)
http_server.serve_forever()
