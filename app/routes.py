from app import app


@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Pamirkhan'}
    return '''
                <html>
                    <head>
                        <title>Home Page - Blog</title>
                    </head>
                    <body>
                        <h1>Hello, ''' + user['username'] + '''!</h1>
                    </body>
                </html>
            '''
