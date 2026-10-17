#!/usr/bin/env python

import sys


def main():
    args = sys.argv[1:]
    if args[0] == 'discover':
        print('hdhomerun device 1072F92A found at 192.168.0.2')
        return
    print('ch=none ss=80')


__name__ == '__main__' and main()
