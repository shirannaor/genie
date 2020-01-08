import eventlet
import socketio

sio = socketio.Server()
app = socketio.WSGIApp(sio)

@sio.on("connect")
def connect(sid,environ):
    print ("connect", sid)

@sio.on("newApprovedVisitor")
def msg(sid,data):
    print ("msg", data)

@sio.on("disconnect")
def disconnect(sid,environ):
    print ("disconnect", sid)

if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('', 5000)), app)