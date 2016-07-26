#!/usr/bin/env python

import sys
import json

def parse_payload(payload):
    if not isinstance(payload, str):
        payload = ' '.join(payload)

    try:
        json.loads(payload)
    except ValueError:
        kv = payload.split(' ', 1)
        if len(kv) > 1:
          payload = '{"%s": "%s"}' % (kv[0], kv[1])
        else:
          payload = '%s' % kv[0]

    return payload

