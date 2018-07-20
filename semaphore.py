#!/usr/bin/python
# encoding: utf-8

import sys
import os
import re
import json

from workflow import Workflow3, ICON_WEB, ICON_WARNING, web, Variables, PasswordNotFound
from workflow.background import run_in_background, is_running

ICON_SEMAPHORE = '%s/semaphore.png' %(os.path.dirname(os.path.abspath(__file__))) 

def main(wf):
    args = wf.args

    auth_token = None
    try:
        auth_token = wf.get_password('semaphoreci-auth-token')
    except PasswordNotFound:  # API key has not yet been set
        wf.add_item('No API key set.',
                     'Please use ci-auth to set your SemaphoreCI auth key.',
                     arg='https://semaphoreci.com/users/edit',
                     valid=False,
                     icon=ICON_WARNING)
        wf.send_feedback()
        return 0
    query = None

    if not wf.cached_data_fresh('projects', 10):
        run_in_background('update',['/usr/bin/python', wf.workflowfile('update_projects.py')])
    projects = sorted(wf.cached_data('projects', max_age=0), key=lambda project: project['updated_at'], reverse=True)
    
    if projects:
        if (len(args) == 0):        
            for project in projects:
                arg = project['name']
                item = wf.add_item(project['name'], '', arg=arg, valid=True, icon=ICON_SEMAPHORE)
                item.setvar('html_url', project['html_url'])
        else:
            query = args[0]
            project = next( (p for p in projects if p['name'] == query), None)
            if project is not None:            
                branches = sorted(project['branches'], key=lambda branch: branch['started_at'], reverse=True)[:3]
                for branch in branches:
                    subtitle = '%s by %s' %(branch['commit']['message'], branch['commit']['author_name'])
                    icon = '%s/%s.png' %(os.path.dirname(os.path.abspath(__file__)),branch['result'])
                    wf.add_item(branch['branch_name'], subtitle, arg=branch['build_url'], 
                                valid=True, icon=icon)            
              
                servers = project['servers']
                for server in filter(None, servers):
                    subtitle = '%s by %s' %(server['commit']['message'], server['commit']['author_name'])
                    icon = '%s/server_%s.png' %(os.path.dirname(os.path.abspath(__file__)),branch['result'])
                    wf.add_item(server['server_name'], subtitle, arg=server['server_html_url'], 
                                valid=True, icon=icon)            
                if len(branches) > 0:            
                    github_url = branches[0]['commit']['url']
                    if 'github.com' in github_url:
                        pr_url = re.sub(r'/commit/.*','/pulls', github_url)
                        wf.add_item('Open GitHub Pull Requests', pr_url, arg=pr_url, 
                                    valid=True, icon=ICON_WEB)     
                wf.add_item('Open on SemaphoreCI', project['html_url'], arg=project['html_url'], 
                                            valid=True, icon=ICON_WEB)
    
    wf.send_feedback()


if __name__ == '__main__':
    wf = Workflow3()
    sys.exit(wf.run(main))