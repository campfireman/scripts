#! /usr/bin/env python3
import argparse
import json
import logging
import os
import pathlib
import shutil
import subprocess
import sys
import urllib

import requests

from utils import logger


class HttpApi:
    BASE_URL = ''
    AUTH_TOKEN_NAME = ''
    USERNAME = ''

    @property
    def _authorization_token(self) -> str:
        return os.environ[self.AUTH_TOKEN_NAME]

    @property
    def _authorization_header(self) -> dict:
        raise NotImplementedError

    def _build_path(self, path) -> str:
        return urllib.parse.urljoin(self.BASE_URL, path)

    def get(self, path: str, expected_code: int = 200, parameters=None) -> requests.Response:
        res = requests.get(self._build_path(path), parameters,
                           headers=self._authorization_header)
        if res.status_code != expected_code:
            logger.debug(res.text)
            raise Exception(f'Status code of GET not {expected_code}')
        return res

    def post(self, path: str, expected_code: int = 200, parameters=None) -> requests.Response:
        res = requests.post(self._build_path(
            path), json=parameters, headers=self._authorization_header)
        if res.status_code != expected_code:
            logger.debug(res.status_code)
            logger.debug(res.text)
            raise Exception(f'Status code of POST not {expected_code}')
        return res

    def delete(self, path: str, expected_code: int = 202) -> requests.Response:
        res = requests.delete(self._build_path(
            path), headers=self._authorization_header)
        if res.status_code != expected_code:
            logger.debug(res.text)
            raise Exception(f'Status code of POST not {expected_code}')
        return res


class GitlabApi(HttpApi):
    BASE_URL = 'https://gitlab.com/api/v4/'
    AUTH_TOKEN_NAME = 'GITLAB_API_TOKEN'
    USERNAME = 'CampFireMan'

    @property
    def _authorization_header(self) -> dict:
        return {'PRIVATE-TOKEN': f'{self._authorization_token}'}

    def projects(self) -> requests.Response:
        return self.get('projects')

    def repo_search(self, repo: str) -> requests.Response:
        query = {
            'search': repo,
            'simple': True,
        }
        return self.get(f'users/{self.USERNAME}/projects/', expected_code=200, parameters=query)

    def repo_exists(self, repo: str) -> bool:
        return len(self.repo_search(repo).json()) > 0

    def repo_create(self, repo_name: str, is_public: bool) -> requests.Response:
        visibility = 'public' if is_public else 'private'
        return self.post(f'projects', expected_code=201, parameters={
            'name': repo_name,
            'visibility': visibility,
        })

    def repo_delete(self, repo_name: str) -> requests.Response:
        path = urllib.parse.quote(f'{self.USERNAME}/{repo_name}', safe='')
        return self.delete(f'projects/{path}', expected_code=202)

    def repo_mirror(self, repo_id: int, mirror_url: str) -> requests.Response:
        return self.post(f'projects/{repo_id}/remote_mirrors', parameters={
            'url': mirror_url,
            'enabled': True,
        }, expected_code=201)


class GithubApi(HttpApi):
    BASE_URL = 'https://api.github.com/'
    AUTH_TOKEN_NAME = 'GITHUB_API_TOKEN'
    USERNAME = 'campfireman'

    @property
    def _authorization_header(self) -> dict:
        return {'Authorization': f'token {self._authorization_token}'}

    def repo_search(self, repo: str) -> requests.Response:
        query = {'q': f'user:{self.USERNAME} {repo} in:name'}
        return self.get('/search/repositories', expected_code=200, parameters=query)

    def repo_exists(self, repo: str) -> bool:
        return self.repo_search(repo).json()['total_count'] > 0

    def repo_create(self, repo_name: str, is_public: bool) -> requests.Response:
        return self.post('user/repos', expected_code=201, parameters={
            'name': repo_name,
            'private': not is_public,
        })

    def repo_delete(self, repo_name: str) -> requests.Response:
        return self.delete(f'/repos/{self.USERNAME}/{repo_name}', expected_code=204)


