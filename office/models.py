# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Ministry(models.Model):
	name = models.CharField(verbose_name="नाम", max_length=255)

	def __unicode__(self):
		return u'%s'%(self.name)

class Department(models.Model):
	ministry = models.ForeignKey(Ministry, verbose_name="मन्त्रालय", related_name="department", on_delete=models.CASCADE)
	name = models.CharField(verbose_name="नाम", max_length=255)

	def __unicode__(self):
		return u'%s'%(self.ministry) + " -- " + u'%s'%(self.name)

class District(models.Model):
	district = models.CharField(verbose_name="जिल्ला", max_length=255)
	
	def __unicode__(self):
		return u'%s'%(self.district)


class Office(models.Model):
	name = models.CharField(verbose_name="नाम", max_length=255)
	address = models.CharField(verbose_name="ठेगाना", max_length=255, blank=True)
	district = models.ManyToManyField(District, verbose_name="जिल्ला", related_name="office")
	email = models.CharField(verbose_name="इमेल", max_length=255, blank=True)
	phone = models.CharField(verbose_name="फोन", max_length=255, blank=True)
	fax = models.CharField(verbose_name="फ्याकस", max_length=255, blank=True)
	office_time = models.CharField(verbose_name="कार्यालय समय", max_length=255, blank=True)
	image = models.ImageField(verbose_name="तस्बिर", upload_to='ompimage', null=True, blank=True)
	department = models.ForeignKey(Department, verbose_name="बिभाग", on_delete=models.CASCADE)
	is_municipality = models.BooleanField(verbose_name="नगरपालिका", default=False)
	is_project = models.BooleanField(verbose_name="आयोजना", default=False)
	# office_setting = models.ForeignKey(OfficeSetting, related_name="office_setting", on_delete=models.CASCADE)
	def __unicode__(self):
		return u'%s'%(self.name)

	@property
	def detail(self):
		if self.is_municipality:
			return self.municipality_detail
		elif self.is_project:
			return self.project_detail
		return None


class ProjectDetail(models.Model):
	project_time = models.CharField(verbose_name="आयोजनाको समय", max_length=30)
	budget = models.CharField(verbose_name="बजेट", max_length=30)
	objective = models.TextField(verbose_name="उद्देस्य", blank=True)
	chief_eng = models.CharField(verbose_name="बरिस्ठ  इन्जिनीयर", max_length=30, blank=True)
	engineers = models.TextField(verbose_name=" इन्जिनीयरहरु", blank=True)
	office = models.OneToOneField(Office,verbose_name="कार्यालय", related_name="project_detail", on_delete=models.CASCADE)

	def __unicode__(self):
		return u'%s'%(self.office.name)


class MunicipalityDetail(models.Model):
	kendra = models.CharField(verbose_name="केन्द्र", max_length=30)
	area = models.CharField(verbose_name="एरिया", max_length=30)
	no_of_wards = models.TextField(verbose_name="वडाहरु को संख्या", blank=True)
	population = models.CharField(verbose_name="जनसंख्या", max_length=30, blank=True)
	activities = models.TextField(verbose_name="कृयाकलापहरु", blank=True)
	mayor_name = models.CharField(verbose_name="मयेर/अध्यक्षको नाम", max_length=30)
	mayor_phone_no = models.CharField(verbose_name="मयेर/अध्यक्षको फोन", max_length=30)
	mayor_address = models.CharField(verbose_name="मयेर/अध्यक्षको ठेगाना ", max_length=30, blank=True)
	sub_mayor_name = models.CharField(verbose_name="उप-मयेर/अध्यक्षको नाम", max_length=30)
	sub_mayor_phone_no = models.CharField(verbose_name="उप-मयेर/अध्यक्षको फोन", max_length=30)
	sub_mayor_address = models.CharField(verbose_name="उप-मयेर/अध्यक्षको ठेगाना ", max_length=30, blank=True)
	ward_chief_details = models.TextField(verbose_name="वडा प्रमुखको विवरण ", blank=True)
	office = models.OneToOneField(Office,verbose_name="कार्यालय", related_name="municipality_detail", on_delete=models.CASCADE)

	def __unicode__(self):
		return u'%s'%(self.office.name)

class OfficeSetting(models.Model):
	#fiscalyear = models.ForeignKey(FiscalYear, verbose_name="", max_length=90, on_delete=models.CASCADE)
	office = models.OneToOneField(Office, verbose_name="", on_delete=models.CASCADE)
	def __unicode__(self):
		return u'%s'%(self.office.id) + "--" + u'%s'%(self.fiscalyear)
