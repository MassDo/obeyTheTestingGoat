import random, string   
from fabric.contrib.files import append, exists
from fabric.api import cd, env, local, run 

REPO_URL = 'https://github.com/MassDo/obeyTheTestingGoat.git'

def deploy():
    site_folder = f'/home/{env.user}/sites/{env.host}'
    run(f'mkdir -p {site_folder}')
    with cd(site_folder):
        _get_latest_source()
        _update_virtualenv()
        _create_or_update_dotenv()
        _update_static_files()
        _update_database()

def _get_latest_source():
    if exists('.git'):
        run('git fetch')
    else:
        run(f'git clone {REPO_URL} .')
    # get the hash of the last local commit
    current_commit = local('git log -n 1 --format=%H', capture=True)
    # blow any changes in the server's code directory 
    # And pull the current_commit
    run(f'git reset --hard {current_commit}')

def _update_virtualenv():
    if not exists(Pipfile):
        # if no Pipfile install pipenv and add to PATH
        run('pip install pipenv && \
            PYTHON_BIN_PATH="$(python3 -m site --user-base)/bin" && \
            PATH="$PATH:$PYTHON_BIN_PATH"')
    run('pipenv install -r requirement')  

def _create_or_update_dotenv():
    append('.env', 'DJANGO_DEBUG_FALSE=y')
    append('.env', f'SITENAME={env.host}')
    current_contents = run('cat .env')
    if DJANGO_SECRET_KEY not in current_contents:
        pool = string.ascii_letters + string.punctuation + string.digits
        new_secret_key = ''.join(random.SystemRandom().choices(pool, k=50))
        append('.env', f'DJANGO_SECRET_KEY={new_secret_key}')

def _update_static_files():
    run('pipenv run ./manage.py collectstatic --noinput')

def _update_database():
    run('pipenv run ./manage.py migrate --noinput')