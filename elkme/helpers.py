#!/usr/bin/env python

import sys
import json

if sys.version_info < (3,):
    def b(x):
        return x

    def s(x):
        return x
else:
    def b(x):
        return bytes(x, 'utf-8')

    def s(x):
        return x.decode('utf-8')


def parse_payload(payload):
    if not isinstance(payload, str):
        payload = ' '.join(payload)

    try:
        json.loads(payload)
    except ValueError:
        kv = payload.split(' ', 1)
        payload = '{"%s": "%s"}' % (kv[0], kv[1])

    return payload

def requires_elements(xs, dictionary):
    missing_values = []
    for x in xs:
        if x not in dictionary:
            missing_values.append(x)
    if missing_values:
        err_msg = ', '.join(missing_values)
        raise KeyError('Missing values %s' % (err_msg))

