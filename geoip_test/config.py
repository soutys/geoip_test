# -*- coding: utf-8 -*-

'''Config module
'''

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
    with_statement,
)

import os


CFG = dict(
    DEBUG=False,
    HOST='127.0.0.1',
    PORT=9100,
    JSONIFY_PRETTYPRINT_REGULAR=False,
    GEOLITE_DB={
        'country': os.path.join(
            os.path.dirname(__file__), '..', 'GeoLite2-Country.mmdb'),
        'city': os.path.join(
            os.path.dirname(__file__), '..', 'GeoLite2-City.mmdb'),
    },
)