class GitInitializer:
    def __init__(self, repo_name: str, template: str, is_public: bool):
        self.repo_name = repo_name
        self.template = template
        self.is_public = is_public

        self.repo_path = os.path.join(os.getcwd(), self.repo_name)
        self.script_path = pathlib.Path(__file__).parent.resolve()

        self.gitlab_api = GitlabApi()
        self.github_api = GithubApi()

        self.local_repo_created = False
        self.gitlab_repo_created = False
        self.github_repo_created = False

    def cleanup(self):
        '''
        - todo: cleanup unfinished repo to run the script again more easily
        '''
        logger.info('Starting cleanup...')
        if self.local_repo_created:
            subprocess.call(["rm", "-rf", self.repo_path])
            logger.info('Deleted local folder')

        if self.gitlab_repo_created:
            self.gitlab_api.repo_delete(self.repo_name)
            logger.info('Deleted Gitlab repo')

        if self.github_repo_created:
            self.github_api.repo_delete(self.repo_name)
            logger.info('Deleted Github repo')

    def stop(self, msg):
        logger.error(msg)
        self.cleanup()
        sys.exit(1)

    def init_template(self):
        '''
        function expects the current working directory to be the repo path
        '''
        # expects the templates to sit in the script dir
        template_dir = os.path.join(self.script_path, 'assets', 'templates')
        with open(os.path.join(template_dir, f'{self.template}.json')) as template_file:
            template = json.loads(template_file.read())

        file_dir = os.path.join(template_dir, "files")
        if 'commands' in template:
            logger.info('Executing commands from template')
            for command in template['commands']:
                subprocess.call(command)

        if 'files' in template:
            logger.info('Creating files from template')
            for file in template["files"]:
                shutil.copy(os.path.join(file_dir, file["origin"]), os.path.join(
                    self.repo_path, file["path"]))

    def run(self):
        # check local repo name availability
        if os.path.exists(self.repo_path):
            raise Exception("Folder already exists!")

        # check remote
        gitlab_repo_exists = self.gitlab_api.repo_exists(self.repo_name)
        github_repo_exists = self.github_api.repo_exists(self.repo_name)
        if gitlab_repo_exists or github_repo_exists:
            output = 'Repo name is already taken on: '
            if github_repo_exists:
                output += '\n- Github'
            if gitlab_repo_exists:
                output += '\n- Gitlab'
            raise Exception(output)
        logger.info("Checked for name availability")

        # create local folder with git
        os.makedirs(self.repo_path)
        self.local_repo_created = True
        logger.info(f'Created folder {self.repo_name}')
        os.chdir(self.repo_path)
        subprocess.call(["git", "init"])
        logger.info("Initialized git repository")

        self.init_template()

        subprocess.call(["git", "add", "*"])
        subprocess.call(["git", "commit", "-m", "Init"])

        # create remote repositories
        gitlab_repo_res = self.gitlab_api.repo_create(
            self.repo_name, self.is_public).json()
        self.gitlab_repo_created = True
        logger.info('Created Gitlab repository')
        self.github_api.repo_create(self.repo_name, self.is_public)
        self.github_repo_created = True
        logger.info('Created Github repository')

        # set mirror
        self.gitlab_api.repo_mirror(
            gitlab_repo_res['id'], f'https://{self.github_api.USERNAME}:{self.github_api._authorization_token}@github.com/{self.github_api.USERNAME}/{self.repo_name}.git')
        logger.info('Created Gitlab mirror')

        # set origin and push
        gitlab_remote_url = f'git@gitlab.com:{self.gitlab_api.USERNAME}/{gitlab_repo_res["path"]}.git'
        subprocess.call(["git", "remote", "add", "origin", gitlab_remote_url])
        subprocess.call(["git", "push", "origin", "master"])
        logger.info('Setup remote for git')


def main():
    parser = argparse.ArgumentParser(
        description='Setup remote repositories automatically')
    parser.add_argument('name',
                        type=str,
                        help="Name of the repository to create")
    parser.add_argument('-t', '--template',
                        dest='template',
                        type=str,
                        default='default',
                        help="A template for the repository")
    parser.add_argument('-v', '--verbose',
                        dest='is_verbose',
                        type=bool,
                        default=True,
                        help="Toggle verbosity")
    parser.add_argument('-p', '--public',
                        dest='is_public',
                        type=bool,
                        default=False,
                        help="Toggle whether repository is public or not")
    args = parser.parse_args()
    if args.is_verbose:
        logging.basicConfig(level=logging.DEBUG)
        logger.setLevel(logging.DEBUG)
    initializer = GitInitializer(args.name, args.template, args.is_public)
    try:
        initializer.run()
    except Exception as e:
        initializer.stop(str(e))


if __name__ == '__main__':
    main()
