from django.conf import settings

minimal = {
    'DATABASES': {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'mydatabase',
        }
    },
    'INSTALLED_APPS': [
        'gelato.addons',
        'gelato.applications',
        'gelato.versions',
        'gelato.translations',
    ],
}

if not settings.configured:
    settings.configure(**minimal)
    from django.test.utils import setup_test_environment
    from django.core import management
    management.call_command('syncdb', interactive=False)
    setup_test_environment()


from django import test

from gelato.constants.base import ADDON_EXTENSION
from gelato.addons.models import AddonBase
from gelato.applications.models import ApplicationBase, AppVersionBase
from gelato.versions.models import VersionBase, ApplicationsVersionBase

# These are the simplest test cases. Test that objects can be created.
class TestAddon(test.TestCase):

    def test_addon(self):
        addon = AddonBase.objects.create(type=ADDON_EXTENSION)
        assert addon.pk


class TestVersion(test.TestCase):

    def setUp(self):
        self.addon = AddonBase.objects.create(type=ADDON_EXTENSION)

    def test_version(self):
        version = VersionBase.objects.create(addon=self.addon)
        assert version.pk


class TestApplicationsVersions(test.TestCase):

    def setUp(self):
        self.addon = AddonBase.objects.create(type=ADDON_EXTENSION)
        self.version = VersionBase.objects.create(addon=self.addon)
        self.app = ApplicationBase.objects.create(guid='a.b.c')
        self.min = AppVersionBase.objects.create(application=self.app,
                                                 version='1.2')
        self.max = AppVersionBase.objects.create(application=self.app,
                                                 version='1.3')

    def test_applicationversion(self):
        appversion = (ApplicationsVersionBase.objects
                        .create(version=self.version, min=self.min,
                                max=self.max))
        assert appversion.pk
