#!/usr/bin/python
# -*- coding: UTF-8 -*-
CONFIG_SERVERURL       = 'http://testrobot.nat123.net/clt'
CONFIG_HTTPTIMEOUT = 30
import os
import sys
import base64
import urllib, urllib2
import commands
try:
    import json
except ImportError:
    try:
        import simplejson as json
    except ImportError:
        print 'There is no json model'
import socket
socket.setdefaulttimeout(CONFIG_HTTPTIMEOUT)

reload(sys)
sys.setdefaultencoding("utf-8")
os.putenv('LANGUAGE', 'en_US:en')
#os.putenv('TERM', 'xterm')

def getExecResult(cmdStr):
    '''
    Execute command and return the output. if failed return ''
    Remember: It's better not use this for command which is using pipe and has too much output
    '''
    status, result  = commands.getstatusoutput(cmdStr)
    if not       0 == status:return ''
    return result

def getHTTPPost(targetUrl, postData):
    request = urllib2.Request(targetUrl, data=postData)
    r       = ''
    try:
        try:
            f   = urllib2.urlopen(request)
            r   = f.read()
        except Exception, e:
            pass
            print e
    finally:
        pass
    return r

def handleHTTPResult(result):
    pass
    print result


def doMainJob():
    sysInfo = SYSINFO.generateInfo()
    postData = {}
    postData['sysinfo'] = sysInfo
    result = getHTTPPost(CONFIG_SERVERURL,urllib2.urlencode(postData))
    print result


