import re

import semver
from invoke import run
from twine.commands import upload as twine_upload

from semantic_release.settings import load_config


def get_current_version():
    return run('python setup.py --version', hide=True).stdout.strip()


def upload_to_pypi(dists='bdist_wheel'):
    run('python setup.py {}'.format(dists))
    twine_upload.upload(dists=['dist/*'], repository='pypi', sign=False, identity=None,
                        username=None, password=None, comment=None, sign_with='gpg')
    run('rm -rf build dist')


def get_new_version(current_version, level_bump):
    if not level_bump:
        return current_version
    return getattr(semver, 'bump_{0}'.format(level_bump))(current_version)


def set_new_version(new_version):
    filename, variable = load_config().get('version_variable').split(':')
    variable = variable.strip()
    with open(filename, mode='r') as fr:
        content = fr.read()

    content = re.sub(
        r'{} ?= ?["\']\d+\.\d+(?:\.\d+)?["\']'.format(variable),
        '{} = \'{}\''.format(variable, new_version),
        content
    )

    with open(filename, mode='w') as fw:
        fw.write(content)
    return True
