#!/usr/bin/env python
#
# Example 1
#
import os
import sys

print ('loaded example')

def hello(name):
    print ("hello %s" % name) # they say this will work in python 2.7 too!

def many(args,kwargs):
    print(args)
    print(kwargs)

def manyargs(*args, **kwargs):
    print ('positional arguments')
    for ii,a in enumerate(args):
        print( '[%d] %s' % (ii,a))
    print ('keyword arguments')
    for k,v in sorted(kwargs.items()):
        print('%s: %s' % (k,v))

if __name__ == '__main__':
    hello('bob')
