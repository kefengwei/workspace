from remote_run import Batch
from ServerMonitor.models import *

def collect_info(host):
    batch = Batch(host)
    result = batch.run('statgrab -M')
    result_dict = {}
    for line in result.strip().split('\n'):
        line = line.split('=')
        result_dict[line[0].strip()] = line[1].strip()
    return result_dict


def search(result_dict, item):
    info = {}
    for k, v in result_dict.items():
        if item+'.' in k:
            info[k[len(item)+1:]] = v
    return info

    
if __name__ == '__main__':
    host = Host.objects.all()
    host_list = []
    for i in host:
        host_list.append(i.public_ip)

    for h in host_list:
        result_dict = collect_info(h)
        loadinfo = search(result_dict, 'load')
        cpuinfo = search(result_dict, 'cpu')
        systeminfo = search(result_dict, 'general')
        memoryinfo = search(result_dict, 'mem')
        diskinfo = search(result_dict, 'disk')
        netinfo = search(result_dict,'net')