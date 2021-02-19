from django.utils.translation import ugettext_lazy as _
from jet.dashboard import modules
from jet.dashboard.dashboard import Dashboard, AppIndexDashboard
from nucleo.models import *


class CustomIndexDashboard(Dashboard):
    columns = 3

    def init_with_context(self, context):
        self.children.append(modules.ModelList(
            _('Models'),
            exclude=('auth.*',),
            column=0,
            order=0
        ))