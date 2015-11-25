"""A helper utility to automatically create a database for the ACM-HSCC app

Author: Logan Gore
This file is responsible for (at the bare minimum) creating the database and
all associated tables for the ACM-HSCC app. It will import all models and
ensure that a table for each model exists.
"""

import argparse
import os
import sys

from hscc import db

from hscc.models import PasswordReset
from hscc.models import School
from hscc.models import User


PARSER = argparse.ArgumentParser(description='ACM-HSCC DB Creation Tool')
PARSER.add_argument(
    '-d', '--drop', action='store_true',
    help='Drop existing DB tables before recreation'
)
PARSER.add_argument(
    '-p', '--populate', action='store_true',
    help='Populate the DB with default values after creation'
)
PARSER.add_argument(
    '-v', '--verbose', action='store_true',
    help='Show extra output about which stage the script is executing'
)
ARGS = PARSER.parse_args()


def vprint(s='', endl='\n'):
    """Print a string if verbose mode is enabled"""
    if ARGS.verbose:
        sys.stderr.write('{s}{endl}'.format(s=s, endl=endl))


def populate_db_users():
    """Populate the database User model"""
    users = [
        User(
            name='ACM-HSCC Admin',
            email='acm@purdue.edu',
            password=os.environ['ACM_HSCC_ADMIN_PASSWORD'],
            school=None,
            team=None,
            grade=None,
            shirt_size=None,
            allergies=None,
            is_admin=True,
        ),
    ]
    db.session.add_all(users)
    db.session.commit()


def populate_db_all():
    """Completely populate a basic db for ACM-HSCC"""
    if 'ACM_HSCC_ADMIN_PASSWORD' not in os.environ:
        print('Please set env variable ACM_HSCC_ADMIN_PASSWORD first.')
        return False

    vprint('Starting DB population script...')
    populate_db_users()
    vprint('User model populated.')
    vprint('\nDB population script complete.')
    return True


if __name__ == '__main__':
    vprint('CreateDB script loaded.')

    if ARGS.drop:
        vprint('Dropping all existing data first!')
        db.session.close()
        db.drop_all()
        vprint('DB dropped.')

    db.create_all()
    vprint('All database models created.')

    res = True
    if ARGS.populate:
        res = populate_db_all()

    if res:
        vprint('CreateDB script exiting successfully.')
    else:
        vprint('CreateDB script exited with failure!')
