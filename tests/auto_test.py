#!/usr/bin/env python
from utils import auto
import sys
from test_db_setup import *
bundle = {
    'mouth': "",
    'user': "uberj",
    'channel': "uberjderp",
    'msg': sys.argv[2],
    'idea': sys.argv[1], # The fist half of the parsed message
    'sensory_input':sys.argv[3] , # The second half of the parsed message
    'conn': conn,
    'cursor': cursor,
    'log': "fail" # legacy code already?
}

print auto(bundle)

