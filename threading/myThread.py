#!/usr/bin/env python

import threading
from time import ctime


class MyThread(threading.Thread):
    def __init__(self, function, args, name=''):
        super(MyThread, self).__init__()
        self.name = name
        self.function = function
        self.args = args

    def getResult(self):
        return self.result

    def run(self):
        print 'starting ', self.name, ' at:', ctime()
        self.result = self.function(*self.args)
        print self.name, ' finished at:', ctime()

