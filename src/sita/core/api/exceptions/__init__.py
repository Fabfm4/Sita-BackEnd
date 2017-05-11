# -*- coding: utf-8 -*-
from django.utils.translation import ugettext as _


class BaseAPIException(Exception):
    def __init__(self, configuration=None, hint=None):
        self.configuration = configuration
        self.hint = hint

    def __str__(self):
        return unicode(self).encode('utf-8')


class MissingConfiguration(BaseAPIException):
    def __unicode__(self):
        if self.configuration:
            base_message = '"{}" configuration is missing.'
            if self.hint:
                base_message += ' Hint: {}.'
                return _(base_message.format(self.configuration, self.hint))

            return _(base_message.format(self.configuration))
        else:
            _('Needed configuration is missing.')


class ImproperlyConfigured(BaseAPIException):
    def __unicode__(self):
        if self.configuration:
            base_message = '"{}" variable was improperly configured.'
            if self.hint:
                base_message += ' Hint: {}.'
                return _(base_message.format(self.configuration, self.hint))

            return _(base_message.format(self.configuration))
        else:
            _('A needed configuration was improperly configurated.')
