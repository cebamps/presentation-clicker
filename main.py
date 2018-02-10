from twisted.internet import reactor
from twisted.web.server import Site
from twisted.web.resource import Resource

from autobahn.twisted.websocket import WebSocketServerFactory, WebSocketServerProtocol
# this one isn't documented, except in examples:
from autobahn.twisted.resource import WebSocketResource

from subprocess import call


keys = {
    b'n': 'Page_Down',
    b'p': 'Page_Up',
}

def run_action(message):
    print("Got ", message)
    key = keys.get(message, None)
    if key:
        call(['xdotool', 'key', key])

class RootResource(Resource):
    def render_GET(self, request):
        return open("./index.html", 'rb').read()

root = Resource()
root.putChild(b'', RootResource())


class ClickerProtocol(WebSocketServerProtocol):
    def onConnect(self, request):
        print("Got websocket connection request: ", request)

    def onMessage(self, payload, isBinary):
        run_action(payload)

clickerFactory = WebSocketServerFactory()
clickerFactory.protocol = ClickerProtocol

root.putChild(b'ws', WebSocketResource(clickerFactory))


site = Site(root)
reactor.listenTCP(8080, site)
reactor.run()
