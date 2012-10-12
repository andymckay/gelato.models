from django.db import models

from gelato.constants.applications import APPS_ALL
from gelato.constants.compare import version_dict, version_int
from gelato.models.base import ModelBase


class ApplicationBase(ModelBase):

    guid = models.CharField(max_length=255, default='')
    supported = models.BooleanField(default=1)
    # We never reference these translated fields, so stop loading them.
    # name = TranslatedField()
    # shortname = TranslatedField()

    class Meta:
        db_table = 'applications'
        app_label = 'applications'

#    def __unicode__(self):
#        return unicode(APPS_ALL[self.id].pretty)


class AppVersionBase(ModelBase):

    application = models.ForeignKey('applications.ApplicationBase')
    version = models.CharField(max_length=255, default='')
    version_int = models.BigIntegerField(editable=False)

    class Meta:
        db_table = 'appversions'
        ordering = ['-version_int']
        app_label = 'applications'

    def save(self, *args, **kw):
        if not self.version_int:
            self.version_int = version_int(self.version)
        return super(AppVersionBase, self).save(*args, **kw)

    def __init__(self, *args, **kwargs):
        super(AppVersionBase, self).__init__(*args, **kwargs)
        # Add all the major, minor, ..., version attributes to the object.
        self.__dict__.update(version_dict(self.version or ''))

    def __unicode__(self):
        return self.version

#    def flush_urls(self):
#        return ['*/pages/appversions/*']
