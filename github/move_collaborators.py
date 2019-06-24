#!/usr/bin/env python  
""" 
@author:Hu Yao 
@license: Apache Licence 
@file: move_collaborators.py 
@time: 2019/06/23
@contact: hooyao@gmail.com
@site:  
@software: PyCharm 
"""

import logging

from github import Github, UnknownObjectException
from urllib3 import Retry

import config

LOGGER = logging.getLogger('move_collaborators')

g = Github(config.ACCESS_TOKEN, retry=Retry(total=5, status_forcelist=[502]))

tscn = g.get_organization('TradeshiftCN')
bwts = g.get_organization('BaiwangTradeshift')
teams = list(bwts.get_teams())
dev_team = next(team for team in teams if team.name == 'Developers')
dev_mem_logins = [mem.login for mem in dev_team.get_members()]

for tscn_repo in tscn.get_repos():
    try:
        if tscn_repo.raw_data['disabled']:
            continue

        tscn_repo_short_name = tscn_repo.name
        tscn_repo_ssh_url = tscn_repo.ssh_url

        tscn_repo_collabs = tscn_repo.get_collaborators('direct')
        if tscn_repo_collabs.totalCount > 0:
            try:
                bwts_repo = bwts.get_repo(tscn_repo_short_name)
                for collab in tscn_repo_collabs:
                    if collab.login in dev_mem_logins:
                        permission = tscn_repo.get_collaborator_permission(collab)
                        bwts_repo.add_to_collaborators(collab, permission=permission)
                LOGGER.info(f'Finished moving collaborator {tscn_repo_short_name}')
            except UnknownObjectException as ukoe:
                # don't care
                pass

    except Exception as e:
        LOGGER.error(f'Failed migrating {tscn_repo}')
        LOGGER.error(e)
