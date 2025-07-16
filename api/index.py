from app import app

def handler(event, context):
    from flask import request
    from werkzeug.wrappers import Response
    from werkzeug.test import create_environ
    
    environ = create_environ(
        path=event['path'],
        method=event['httpMethod'],
        headers=dict(event.get('headers', {})),
        query_string=event.get('queryStringParameters', {}),
        json=event.get('body')
    )
    
    with app.request_context(environ):
        response = app.full_dispatch_request()
        
    return {
        'statusCode': response.status_code,
        'headers': dict(response.headers),
        'body': response.get_data(as_text=True)
    }
