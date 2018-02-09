from twisted.internet import reactor
from twisted.web.server import Site
from twisted.web.resource import Resource

from subprocess import call

def home(request):
    return open("./index.html", 'rb').read()

def next(req):
    print("Got next")
    call(["sh", '-c' , 'xdotool key --window "$(xdotool search "Slides" | head -n1)" Right'])
    return b"ok"

def prev(req):
    print("Got prev")
    call(["sh", '-c' , 'xdotool key --window "$(xdotool search "Slides" | head -n1)" Left'])
    return b"ok"


class CallResource(Resource):
    def __init__(self, fun):
        Resource.__init__(self)
        self.fun = fun

    def render_GET(self, request):
        return self.fun(request)

root = Resource()
root.putChild(b'',     CallResource(home))
root.putChild(b'next', CallResource(next))
root.putChild(b'prev', CallResource(prev))

site = Site(root)
reactor.listenTCP(8080, site)
reactor.run()
