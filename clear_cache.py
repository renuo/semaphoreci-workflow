#!/usr/bin/python
# encoding: utf-8

import sys
import os
import re

from workflow import Workflow3, web
from workflow.notify import notify

def main(wf):
    wf.clear_cache()    
    notify('SemaphoreCI', 'Cache cleared successfully!')
    wf.send_feedback()

if __name__ == '__main__':
    wf = Workflow3()
    sys.exit(wf.run(main))