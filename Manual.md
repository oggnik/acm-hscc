# Purdue ACM High School Coding Competition Registration Website

## Installation
1. After downloading the repo, you need to set the following environmental variables:
    * ACM_HSCC_DEBUG
    * ACM_HSCC_DB_USERNAME
    * ACM_HSCC_DB_PASSWORD
    * ACM_HSCC_DB_HOST
    * ACM_HSCC_DB_PORT
    * ACM_HSCC_DB_NAME
    * ACM_HSCC_MAIL_SERVER
    * ACM_HSCC_MAIL_PORT
    * ACM_HSCC_MAIL_USERNAME
    * ACM_HSCC_MAIL_PASSWORD
    * ACM_HSCC_MAIL_DEFAULT_SENDER
    * ACM_HSCC_MAIL_USE_TLS
    * ACM_HSCC_MAIL_USE_SSL
    * ACM_HSCC_SITE_URL
    * ACM_HSCC_APPLICATION_ROOT
    * ACM_HSCC_THREADS_PER_PAGE
    * ACM_HSCC_CSRF_SESSION_KEY
    * ACM_HSCC_SECRET_KEY
    * ACM_HSCC_SERVER_HOST
    * ACM_HSCC_SERVER_PORT
    * ACM_HSCC_ADMIN_PASSWORD

It helps to add these to a file (e.g. '~/.env_setup') and sourcing this from your .bashrc.

2. Start the virtual environment: `source venv/bin/activate`
3. Install the required modules: `pip install -r .requirements`
4. Install MySQL and the python wrapper
5. Create the user in MySQL defined in the environmental variables
6. Launch `python` and run
```
from hscc import db
db.create_all()
```

## Running locally
Launch the server by running `python run.py`

## Running in production
0. Install the previous on a server where you have admin privileges, I suggest DigitalOcean.
1. Install nginx
2. Run `uwsgi_start`
3. Add a new server location to nginx which points to 127.0.0.1:3205
    - The following adds the website on the '/hscc' subdirectory.  It can be accessed by visiting IP/hscc
```
server {
        location = /hscc{ rewrite ^ /hscc/; }
        location /hscc { try_files $uri @hscc; }
        location @hscc {
                include uwsgi_params;
                uwsgi_pass 127.0.0.1:3205;
        }
}
```
4. If you want to have acm.cs.purdue.edu/hscc link to the website, set up a reverse proxy on the acm website.