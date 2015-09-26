from fabric.contrib.console import confirm
import requests, json, os
from fabric.api import *

env.use_ssh_config = True

SLACK_WEBHOOK = "https://hooks.slack.com/services/..."
SLACK_ROOM = "#edgecaselabs"

def production():
    env.hosts = ['ecl', 'ecl2',]

def deploy():
    run('whoami')

def clone():
    with cd('~/webapps/fabric_demo'):
        run('git clone https://github.com/edgecaselabs/fabric-demo.git myproject')

def checkout(branch=None):
    with cd('~/webapps/fabric_demo/myproject'):
        run('git checkout %s' % branch)

@parallel(pool_size=5)
def pull():
    with cd('~/webapps/fabric_demo/myproject'):
        run('git pull')
        #sudo('git pull', user='webapp')

@runs_once
def migrate():
    with cd('~/webapps/fabric_demo/myproject'):
        run('python3.4 manage.py migrate')


def start():
    run('~/webapps/fabric_demo/apache2/bin/start')

def stop():
    run('~/webapps/fabric_demo/apache2/bin/stop')

def restart():
    run('~/webapps/fabric_demo/apache2/bin/restart')

# def start(group='cmap:'):
#     run('supervisorctl start %s' % group)
#
# def stop(group='cmap:'):
#     run('supervisorctl stop %s' % group)
#
# def restart(group='cmap:'):
#     run('supervisorctl restart %s' % group)
#
# def update():
#     run('supervisorctl update')
#     run('nginx -s reload')

def static():
    with cd('~/webapps/fabric_demo/myproject'):
        run('python3.4 manage.py collectstatic --noinput')

def status():
    run('free -m')
    run('df -h')

    run('cd ~/webapps/fabric_demo/myproject && git log -1')

    run('ps -ef | grep apache2 | grep -v grep')


def scp(local, remote):
    put(local, remote)

def add_auth_key(file):
    scp(file, os.path.basename(file))
    run('cat %s >> .ssh/authorized_keys' % os.path.basename(file))


def getgit():
    git_rev = local('git rev-parse --short HEAD', capture=True)
    git_changelog = local('git log -1 %s' % git_rev, capture=True).replace("\n", "\\n")
    return git_rev, git_changelog

def notify_slack(message):
    global SLACK_WEBHOOK, SLACK_ROOM
    return requests.post(
        SLACK_WEBHOOK,
        data=json.dumps(
            {'channel': SLACK_ROOM, 'username': 'deployment squirrel', 'text': message, 'icon_emoji': ':squirrel:',
             "unfurl_links": True})).content


from fabric.contrib import django

django.project('webapp')
from widgets.models import Widget

def print_instances():
    for instance in Widget.objects.all():
        print(instance)










def reset():
    if confirm('Are you sure?'):
        with cd('~/webapps/fabric_demo'):
            run('./reset.sh')


from fabric.contrib.files import *