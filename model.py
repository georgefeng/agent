# -*- coding: utf-8 -*-

import argparse


def action_parser(action_str):
    parser = argparse.ArgumentParser(description='Action app')
    parser.add_argument('task', help="Please input the task name.")
    parser.add_argument('-f', '--freq', default=2, type=int)
    parser.add_argument('-c', '--create', type=int, dest='createdAt', default=19700101000000)
    parser.add_argument('-n', '--new', action="store_true", dest='is_new', help='Add a new task.')
    parser.add_argument('-e', '--exec', action="store_true", dest='is_exec', help='Refresh last.')
    parser.add_argument('-u', '--update', action="store_true", dest='is_update')
    parser.add_argument('-d', '--delete', action="store_true", dest='is_delete')

    #
    # parser.add_argument('-a','--add', action="store_true", default=False)
    # parser.add_argument('-b', action="store", dest="babgaa")
    # parser.add_argument('-c', action="store", dest="c", type=int)

    return parser.parse_args(action_str.split(' '))

if __name__ == '__main__':
    # action_parser('-a 1')
    args = action_parser('中文 -c 1 -e -f 3')

    print(args)
    print(args.task)