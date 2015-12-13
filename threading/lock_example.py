#!/usr/bin/env python

from atexit import register
from random import randrange
from threading import Thread, Lock, currentThread
from time import ctime, sleep


class CleanOuputSet(set):
    def __str__(self):
        return ', '.join(x for x in self)


lock = Lock()
loops = (randrange(2,5) for x in xrange(randrange(3,7)))
remaining = CleanOuputSet()


def loop(n_seconds):
    my_name = currentThread().name
    with lock:
        remaining.add(my_name)
        print '[{0}] Started {1}'.format(ctime(), my_name)
    sleep(n_seconds)
    with lock:
        remaining.remove(my_name)
        print '[{0}] Completed {1} ({2} seconds)'.format(
            ctime(), my_name, n_seconds)
        print '    (remaining: {0})'.format(remaining or 'None')


def main():
    for pause in loops:
        Thread(target=loop, args=(pause,)).start()


@register
def _atexit():
    print 'all DONE at:', ctime()


if __name__ == "__main__":
    main()
