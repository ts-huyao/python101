#!/usr/bin/env python  
""" 
@author:Hu Yao 
@license: Apache Licence 
@file: mover.py 
@time: 2019/06/11
@contact: hooyao@gmail.com
@site:  
@software: PyCharm 
"""

import logging
import os
from logging.handlers import WatchedFileHandler

from coloredlogs import ColoredFormatter
from github import Github, GithubException, UnknownObjectException
from github.GithubObject import NotSet
from urllib3 import Retry

from utils import TqdmHandler, GitHubRepo

ACCESS_TOKEN = 'token'
WORKING_DIR_TSCN = os.path.expanduser('~/GithubMover/TSCN')

SUC_TAG = 'migration-completed-2'
if not os.path.exists(WORKING_DIR_TSCN):
    os.makedirs(WORKING_DIR_TSCN)

LOGFORMAT = '%(name)s - %(levelname)s - %(message)s'
formatter = ColoredFormatter(LOGFORMAT)
stream = TqdmHandler()
stream.setLevel(logging.INFO)
stream.setFormatter(formatter)

file_handler = WatchedFileHandler(filename=os.path.join(WORKING_DIR_TSCN, 'mover.log'))
file_handler.setFormatter(formatter)

logging.basicConfig(level=logging.INFO,
                    format=LOGFORMAT,
                    handlers=[stream, file_handler])

LOGGER = logging.getLogger('GitHubRepo')

WEB_HOOKS = [
    ({'content_type': 'form',
      'insecure_ssl': '1',
      'url': 'https://ci.public-corp-lb.bwtsi.cn/github-webhook/'},
     ['issue_comment', 'pull_request', 'push']),
    ({'content_type': 'form',
      'insecure_ssl': '1',
      'url': 'https://ci.public-corp-lb.bwtsi.cn/ghprbhook/'},
     ['issue_comment', 'pull_request', 'push']),
    ({'url': 'https://tradeshift.atlassian.net/rest/bitbucket/1.0/repository/9999/sync',
      'insecure_ssl': '0',
      'content_type': 'form'},
     ['push']),
    ({'content_type': 'json',
      'url': 'https://tradeshift.atlassian.net/rest/bitbucket/1.0/repository/9999/sync',
      'insecure_ssl': '0'},
     ['issue_comment', 'pull_request', 'pull_request_review_comment', 'push'])

]

g = Github(ACCESS_TOKEN, retry=Retry(total=5, status_forcelist=[502]))

tscn = g.get_organization('TradeshiftCN')
bwts = g.get_organization('BaiwangTradeshift')
teams = list(bwts.get_teams())
ci_team = next(team for team in teams if team.name == 'ci')
devops_team = next(team for team in teams if team.name == 'cn-devops')
dev_team = next(team for team in teams if team.name == 'Developers')
mover_team = next(team for team in teams if team.name == 'MOVER')

for tscn_repo in tscn.get_repos():
    try:
        if tscn_repo.raw_data['disabled']:
            continue

        tscn_repo_short_name = tscn_repo.name
        tscn_repo_ssh_url = tscn_repo.ssh_url

