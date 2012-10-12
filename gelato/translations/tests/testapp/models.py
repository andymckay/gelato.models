from django.db import models

from gelato.translations.fields import TranslatedField, PurifiedField, LinkifiedField


class TranslatedModel(models.Model):
    name = TranslatedField()
    description = TranslatedField()
    default_locale = models.CharField(max_length=10)
    no_locale = TranslatedField(require_locale=False)


class UntranslatedModel(models.Model):
    """Make sure nothing is broken when a model doesn't have translations."""
    number = models.IntegerField()


class FancyModel(models.Model):
    """Mix it up with purified and linkified fields."""
    purified = PurifiedField()
    linkified = LinkifiedField()
