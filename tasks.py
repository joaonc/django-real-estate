import os
from pathlib import Path
from typing import List, Optional

from invoke import Collection, task

PROJECT_DIR = Path()
REQUIREMENTS_MAIN = 'main'
REQUIREMENTS_FILES = {
    REQUIREMENTS_MAIN: 'requirements',
    'dev': 'requirements-dev',
    'docs': 'requirements-docs',
}
"""
Requirements files.
Order matters as most operations with multiple files need ``requirements.txt`` to be processed
first.
"""

REQUIREMENTS_TASK_HELP = {
    'requirements': '`.in` file. Full name not required, just the initial name after the dash '
    f'(ex. \'dev\'). For main file use \'{REQUIREMENTS_MAIN}\'. Available requirements: '
    f'{", ".join(REQUIREMENTS_FILES)}.'
}

os.environ.setdefault('INVOKE_RUN_ECHO', '1')  # Show commands by default


def _csstr_to_list(csstr: str) -> List[str]:
    """
    Convert a comma-separated string to list.
    """
    return [s.strip() for s in csstr.split(',')]


def _get_requirements_file(requirements: str, extension: str) -> str:
    """
    Return the full requirements file name (with extension).

    :param requirements: The requirements file to retrieve. Can be the whole filename
        (no extension), ex `'dev-requirements'` or just the initial portion, ex `'dev'`.
        Use `'main'` for the `requirements` file.
    :param extension: Requirements file extension. Can be either `'in'` or `'txt'`.
    """
    filename = REQUIREMENTS_FILES.get(requirements, requirements)
    if filename not in REQUIREMENTS_FILES.values():
        raise FileNotFoundError(f'`{requirements}` is an unknown requirements file.')

    return f'{filename}.{extension.lstrip(".")}'


def _get_requirements_files(requirements: Optional[str], extension: str) -> List[str]:
    extension = extension.lstrip('.')
    if requirements is None:
        requirements_files = list(REQUIREMENTS_FILES)
    else:
        requirements_files = _csstr_to_list(requirements)

    # Get full filename+extension and sort by the order defined in `REQUIREMENTS_FILES`
    filenames = [
        _get_requirements_file(r, extension) for r in REQUIREMENTS_FILES if r in requirements_files
    ]

    return filenames


@task
def lint_black(c):
    c.run('black .')


@task
def lint_flake8(c):
    c.run('flake8 .')


@task
def lint_isort(c):
    c.run('isort .')


@task
def lint_mypy(c):
    c.run('mypy .')


@task
def lint_safety(c):
    c.run('safety check')


@task(lint_isort, lint_black, lint_flake8, lint_mypy, lint_safety)
def lint_all(c):
    """
    Run all linters.
    Config for each of the tools is in ``pyproject.toml`` and ``setup.cfg``.
    """
    print('Done')


@task
def serve(c):
    """
    Run API server locally.
    """
    c.run('uvicorn app.main:app --reload')


@task
def test(c):
    """
    Run unit tests.
    """
    c.run('python -m pytest .')


@task(help={'m': 'Message/description of migration.'})
def db_revision(c, m):
    """
    Create a DB revision for migration.
    """
    c.run(f'alembic revision --autogenerate -m "{m}"')


@task(help={'sql': "Don't emit SQL to database, dump to standard output/file instead."})
def db_upgrade(c, sql=False):
    """
    Upgrade DB to head, ie, run migration script.

    For downgrade or upgrading to a revision other than `head`, please refer to the Alembic
    documentation.
    """
    c.run('alembic upgrade head' + (' --sql' if sql else ''))


@task
def docs_serve(c):
    """
    Start documentation local server.
    """
    c.run('mkdocs serve')


@task
def docs_deploy(c):
    """
    Publish documentation to GitHub Pages at https://joaonc.github.io/maroon-back.
    """
    c.run('mkdocs gh-deploy')


@task(help=REQUIREMENTS_TASK_HELP)
def pip_compile(c, requirements=None):
    """
    Compile requirements file.
    """
    for filename in _get_requirements_files(requirements, 'in'):
        c.run(f'pip-compile {filename}')


@task(help=REQUIREMENTS_TASK_HELP)
def pip_sync(c, requirements=None):
    """
    Synchronize environment with requirements file.
    """
    c.run(f'pip-sync {" ".join(_get_requirements_files(requirements, "txt"))}')


@task(
    help={
        **REQUIREMENTS_TASK_HELP,
        **{'package': 'Package to upgrade. Can be a comma separated list.'},
    }
)
def pip_package(c, requirements, package):
    """
    Upgrade package.
    """
    packages = [p.strip() for p in package.split(',')]
    for filename in _get_requirements_files(requirements, 'in'):
        c.run(f'pip-compile --upgrade-package {" --upgrade-package ".join(packages)} {filename}')


@task(help=REQUIREMENTS_TASK_HELP)
def pip_upgrade(c, requirements):
    """
    Try to upgrade all dependencies to their latest versions.
    """
    for filename in _get_requirements_files(requirements, 'in'):
        c.run(f'pip-compile --upgrade {filename}')


@task
def precommit_install(c):
    """
    Install pre-commit into the git hooks, which will cause pre-commit to run on automatically.
    This should be the first thing to do after cloning this project and installing requirements.
    """
    c.run('pre-commit install')


@task
# `upgrade` instead of `update` to maintain similar naming to `pip-compile upgrade`
def precommit_upgrade(c):
    """
    Upgrade pre-commit config to the latest repos' versions.
    """
    c.run('pre-commit autoupdate')


@task(help={'hook': 'Name of hook to run. Default is to run all.'})
def precommit_run(c, hook=None):
    """
    Manually run pre-commit hooks.
    """
    hook = hook or '--all-files'
    c.run(f'pre-commit run {hook}')


ns = Collection()  # Main namespace
ns.add_task(serve)
ns.add_task(test)

db = Collection('db')
db.add_task(db_revision, 'revision')
db.add_task(db_upgrade, 'upgrade')

docs = Collection('docs')
docs.add_task(docs_serve, 'serve')
docs.add_task(docs_deploy, 'deploy')

lint = Collection('lint')
lint.add_task(lint_all, 'all')
lint.add_task(lint_black, 'black')
lint.add_task(lint_flake8, 'flake8')
lint.add_task(lint_isort, 'isort')
lint.add_task(lint_mypy, 'mypy')
lint.add_task(lint_safety, 'safety')

pip = Collection('pip')
pip.add_task(pip_compile, 'compile')
pip.add_task(pip_package, 'package')
pip.add_task(pip_sync, 'sync')
pip.add_task(pip_upgrade, 'upgrade')

precommit = Collection('precommit')
precommit.add_task(precommit_run, 'run')
precommit.add_task(precommit_install, 'install')
precommit.add_task(precommit_upgrade, 'upgrade')

ns.add_collection(db)
ns.add_collection(docs)
ns.add_collection(lint)
ns.add_collection(pip)
ns.add_collection(precommit)