#        if 'Backend-Common' != tscn_repo_short_name:
 #           continue

        if tscn_repo.fork:
            parent_full_name = tscn_repo.parent.full_name
            if 'Tradeshift/' not in parent_full_name:
                continue
            new_repo_on_bwts = bwts.create_fork(tscn_repo.parent)
            if new_repo_on_bwts.name != tscn_repo.name:
                new_repo_on_bwts.edit(name=tscn_repo.name)
                LOGGER.warning(f'BWTS repo "{new_repo_on_bwts.name}" is renamed to "{tscn_repo.name}" following TSCN')
        else:
            try:
                new_repo_on_bwts = bwts.get_repo(tscn_repo_short_name)
            except UnknownObjectException as ukoe:
                new_repo_on_bwts = bwts.create_repo(tscn_repo_short_name)

        # Check Migration is done
        bwts_repo_topics = new_repo_on_bwts.get_topics()
        if SUC_TAG in bwts_repo_topics:
            continue

        devops_team.set_repo_permission(new_repo_on_bwts, 'read')
        dev_team.set_repo_permission(new_repo_on_bwts, 'write')
        ci_team.set_repo_permission(new_repo_on_bwts, 'write')

        local_tscn_repo = GitHubRepo(work_dir=WORKING_DIR_TSCN,
                                     dir_name=tscn_repo_short_name,
                                     org_name='TradeshiftCN',
                                     repo_name=tscn_repo_short_name)
        local_tscn_repo.add_remote(remote_url=tscn_repo_ssh_url, remote_name='origin')
        local_tscn_repo.fetch('origin')

        local_tscn_repo.add_remote(remote_url=new_repo_on_bwts.ssh_url, remote_name='bwts')

        # Push branches
        #        for branch in local_tscn_repo.get_branches('origin'):
        #            local_tscn_repo.push_branch('origin', 'bwts', branch)

        for bwts_repo_branch in new_repo_on_bwts.get_branches():
            if bwts_repo_branch.protected:
                bwts_repo_branch.remove_protection()

        for branch in local_tscn_repo.get_branches('origin'):
            local_tscn_repo.push_branch('origin', 'bwts', branch)

        # local_tscn_repo.push_all_branches('bwts')
        local_tscn_repo.push_all_tags('bwts')

        # create web hook
        for config in WEB_HOOKS:
            try:
                new_repo_on_bwts.create_hook("web", config[0], config[1], active=True)
            except GithubException as ge:
                LOGGER.warning(ge.data)
            except Exception as e:
                LOGGER.error(e)

        # copy settings
        new_repo_on_bwts.edit(description=tscn_repo.description if tscn_repo.description else NotSet,
                              homepage=tscn_repo.homepage if tscn_repo.homepage else NotSet,
                              private=tscn_repo.private,
                              has_issues=tscn_repo.has_issues,
                              has_projects=tscn_repo.has_projects,
                              has_wiki=tscn_repo.has_wiki,
                              has_downloads=tscn_repo.has_downloads,
                              default_branch=tscn_repo.default_branch if tscn_repo.default_branch else NotSet,
                              allow_squash_merge=tscn_repo.allow_squash_merge,
                              allow_merge_commit=tscn_repo.allow_merge_commit,
                              allow_rebase_merge=tscn_repo.allow_rebase_merge,
                              archived=NotSet)

        # copy branch protection
        tscn_repo_branch_dict = {b.name: b for b in tscn_repo.get_branches()}

        for bwts_repo_branch in new_repo_on_bwts.get_branches():
            if bwts_repo_branch.name in tscn_repo_branch_dict:
                tscn_repo_branch = tscn_repo_branch_dict[bwts_repo_branch.name]
                if tscn_repo_branch.protected:
                    protection = tscn_repo_branch.get_protection()
                    user_push_restriction = protection.get_user_push_restrictions()
                    team_push_restriction = protection.get_team_push_restrictions()
                    required_status_checks = protection.required_status_checks
                    required_pull_request_reviews = protection.required_pull_request_reviews
                    bwts_repo_branch.edit_protection(
                        strict=required_status_checks.strict if required_status_checks and required_status_checks.strict else NotSet,
                        contexts=required_status_checks.contexts if required_status_checks and required_status_checks.contexts else NotSet,
                        enforce_admins=protection.enforce_admins,
                        dismissal_users=[user.login for user in
                                         required_pull_request_reviews.dismissal_users] if required_pull_request_reviews and required_pull_request_reviews.dismissal_users else NotSet,
                        dismissal_teams=[team.name for team in
                                         required_pull_request_reviews.dismissal_teams] if required_pull_request_reviews and required_pull_request_reviews.dismissal_teams else NotSet,
                        dismiss_stale_reviews=required_pull_request_reviews.dismiss_stale_reviews if required_pull_request_reviews and required_pull_request_reviews.dismiss_stale_reviews else NotSet,
                        require_code_owner_reviews=required_pull_request_reviews.require_code_owner_reviews if required_pull_request_reviews and required_pull_request_reviews.require_code_owner_reviews else NotSet,
                        required_approving_review_count=required_pull_request_reviews.required_approving_review_count if required_pull_request_reviews and required_pull_request_reviews.required_approving_review_count else NotSet,
                        user_push_restrictions=[user.login for user in
                                                user_push_restriction] if user_push_restriction else NotSet,
                        team_push_restrictions=[team.name for team in
                                                team_push_restriction] if team_push_restriction else NotSet)

        # Mark Migration is donw
        bwts_repo_topics = new_repo_on_bwts.get_topics()
        if SUC_TAG not in bwts_repo_topics:
            bwts_repo_topics.append(SUC_TAG)
        new_repo_on_bwts.replace_topics(bwts_repo_topics)

        LOGGER.info(f'Finished migrating {tscn_repo_short_name}')
    except Exception as e:
        LOGGER.error(f'Failed migrating {tscn_repo}')
        LOGGER.error(e)
