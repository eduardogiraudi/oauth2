from flask import Response
from json import dumps

def bad_request(err, descr):
    return Response(
        response=dumps({
            'error': err,
            'error_description': descr
        }),
        status=400,  
        mimetype='application/json',  
        headers={
            "Cache-Control": "no-store",  
            "Pragma": "no-cache"
        }
    )
def not_found(err, descr):
    return Response(
        response=dumps({
            'error': err,
            'error_description': descr
        }),
        status=404,  
        mimetype='application/json',  
        headers={
            "Cache-Control": "no-store",  
            "Pragma": "no-cache"
        }
    )
def unauthorized(err, descr):
    return Response(
        response=dumps({
            'error': err,
            'error_description': descr
        }),
        status=401,  
        mimetype='application/json',  
        headers={
            "Cache-Control": "no-store",  
            "Pragma": "no-cache"
        }
    )
def temporarily_unavailable(descr):
    return Response(
        response=dumps({
            'error': 'temporarily_unavailable',
            'error_description': descr
        }),
        status=503,
        mimetype='application/json',
        headers={
            "Cache-Control": "no-store",
            "Pragma": "no-cache"
        }
    )
def server_error():
    return Response(
        response=dumps({
            'error': 'server_error',
            'error_description': 'Internal server error'
        }),
        status=500,
        mimetype='application/json',
        headers={
            "Cache-Control": "no-store",
            "Pragma": "no-cache"
        }
    )
def forbidden(descr):
    return Response(
        response=dumps({
            'error': 'forbidden',
            'error_description': descr
        }),
        status=403,
        mimetype='application/json',
        headers={
            "Cache-Control": "no-store",
            "Pragma": "no-cache"
        }
    )

def ok(data):
    return Response(
        response=dumps({'message':data}),  
        status=200,  
        mimetype='application/json' 
    )