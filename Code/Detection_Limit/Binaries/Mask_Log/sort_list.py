#!/usr/bin/env python

location = raw_input('Enter file name & location: ')
info = open(location, 'r')

file = info.readlines()
file = file[0]
fixed = file.split(' ')
x = open(location, 'w')

for i in fixed:
    x.write(i+'\n')
x.close()