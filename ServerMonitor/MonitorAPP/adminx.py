__author__ = 'Administrator'
import xadmin
from xadmin import views
from models import *
from xadmin.layout import Main, TabHolder, Tab, Fieldset, Row, Col, AppendedText, Side
from xadmin.plugins.inline import Inline
from xadmin.plugins.batch import BatchChangeAction


class MainDashboard(object):
    widgets = [
        [{"type": "list", "model": "ServerMonitor.host", 'params': {'o': 'create_time'}},
            {"type": "html", "title": "Test Widget", "content": "<h3> Welcome to Xadmin! </h3><p>Join Online Group: <br/>QQ Qun : 282936295</p>"},
            {"type": "chart", "model": "app.accessrecord", 'chart': 'user_count', 'params': {'_p_date__gte': '2013-01-08', 'p': 1, '_p_date__lt': '2013-01-29'}},
            {"type": "list", "model": "app.host", 'params': {
                'o': '-guarantee_date'}},
        ],
        [
            {"type": "qbutton", "title": "Quick Start", "btns": [{'model': Host}, {'model': HostGroup}, {'title': "Google", 'url': "http://www.google.com"}]},
            {"type": "addform", "model": MaintainLog},
        ]
    ]
xadmin.site.register(views.IndexView, MainDashboard)


class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True
xadmin.site.register(views.BaseAdminView, BaseSetting)


class MaintainInline(object):
    model = MaintainLog
    extra = 1
    style = 'accordion'


class HostGroupAdmin(object):
    list_display = ('name', 'description')
    list_display_links = ('name',)

    search_fields = ['name']
    style_fields = {'hosts': 'checkbox-inline'}


xadmin.site.register(HostGroup, HostGroupAdmin)


class HostAdmin(object):
    list_display = ('name', 'public_ip', 'status', 'cpu', 'hard_disk', 'asset_collect_time')
    list_filter = ('name', 'public_ip')
    search_fields = ('host', 'public_ip', 'internal_ip', 'system')
    list_export = ('xls', 'xml', 'json')
    list_display_links = ('name', 'public_ip')

    reversion_enable = True

xadmin.site.register(Host, HostAdmin)


class MaintainLogAdmin(object):
    list_display = (
        'host', 'maintain_type', 'hard_type', 'time', 'operator', 'note')
    list_display_links = ('host',)

    list_filter = ['host', 'maintain_type', 'hard_type', 'time', 'operator']
    search_fields = ['note']

    form_layout = (
        Col("col2",
            Fieldset('Record data',
                     'time', 'note',
                     css_class='unsort short_label no_title'
                     ),
            span=9, horizontal=True
            ),
        Col("col1",
            Fieldset('Comm data',
                     'host', 'maintain_type'
                     ),
            Fieldset('Maintain details',
                     'hard_type', 'operator'
                     ),
            span=3
            )
    )
    reversion_enable = True

xadmin.site.register(MaintainLog, MaintainLogAdmin)