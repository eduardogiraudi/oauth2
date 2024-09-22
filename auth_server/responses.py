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
