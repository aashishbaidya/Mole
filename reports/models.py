# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from office.models import Office


class FiscalYear(models.Model):
    date_range = models.CharField(max_length=255)

    def __unicode__(self):
        return u'%s' % (self.date_range)

class OfficeSetting(models.Model):
    fiscal_year = models.ForeignKey(FiscalYear, verbose_name="Arthik Barsa", blank=True, null=True, related_name="settings")
    office = models.OneToOneField(Office, verbose_name="",related_name="settings", on_delete=models.CASCADE)

AWADHI_CHOICES = (
        (0, 'बार्षिक'),
        (1, 'प्रथम'),
        (2, 'दितिय'),
        (3, 'तृतीय'),
    )


class KaryaKram(models.Model):
    karyakram = models.ForeignKey('self', verbose_name="कार्यक्रम", blank=True, null=True, related_name="parent", help_text="")
    name = models.CharField(max_length=255, verbose_name="कार्यक्रम",)
    office = models.ForeignKey(Office, verbose_name="कार्यालय", related_name="karyakram")
    code = models.CharField(verbose_name="कोड", max_length=15, null=True, blank=True, help_text="")
    unit = models.CharField(verbose_name="युनिट", max_length=15)
    kriyakalap = models.CharField(verbose_name="कृयाकलाप", max_length=15, null=True, blank=True, help_text="")

    @property
    def is_valid(self):
        return True if self.parent.all().count() else False

    def __unicode__(self):
		return u'%s'%(self.name)


class Lakxya(models.Model):
    karyakram = models.ForeignKey(KaryaKram, verbose_name=" कार्यक्रम", related_name="lakxya", help_text="")
    fiscal_year = models.ForeignKey(FiscalYear, verbose_name="आर्थिक-वर्ष", related_name="lakxya")
    paridam = models.FloatField(verbose_name="परिदम", default=0.00)
    var = models.FloatField(verbose_name="भार", default=0.00)
    budget = models.FloatField(verbose_name="बजेट", default=0.00)
    awadhi = models.IntegerField(verbose_name="अवधि", choices=AWADHI_CHOICES, default=0)


class Pragati(models.Model):
    karyakram = models.ForeignKey(KaryaKram, verbose_name="कार्यक्रम", related_name="pragati", help_text="")
    fiscal_year = models.ForeignKey(FiscalYear, verbose_name="आर्थिक-वर्ष", related_name="pragati")
    paridam = models.FloatField(verbose_name="परिदम", default=0.00)
    var = models.FloatField(verbose_name="भार", default=0.00)
    budget = models.FloatField(verbose_name="बजेट", default=0.00)
    awadhi = models.IntegerField(verbose_name="अवधि", choices=AWADHI_CHOICES, default=1)


class PragatiHistory(models.Model):
    paridam = models.FloatField(verbose_name="परिदम", default=0.00)
    var = models.FloatField(verbose_name="भार", default=0.00)
    budget = models.FloatField(verbose_name="बजेट", default=0.00)
    pragati = models.ForeignKey(Pragati, verbose_name="प्रगती", related_name="history")


class LakxyaHistory(models.Model):
    paridam = models.FloatField(verbose_name="परिदम", default=0.00)
    var = models.FloatField(verbose_name="भार", default=0.00)
    budget = models.FloatField(verbose_name="बजेट", default=0.00)
    lakxya = models.ForeignKey(Lakxya, verbose_name="लक्ष्य",  related_name="history")