class SYSINFO:
    '''
    get system info executing shell scripts
    '''
    @staticmethod
    def generateInfo():
        info                        = {}
        info['hostname']            = SYSINFO.getHostName()
        info['issue']               = SYSINFO.getIssue()
        info['uname']               = SYSINFO.getUname()
        info['memory']              = SYSINFO.getMemory()
        info['memorytopn']          = SYSINFO.getMemoryTopN()
        info['cpu']                 = SYSINFO.getProcessor()
        info['cpuusage']            = SYSINFO.getCPUUsage()
        info['cputopn']             = SYSINFO.getCPUTopN()
        info['disk']                = SYSINFO.getDisk()
        info['uptime']              = SYSINFO.getUptime()
        info['processescount']      = SYSINFO.getProcessesCount()
        info['networkconnections']  = SYSINFO.getNetworkConnections()
        info['networklistening']    = SYSINFO.getNetworkListening()
        info['activemac']           = SYSINFO.getActiveMAC()
        info['unused']              = 'unused'
        infoJson                    = json.dumps(info)
        return infoJson

    @staticmethod
    def getHostName():
        '''
        return system hostname
        example: {"hostname": "joe-us"}
        '''
        hostname = getExecResult('hostname -s')
        return "{\"hostname\": \"%s\"}" % hostname

    @staticmethod
    def getIssue():
        '''
        return os info : Ubuntu 12.04.3 LTS
        example: {"issue": "Ubuntu 12.04.3 LTS"}
        '''
        issue = ''
        if os.path.exists('/etc/issue.net'):
            issue = getExecResult('cat /etc/issue.net | head -n 1').replace('\\n', '').replace('\\l', '').strip()
        elif os.path.exists('/etc/issue'):
            issue = getExecResult('cat /etc/issue     | head -n 1').replace('\\n', '').replace('\\l', '').strip()
        else:
            issue = getExecResult('uname -n')
        return '{\"issue\": \"%s\"}' % issue

    @staticmethod
    def getUname():
        '''
        return OS and hardware platform information
        example: {"kernel_release": "3.2.0-58-generic-pae", "processor_type": "i686", "kernel_version": "#88-Ubuntu SMP Tue Dec 3 18:00:02 UTC 2013", "machine_hardware_name": "i686", "operating_system": "GNU/Linux", "kernel_name": "Linux", "hardware_platform": "i386", "uname_all": "Linux joe-us 3.2.0-58-generic-pae #88-Ubuntu SMP Tue Dec 3 18:00:02 UTC 2013 i686 i686 i386 GNU/Linux", "network_node_hostname": "joe-us"}
        Usage: uname [OPTION]...
        Print certain system information.  With no OPTION, same as -s.

          -a, --all                print all information, in the following order,
                                     except omit -p and -i if unknown:
          -s, --kernel-name        print the kernel name
          -n, --nodename           print the network node hostname
          -r, --kernel-release     print the kernel release
          -v, --kernel-version     print the kernel version
          -m, --machine            print the machine hardware name
          -p, --processor          print the processor type or "unknown"
          -i, --hardware-platform  print the hardware platform or "unknown"
          -o, --operating-system   print the operating system
        --help     display this help and exit
        --version  output version information and exit

        '''
        uname                            = {}
        uname['kernel_name']             = getExecResult('uname -s')
        uname['kernel_release']          = getExecResult('uname -r')
        uname['kernel_version']          = getExecResult('uname -v')
        uname['machine_hardware_name']   = getExecResult('uname -m')
        uname['processor_type']          = getExecResult('uname -p')
        uname['hardware_platform']       = getExecResult('uname -i')
        uname['operating_system']        = getExecResult('uname -o')
        uname['network_node_hostname']   = getExecResult('uname -n')
        uname['uname_all']               = getExecResult('uname -a')

        #(kernel_name, kernel_release, kernel_version, machine_hardware_name, processor_type, hardware_platform, operating_system, network_node_hostname)
        return json.dumps(uname)

    @staticmethod
    def getMemory():
        '''
        return memory usage Info in kB
        example: {"Cached": "714236", "SwapCached": "0", "MemFree": "2456472", "MemTotal": "4001988", "Buffers": "74276"}
        :~$ cat /proc/meminfo|head -n 5|awk '{print $1, $2$3}'
        MemTotal: 4001988kB
        MemFree: 2467096kB
        Buffers: 72748kB
        Cached: 713640kB
        SwapCached: 0kB
        :~$ cat /proc/meminfo|head -n 7|awk '{print $2}'
        4001988
        2478476
        73496
        700740
        0
        '''
        cmdStr                  = "cat /proc/meminfo|head -n 5|awk '{print $2}'"
        memList                 = getExecResult(cmdStr).splitlines()
        if not    len(memList) == 5:return ''

        memDict                 = {}
        memDict['MemTotal']     = memList[0]
        memDict['MemFree']      = memList[1]
        memDict['Buffers']      = memList[2]
        memDict['Cached']       = memList[3]
        memDict['SwapCached']   = memList[4]
        return json.dumps(memDict)

    @staticmethod
    def getProcessor():
        return SYSINFO.getCPU()

    @staticmethod
    def getCPU():
        '''
        return processor information
        example:
        {"1": {"vendorid": "GenuineIntel", "modelname": "Intel(R) Core(TM) i5-2520M CPU @ 2.50GHz", "cpucores": "2", "cachesizeKB": "3072", "siblings": "4", "cpuMHZ": "2501.000"},}

        cat /proc/cpuinfo
        processor   : 0
        vendor_id   : GenuineIntel
        cpu family  : 6
        model       : 42
        model name  : Intel(R) Core(TM) i5-2520M CPU @ 2.50GHz
        stepping    : 7
        microcode   : 0x23
        cpu MHz     : 800.000
        cache size  : 3072 KB
        physical id : 0
        siblings    : 4
        core id     : 0
        cpu cores   : 2
        '''
        cpuCount         = getExecResult('cat /proc/cpuinfo | grep processor | wc -l')
        if '' == cpuCount or 0 == int(cpuCount) :return '{}'
        cpuCount         = int(cpuCount)
        vendorid_List    = getExecResult("cat /proc/cpuinfo | grep vendor_id    | awk        '{print $3}'").splitlines()
        modelname_List   = getExecResult("cat /proc/cpuinfo | grep 'model name' | awk -F': ' '{print $2}'").splitlines()
        cpuMHZ_List      = getExecResult("cat /proc/cpuinfo | grep MHz          | awk        '{print $4}'").splitlines()
        cachesizeKB_List = getExecResult("cat /proc/cpuinfo | grep 'cache size' | awk        '{print $4}'").splitlines()
        siblings_List    = getExecResult("cat /proc/cpuinfo | grep siblings     | awk        '{print $3}'").splitlines()
        cpucores_List    = getExecResult("cat /proc/cpuinfo | grep 'cpu cores'  | awk        '{print $4}'").splitlines()
        if not len(vendorid_List) == cpuCount or not len(modelname_List)   == cpuCount or \
           not len(cpuMHZ_List)   == cpuCount or not len(cachesizeKB_List) == cpuCount:return '{}'
        cpu = {}
        for i in range(cpuCount):
            dicTemp                 = {}
            dicTemp['vendorid']     = vendorid_List[i]
            dicTemp['modelname']    = modelname_List[i]
            dicTemp['cpuMHZ']       = cpuMHZ_List[i]
            dicTemp['cachesizeKB']  = cachesizeKB_List[i]
            if len(siblings_List)  == cpuCount:
                dicTemp['siblings'] = siblings_List[i]
            if len(cpucores_List)  == cpuCount:
                dicTemp['cpucores'] = cpucores_List[i]
            cpu['%d' % i]           = dicTemp
        return json.dumps(cpu)

    @staticmethod
    def getCPUUsage():
        '''
        return cpu usage by top -b -n 1
        example:{"ni": "0.1", "sy": "2.3", "wa": "1.0", "us": "4.3", "st": "0.0", "si": "0.0", "hi": "0.0", "id": "92.2"}
        top - 14:06:22 up  1:46,  2 users,  load average: 0.42, 0.39, 0.39
        Tasks: 192 total,   1 running, 190 sleeping,   0 stopped,   1 zombie
        Cpu(s):  4.1%us,  2.3%sy,  0.2%ni, 92.2%id,  1.3%wa,  0.0%hi,  0.0%si,  0.0%st
        Mem:   4001988k total,  2661932k used,  1340056k free,   366632k buffers
        Swap:  3999740k total,        0k used,  3999740k free,  1029448k cached

          PID USER      PR  NI  VIRT  RES  SHR S %CPU %MEM    TIME+  COMMAND
         1941 joe        9 -11  162m 8420 6880 S    4  0.2   3:02.54 pulseaudio

        2c. CPU States
        The CPU states are shown in the  Summary  Area.  They  are  always
        shown  as  a  percentage  and are for the time between now and the
        last refresh.

        us  --  User CPU time
          The time the CPU has spent running users'  processes  that  are
          not niced.

        sy  --  System CPU time
          The  time  the  CPU  has  spent running the kernel and its pro‐
          cesses.

        ni  --  Nice CPU time
          The time the CPU has spent running users'  proccess  that  have
          been niced.

        wa  --  iowait
          Amount of time the CPU has been waiting for I/O to complete.

        hi  --  Hardware IRQ
          The  amount  of time the CPU has been servicing hardware inter‐
          rupts.

        si  --  Software Interrupts
          The amount of time the CPU has been servicing  software  inter‐
          rupts.

        st  --  Steal Time
          The  amount  of  CPU  'stolen' from this virtual machine by the
          hypervisor for other tasks (such  as  running  another  virtual
          machine).
        '''
        cmdStr          = "top -b -n 1 |grep 'Cpu(s):'"
        cpuusageStr     = getExecResult(cmdStr)
        cpuusage        = {}
        cpuusage['us']  = cpuusageStr.split('%us')[0].split(':')[-1].strip()
        cpuusage['sy']  = cpuusageStr.split('%sy')[0].split(',')[-1].strip()
        cpuusage['ni']  = cpuusageStr.split('%ni')[0].split(',')[-1].strip()
        cpuusage['id']  = cpuusageStr.split('%id')[0].split(',')[-1].strip()
        cpuusage['wa']  = cpuusageStr.split('%wa')[0].split(',')[-1].strip()
        cpuusage['hi']  = cpuusageStr.split('%hi')[0].split(',')[-1].strip()
        cpuusage['si']  = cpuusageStr.split('%si')[0].split(',')[-1].strip()
        cpuusage['st']  = cpuusageStr.split('%st')[0].split(',')[-1].strip()

        return json.dumps(cpuusage)

    @staticmethod
    def getDisk():
        '''
        return disk usage infomation
        example:{"1": {"totalsize": "1993688", "mount": "/dev", "usedsize": "4", "unusedsize": "1993684", "usedrate": "1", "filesystem": "udev"}}


        joe@joe-us:~$ df -P | awk 'NR>0 {print $0}'
        Filesystem     1K-blocks    Used Available Use% Mounted on
        /dev/sda8       57988332 8109620  46933024  15% /
        udev             1993688       4   1993684   1% /dev
        tmpfs             800400     856    799544   1% /run
        none                5120       0      5120   0% /run/lock
        none             2000992    1716   1999276   1% /run/shm
        '''
        diskStr  = getExecResult("df -P | awk 'NR>1 {print $0}'")
        diskList = diskStr.splitlines()
        disk     = {}
        for i in range(len(diskList)):
            item                  = diskList[i]
            itemSplited           = item.split()
            dicTemp               = {}
            dicTemp['filesystem'] = itemSplited[0]
            dicTemp['totalsize']  = itemSplited[1]
            dicTemp['usedsize']   = itemSplited[2]
            dicTemp['unusedsize'] = itemSplited[3]
            dicTemp['usedrate']   = itemSplited[4][0:-1]
            dicTemp['mountname']  = itemSplited[5]
            disk['%d' % i]        = dicTemp
        return json.dumps(disk)

    @staticmethod
    def getUptime():
        '''
         uptime gives a one line display of the following information.  The cur‐
         rent time, how long the system has been running,  how  many  users  are
         currently  logged  on,  and the system load averages for the past 1, 5,
         and 15 minutes.
        '''
        uptime = getExecResult("cat /proc/uptime | awk '{print $1}' ")
        return '{\"uptime\": \"%s\"}' % uptime

    @staticmethod
    def getProcessesCount():
        '''
        return system current processes total number
        {"processesCount": "9"}
        '''
        processesCount = getExecResult("ps -ef| grep -v 'ps -ef' | wc -l")
        return '{\"processesCount\": \"%s\"}' % processesCount

    @staticmethod
    def getNetworkConnections():
        '''
        return getNetwork connection types and counts
        example:{"FIN_WAIT1": "11", "TIME_WAIT": "55", "LAST_ACK": "5", "CLOSE_WAIT": "1"}
        :~$ netstat -n | awk '/^tcp/ {++S[$NF]} END {for(a in S) print a, S[a]}'
        CLOSE_WAIT 1
        ESTABLISHED 18
        SYN_SENT 4
        '''
        cmdStr              = "netstat -n | awk '/^tcp/ {++S[$NF]} END {for(a in S) print a, S[a]}'"
        connectionStr       = getExecResult(cmdStr)
        connectionList      = connectionStr.splitlines()
        networkConnections  = {}
        for item in connectionList:
            (connectionType, connctionCount) = item.split()
            networkConnections["%s" % connectionType] = connctionCount
        return json.dumps(networkConnections)
    @staticmethod
    def getNetworkListening():
        '''
        return server ports listening status
        user privilege can only get limited information
        example:
        {"3": {"ip": "0.0.0.0", "pid": "-", "protocol": "tcp", "port": "22", "process": "-"}
         "2": {"ip": "127.0.0.1", "pid": "-", "protocol": "tcp", "port": "53", "process": "-"}
        netstat -tnpl | awk 'NR>2 {printf "%-6s %-30s %-30s\n",$1, $4,$7}'
        (Not all processes could be identified, non-owned process info
         will not be shown, you would have to be root to see it all.)
        tcp  127.0.0.1:53         -
        tcp  0.0.0.0:22           -
        tcp  127.0.0.1:631        -
        tcp  127.0.0.1:3306       -
        tcp6 :::22                -
        tcp6 ::1:631              -
        sudo netstat -tnpl | awk 'NR>2 {printf "%-6s %-30s %-30s\n",$1, $4,$7}'
        tcp    127.0.0.1:53                   1679/dnsmasq
        tcp    0.0.0.0:22                     807/sshd
        tcp    127.0.0.1:631                  884/cupsd
        tcp    127.0.0.1:3306                 1044/mysqld
        tcp6   :::22                          807/sshd
        tcp6   ::1:631                        884/cupsd
        '''
        cmdStr  = 'netstat -tnpl > /tmp/py.netstat.tmp'
        getExecResult(cmdStr)
        if not os.path.exists('/tmp/py.netstat.tmp'):return '{}'

        cmdStr  = "cat /tmp/py.netstat.tmp | awk 'NR>2 {printf \"%-6s %-30s %-30s\\n\",$1, $4,$7}'"
        cmdList =  getExecResult(cmdStr).splitlines()

        cmdDic  = {}
        for i in range(len(cmdList)):
            item                   = cmdList[i]
            if -1 == item.find(':'):continue
            itemSplited            = item.split()
            dicTemp                = {}
            dicTemp['protocol']    = itemSplited[0]
            dicTemp['port']        = itemSplited[1].split(':')[-1]
            dicTemp['ip']          = itemSplited[1].replace(':' + dicTemp['port'], '')
            dicTemp['pid']         = itemSplited[-1].split('/')[0]
            dicTemp['process']     = itemSplited[-1].split('/')[-1]
            cmdDic['%d' % i]       = dicTemp

        getExecResult('rm -rf /tmp/py.netstat.tmp')
        return json.dumps(cmdDic)

    @staticmethod
    def getMemoryTopN(top = 5):
        '''
        return top N processes which are using too much memory resource.
        Popen is used to prevent pipe error problems.
        example:
        {"0": {"pcpu": "2.1", "args": "/bin/bash", "pid": "3028", "rss": "147684", "vsize": "340904", "pmem": "3.6"},
         "1": {"pcpu": "1.1", "args": "/bin/bash", "pid": "3027", "rss": "111111", "vsize": "222222", "pmem": "1.6"}}
        $ ps -eo pid,rss,pmem,pcpu,vsize,args | awk 'NR>1 {print $0}' | sort -k 3 -r -n | head -n 10
        106188  2.6 2.2 271204 /usr/bin/python /usr/bin/software-center
        78324  1.9  1.9 255556 compiz
        51304  1.2  2.7 217720 sublime/sublime_text
        35508  0.8  0.1 111652 gedit
        33464  0.8  0.0 317520 /usr/sbin/mysqld
        26996  0.6  0.0 159228 nautilus -n
        26884  0.6  0.2 107104 /usr/lib/unity/unity-panel-service
        25296  0.6  0.0  76228 /usr/bin/python /usr/lib/ubuntuone-client/ubuntuone-syncdaemon
        22948  0.5  0.1 101220 /usr/bin/python /usr/share/ibus/ui/gtk/main.py
        19860  0.4  0.8 102412 gnome-terminal
        '''
        cmdStr          = "ps -eo pid,rss,pmem,pcpu,vsize,args | grep -v 'ps -eo pid,rss,pmem,pcpu,vsize,args' | grep -v 'NR>1 {print          $0}' | grep -v 'sort -k 3 -r -n' | awk 'NR>1 {print          $0}' | sort -k 3 -r -n > /tmp/py.memTopN.tmp"
        getExecResult(cmdStr)
        if not os.path.exists('/tmp/py.memTopN.tmp'):return '{}'

        cmdStr          = 'cat /tmp/py.memTopN.tmp |head -n 10 | cut -c1-160'
        memTopNList     = getExecResult(cmdStr).splitlines()

        memTopN         = {}
        for i in range(len(memTopNList)):
            item                          = memTopNList[i]
            itemSplit                     = item.split()
            dicTemp                       = {}
            (pid, rss, pmem, pcpu, vsize) = (itemSplit[0], itemSplit[1], itemSplit[2], itemSplit[3], itemSplit[4])
            args                          = item.split(' %s ' % vsize)[-1]
            dicTemp['pid']                = pid
            dicTemp['rss']                = rss
            dicTemp['pmem']               = pmem
            dicTemp['pcpu']               = pcpu
            dicTemp['vsize']              = vsize
            dicTemp['args']               = args
            memTopN["%d" % i]             = dicTemp

        getExecResult('rm -rf /tmp/py.memTopN.tmp')
        return json.dumps(memTopN)

    @staticmethod
    def getCPUTopN(top = 5):
        '''
        return top N processes which are using too much CPU resource.
        Popen is used to prevent pipe error problems.
        example:
        {"0": {"pcpu": "2.1", "args": "/bin/bash", "pid": "3028", "rss": "147684", "vsize": "340904", "pmem": "3.6"},
         "1": {"pcpu": "1.1", "args": "/bin/bash", "pid": "3027", "rss": "111111", "vsize": "222222", "pmem": "5.6"}}
        '''
        cmdStr          = "ps -eo pid,rss,pmem,pcpu,vsize,args | grep -v 'ps -eo pid,rss,pmem,pcpu,vsize,args' | grep -v 'NR>1 {print          $0}' | grep -v 'sort -k 4 -r -n' | awk 'NR>1 {print          $0}' | sort -k 4 -r -n > /tmp/py.CPUTopN.tmp"
        getExecResult(cmdStr)
        if not os.path.exists('/tmp/py.CPUTopN.tmp'):return '{}'

        cmdStr          = 'cat /tmp/py.CPUTopN.tmp | head -n 10 | cut -c1-160'
        cpuTopNList     = getExecResult(cmdStr).splitlines()

        cpuTopN         = {}
        for i in range(len(cpuTopNList)):
            item                          = cpuTopNList[i]
            itemSplit                     = item.split()
            dicTemp                       = {}
            (pid, rss, pmem, pcpu, vsize) = (itemSplit[0], itemSplit[1], itemSplit[2], itemSplit[3], itemSplit[4])
            args                          = item.split(' %s ' % vsize)[-1]
            dicTemp['pid']                = pid
            dicTemp['rss']                = rss
            dicTemp['pmem']               = pmem
            dicTemp['pcpu']               = pcpu
            dicTemp['vsize']              = vsize
            dicTemp['args']               = args
            cpuTopN["%d" % i]             = dicTemp

        getExecResult('rm -rf /tmp/py.CPUTopN.tmp')
        return json.dumps(cpuTopN)

    @staticmethod
    def getActiveMAC():
        '''
        return active interface mac address
        example: {"wlan0": "08:11:96:E2:AD:64", "eth0": "00:21:CC:B8:A7:3E"}
        ip -f inet -o link | sort |grep 'link/ether'  | grep -v 'DOWN'
        3: wlan0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc mq state UP qlen 1000\    link/ether 08:11:96:e2:ad:64 brd ff:ff:ff:ff:ff:ff
        '''
        cmdStr          = "ip -f inet -o link | sort | grep 'link/ether'  | grep -v 'DOWN'"
        activeMACList   = getExecResult(cmdStr).splitlines()
        activeMAC       = {}
        for item in activeMACList:
            dicTemp     = {}
            ethName     = item.split(': ')[1]
            ethMAC      = item.split('link/ether')[-1].split('brd')[0].strip().upper()
            activeMAC['%s' % ethName] = ethMAC
        return json.dumps(activeMAC)

if __name__ == '__main__':
    if os.name == 'nt' or not os.name == 'posix':
        print 'OS platform is not supported by this verison of script...'
        sys.exit()
    '''
    print SYSINFO.getMemory()
    print SYSINFO.getIssue()
    print SYSINFO.getHostName()
    print SYSINFO.getUname()
    print SYSINFO.getUptime()
    print SYSINFO.getNetworkConnections()
    print SYSINFO.getNetworkListening()
    print SYSINFO.getCPU()
    print SYSINFO.getDisk()
    print SYSINFO.getCPUUsage()
    print SYSINFO.getCPUTopN(10)
    print SYSINFO.getMemoryTopN(10)
    '''
    print SYSINFO.getActiveMAC()
    doMainJob()