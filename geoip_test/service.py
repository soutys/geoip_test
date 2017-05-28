#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''Service module

$ pip install -U .
$ python -m geoip_test.service
'''

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
    with_statement,
)

import logging

import geoip2.database
from flask import Flask
from flask.json import jsonify

from geoip_test.config import CFG


APP = Flask(__name__)
APP.config.update(CFG)
LOG_HNDLR = logging.StreamHandler()
LOG_HNDLR.setLevel(logging.NOTSET if APP.debug else logging.ERROR)
LOG_HNDLR.setFormatter(
    logging.Formatter(
        fmt='%(asctime)s %(name)s'
            ' %(levelname)s %(module)s:%(lineno)s %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'))
APP.logger.addHandler(LOG_HNDLR)

APP.geolite_country_db = geoip2.database.Reader(
    CFG['GEOLITE_DB']['country'], locales=['en'], mode=geoip2.database.MODE_MMAP)
APP.geolite_city_db = geoip2.database.Reader(
    CFG['GEOLITE_DB']['city'], locales=['en'], mode=geoip2.database.MODE_MMAP)

LOG = logging.getLogger(__name__)


def _json_response(data_dc, status=200):
    '''Creates HTTP response object with appropriate headers for JSON data
    '''
    resp = jsonify(**data_dc)
    resp.headers['Server'] = 'Flask'
    resp.status_code = status
    return resp


@APP.errorhandler(404)
def not_found(_):
    '''HTTP 404 error handler
    '''
    return _json_response({'error': True, 'status': 404}, status=404)


@APP.errorhandler(405)
def method_not_allowed(_):
    '''HTTP 405 error handler
    '''
    return _json_response({'error': True, 'status': 405}, status=405)


@APP.errorhandler(400)
def bad_request(_):
    '''HTTP 400 error handler
    '''
    return _json_response({'error': True, 'status': 400}, status=400)


@APP.errorhandler(500)
def internal_server_error(_):
    '''HTTP 500 error handler
    '''
    return _json_response({'error': True, 'status': 500}, status=500)


@APP.route('/city/<ip_str>', methods=['GET'])
def get_city(ip_str=None):
    '''Returns city
    '''
    if not ip_str:
        return _json_response({'error': True, 'status': 400}, status=400)

    try:
        country_db_res = APP.geolite_country_db.country(ip_str)
    except ValueError:
        return _json_response({'error': True, 'status': 412}, status=412)

    try:
        city_db_res = APP.geolite_city_db.city(ip_str)
    except ValueError:
        return _json_response({'error': True, 'status': 412}, status=412)

    return _json_response(
        {
            'error': False,
            'status': 200,
            'country_by_country_db': country_db_res.country.iso_code,
            'country_by_city_db': city_db_res.country.iso_code},
        status=200)


if __name__ == '__main__':
    APP.run(host=APP.config['HOST'], port=APP.config['PORT'])
