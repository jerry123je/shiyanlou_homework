#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import pandas as pd
import os, sys

def analysis(filename, user_id):
    times = 0
    minutes = 0
    files = open(filename,'r').read()
    data = pd.read_json(files)
    times = data['user_id'].where(data['user_id']==user_id).count()
    if times == 0:
        print('Can not find user!')
        exit(0)
    minutes = data['minutes'].where(data['user_id']==user_id).sum()
    return times, minutes

def usage():
    print('Useage: %s xx.json userid')
    exit(0)

if len(sys.argv) != 3:
    usage()
else:
    filename = sys.argv[1]
    if not os.path.exists(filename):
        usage()
    try:
        user_id = int(sys.argv[2])
    except ValueError:
        usage()
    times,minutes = analysis(filename,user_id)

