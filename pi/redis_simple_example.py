#!/usr/bin/env python3 

import redis

if __name__ == '__main__':
    r = redis.Redis('localhost', port=6379, db=0, password='e101class')
    print("write to redis")
    r.set('robot','is cool')
    print("read from redis",r.get('robot'))

    
