#import caching.base
#import waffle
from tower import ugettext_lazy as _

from django.db import models
from gelato.translations.fields import PurifiedField
from gelato.constants.applications import APP_IDS
from gelato.models.base import ModelBase


class VersionBase(ModelBase):

    addon = models.ForeignKey('addons.AddonBase', related_name='_versions')
    #license = models.ForeignKey('License', null=True)
    releasenotes = PurifiedField()
    approvalnotes = models.TextField(default='', null=True)
    version = models.CharField(max_length=255, default='0.1')
    version_int = models.BigIntegerField(null=True, editable=False)

    nomination = models.DateTimeField(null=True)
    reviewed = models.DateTimeField(null=True)

    has_info_request = models.BooleanField(default=False)
    has_editor_comment = models.BooleanField(default=False)

    class Meta(ModelBase.Meta):
        db_table = 'versions'
        ordering = ['-created', '-modified']
        app_label = 'versions'


class ApplicationsVersionBase(models.Model):

#    application = models.ForeignKey(Application)
    version = models.ForeignKey('versions.VersionBase', related_name='apps')
    min = models.ForeignKey('applications.AppVersionBase', db_column='min',
        related_name='min_set')
    max = models.ForeignKey('applications.AppVersionBase', db_column='max',
        related_name='max_set')

    #objects = caching.base.CachingManager()

    class Meta:
        db_table = u'applications_versions'
        #unique_together = (("application", "version"),)
        app_label = 'versions'

    def __unicode__(self):
        if (waffle.switch_is_active('d2c-buttons') and
            self.version.is_compatible[0] and
            self.version.is_compatible_app(APP_IDS[self.application.id])):
            return _(u'{app} {min} and later').format(app=self.application,
                                                      min=self.min)
        return u'%s %s - %s' % (self.application, self.min, self.max)
