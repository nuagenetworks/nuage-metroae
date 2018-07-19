import subprocess

from pyVim import connect

proc = subprocess.Popen(["sudo dmidecode|grep UUID|awk '{print $2}'"], 
                        stdout=subprocess.PIPE,
                        shell=True)
out, err proc.communicate()
uuid = out[:-1]

SI = None
SI = connect.SmartConnect(host=ARGS.host,
                          user=ARGS.user,
                          pwd=ARGS.password,
                          port=ARGS.port)
vm = SI.content.searchIndex.FindbyUuid(None,
                                       uuid,
                                       True,
                                       False)
host = vm.runtime.host 

print "Host name: {}".format(host.name)