# Basic server to serve static files
from flask import Flask

# Set the static url path to '' to redirect unrouted urls to the static folder
# This allows us to serve static files without having to prepend /static to them.
app = Flask(__name__, static_url_path='')


# Send the index.html file when accessing the root url
@app.route('/')
def root():
    return app.send_static_file('index.html')


if __name__ == '__main__':
    app.run()