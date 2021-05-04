import secrets
from string import ascii_letters

from fabric.contrib.files import append, exists
from fabric.api import cd, env, local, run

REPO_URL = 'https://github.com/wpbindt/tdd-book-percival.git'
SITE_URL = 'www.tdd-book.nl'

def deploy():
    site_folder = f'/home/{env.user}/sites/{SITE_URL}'
    run(f'mkdir -p {site_folder}/src')
    with cd(site_folder): 
        run(f'mkdir -p database static')
        _create_or_update_dotenv()
    with cd(site_folder + '/src'):
        _get_latest_source()
        _update_virtualenv()
        _update_static_files()
        _update_database()


def _get_latest_source():
    if exists('.git'):
        run('git fetch')
    else:
        run(f'git clone {REPO_URL} .')
    current_commit = local('git log -n 1 --format=%H', capture=True)
    run(f'git reset --hard {current_commit}')


def _update_virtualenv():
    if not exists('virtualenv/bin/pip'):
        run(f'python3 -m venv virtualenv')
    run('./virtualenv/bin/pip install -r requirements.txt')


def _create_or_update_dotenv():
    append('.env', 'DJANGO_DEBUG_FALSE=y')
    current_contents = run('cat .env')
    if 'DJANGO_SECRET_KEY' not in current_contents:
        new_secret = ''.join(secrets.choice(ascii_letters) for _ in range(50))
        append('.env', f'DJANGO_SECRET_KEY={new_secret}')


def _update_static_files():
    run('./virtualenv/bin/python manage.py collectstatic --noinput')


def _update_database():
    run('./virtualenv/bin/python manage.py migrate --noinput')

