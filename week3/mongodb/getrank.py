#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from pymongo import MongoClient

def get_rank(user_id):
    client = MongoClient()
    db = client.shiyanlou
    contests = db.contests
    user_rawdata = contests.find().sort('user_id')
    userinfo = []
    for user in user_rawdata:
        uid = user.get('user_id')
        if not userinfo:
            score = user.get('score')
            submit_time = user.get('submit_time')
            userinfo.append([uid,score,submit_time])
            continue
        if uid != userinfo[-1][0]:
            score = user.get('score')
            submit_time = user.get('submit_time')
            userinfo.append([uid,score,submit_time])
        else:
            userinfo[-1][1] += user.get('score')
            userinfo[-1][2] += user.get('submit_time')

    userinfo = sorted(userinfo,key=lambda x:(int(x[1]),int(x[2])))
    print(userinfo)
    for index, user in enumerate(userinfo):
        userinfo[index].append(index + 1)
        if user_id == user[0]:
            rank = index + 1
            score = user[1]
            submit_time = user[2]

#    print(userinfo)
    
    return rank, score , submit_time

if __name__ == '__main__':
    
    try:
        user_id = int(sys.argv[1])
    except ValueError:
        print('User id should be a number!')

    userdata = get_rank(user_id)
    print(userdata)
