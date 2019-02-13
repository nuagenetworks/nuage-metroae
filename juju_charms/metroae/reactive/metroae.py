from charms.reactive import when, when_not, set_flag
import subprocess
import os


CHARM_DIR = os.environ['CHARM_DIR']
METRO_DIRECTORY = os.path.join(CHARM_DIR, 'nuage-metro')


@when_not('metroae.installed')
def install_metroae():
    run_shell("virtualenv -p python2.7 .metroaenv")
    run_shell("source .metroaenv/bin/activate && ./metro-setup.sh")
    set_flag("metroae.installed")


@when_not('vsc.installed')
@when('metroae.installed')
def install_vsc():
    run_shell("source .metroaenv/bin/activate && ./metroae -vvv")
    set_flag("vsc.installed")


def run_shell(cmd):
    ret = subprocess.Popen(cmd,
                           shell=True,
                           executable='/bin/bash',
                           cwd=METRO_DIRECTORY)
    retcode = ret.wait()
    if retcode != 0:
        raise Exception("Non-zero %d return code from %s" % (retcode, cmd))
