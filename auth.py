#!/usr/bin/python
# encoding: utf-8

import sys
import os
import re

from workflow import Workflow3, web

def main(wf):
    query = wf.args[0]
    wf.save_password('semaphoreci-auth-token', query)
    notify('SemaphoreCI', 'Auth Token set correctly.')
    wf.send_feedback()

if __name__ == '__main__':
    wf = Workflow3()
    sys.exit(wf.run(main))