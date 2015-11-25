from hscc import app

app.run(
    host=app.config['SERVER_HOST'],
    port=app.config['SERVER_PORT'],
    debug=app.config['DEBUG'],
)
