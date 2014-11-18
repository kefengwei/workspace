__author__ = 'Administrator'
from django.db import models

SERVER_STATUS = (
    (0, u"Normal"),
    (1, u"Down"),
    (2, u"No Connect"),
    (3, u"Error"),
)


class Host(models.Model):
    name = models.CharField(max_length=64)
    public_ip = models.IPAddressField(blank=False)
    internal_ip = models.IPAddressField(blank=True, null=True)
    user = models.CharField(max_length=64)
    password = models.CharField(max_length=64)
    ssh_port = models.IntegerField(blank=True, null=True)
    status = models.SmallIntegerField(choices=SERVER_STATUS)
    model = models.CharField(max_length=64)
    cpu = models.CharField(max_length=64)
    core_num = models.SmallIntegerField(blank=True)
    hard_disk = models.CharField(max_length=200)
    memory = models.IntegerField()
    system = models.CharField(u'System OS', max_length=32, choices=[(i, i) for i in (u'CentOS', u'OPENSUSE',
                                                                                     u'Windows Server')])
    system_version = models.CharField(max_length=32)
    system_arch = models.CharField(max_length=32, choices=[(i, i) for i in (u'i386', u'x86_64')])
    create_time = models.DateField()
    asset_collect_time = models.DateField(auto_now=True)

    def __unicode__(self):
        return '%s:%s' % (self.name, self.public_ip)

    class Meta:
        verbose_name = u'Host'
        verbose_name_plural = verbose_name


class MaintainLog(models.Model):
    host = models.ForeignKey(Host)
    maintain_type = models.CharField(max_length=32)
    hard_type = models.CharField(max_length=16)
    time = models.DateTimeField()
    operator = models.CharField(max_length=16)
    note = models.TextField()

    def __unicode__(self):
        return '%s maintain-log [%s] %s %s' % (self.host.name, self.time.strftime('%Y-%m-%d %H:%M:%S'),
                                               self.maintain_type, self.hard_type)

    class Meta:
        verbose_name = u"Maintain Log"
        verbose_name_plural = verbose_name


class HostGroup(models.Model):

    name = models.CharField(max_length=32)
    description = models.TextField()
    hosts = models.ManyToManyField(Host, verbose_name=u'Hosts', blank=True, related_name='groups')

    class Meta:
        verbose_name = u"Host Group"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name


class LoadStatus(models.Model):
    host = models.ForeignKey(Host)
    load1 = models.CharField(max_length=16)
    load5 = models.CharField(max_length=16)
    load15 = models.CharField(max_length=16)
    update_time = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return "%s 's CpuStatus: Load1:%s,Load5:%s,Load15:%s,Update_Time:%s" % (self.host, self.load1, self.load5,
                                                                                self.load15, self.update_time)

    class Meta:
        verbose_name = u'CpuStatus'
        verbose_name_plural = verbose_name


class SystemInfo(models.Model):
    host = models.ForeignKey(Host)
    system_time = models.CharField(max_length=32)
    up_time = models.CharField(max_length=32)
    login_user = models.IntegerField()
    update_time = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return "%s 's Current System Info: System_Time:%s, UpTime:%s, LoginUser:%s, Update_Time:%s" % (self.host,
                                                                                                       self.system_time,
                                                                                                       self.up_time,
                                                                                                       self.login_user,
                                                                                                       self.update_time)

    class Meta:
        verbose_name = u'SystemInfo'
        verbose_name_plural = verbose_name


class MemoryStatus(models.Model):
    host = models.ForeignKey(Host)
    total_ram = models.IntegerField()
    used_ram = models.IntegerField()
    free_ram = models.IntegerField()
    total_swap = models.IntegerField()
    used_swap = models.IntegerField()
    update_time = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return "%s 's Current MemoryStatus: Total_RAM:%s, Used_RAM:%s, " \
               "Free_RAM:%s, Total_SWAP:%s,Used_SWAP:%s,Update_Time:%s" % (self.host, self.total_ram, self.used_ram,
                                                                           self.free_ram, self.total_ram,
                                                                           self.used_swap, self.update_time)

    class Meta:
        verbose_name = u'MemoryStatus'
        verbose_name_plural = verbose_name