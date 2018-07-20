#!/usr/bin/python
# encoding: utf-8

import sys
import os
import re

from workflow import Workflow3, web

def get_projects_list(auth_token):
    alfred_projects = []
    url = 'https://semaphoreci.com/api/v1/projects'
    params = dict(auth_token=auth_token)
    r = web.get(url, params)
    r.raise_for_status()
    alfred_projects = r.json()
    return sorted(alfred_projects, key=lambda project: project['name'].lower())

def main(wf):
    def wrapper():
        auth_token = wf.get_password('semaphoreci-auth-token')
        return get_projects_list(auth_token)
    wf.cached_data('projects', wrapper, max_age=10)    
    wf.send_feedback()
if __name__ == '__main__':
    wf = Workflow3()
    sys.exit(wf.run(main))