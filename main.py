import os
import csv
import json
import urllib2

from github import Github, UnknownObjectException  # needs PyGitHub

GITHUB_SECRET = os.environ['GHSECRET']
TARGET_REPO = os.getenv('TARGET_REPO')
DATA_PATH = os.environ['DATA_PATH']

def main():
    owner = get_repo_owner()
    data = get_testdata(owner)
    json_data = json.dumps(data)
    write_testdata(json_data)


def get_testdata(owner):
    response = urllib.request.urlopen(DATA_PATH)
    lines = [l.decode('utf-8') for l in response.readlines()]
    csv_reader_object = csv.DictReader(lines, delimiter=';')
    for row in csv_reader_object:
        if row['userid'] == owner:
            return row


def get_repo_owner():
    parts = TARGET_REPO.split('-')
    parts.pop(0)
    if parts[-1] == 'bzz':
        owner = parts[-2] + '-' + parts[-1]
    else:
        owner = parts[-1]
    print(f'Owner={owner}')
    return owner


def write_testdata(json_data):
    token = Github(GITHUB_SECRET)
    target_repo = token.get_repo(TARGET_REPO)
    try:
        existing_data = target_repo.get_contents('testdata2.json')
        target_repo.update_file(
            path='testdata.json',
            message='update tests',
            content=json_data,
            sha=existing_data.sha
        )
    except UnknownObjectException as e:
        target_repo.create_file(
            path='testdata.json',
            message='create tests',
            content=json_data
        )
    pass


if __name__ == '__main__':
    main()
