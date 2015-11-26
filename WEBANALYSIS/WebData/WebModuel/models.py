# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin sqlcustom [app_label]'
# into your database.
from __future__ import unicode_literals

from django.db import models


class Codes(models.Model):
    code = models.CharField(primary_key=True, max_length=200)
    flag = models.CharField(max_length=5, blank=True, null=True)
    degree = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'codes'

class Links(models.Model):
    website = models.CharField(max_length=50)
    link = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'links'
        unique_together = (('website', 'link'),)


class Matchresult(models.Model):
    degree = models.CharField(max_length=1, blank=True, null=True)
    count = models.IntegerField(blank=True, null=True)
    website = models.CharField(max_length=50, blank=True, null=True)
    code = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'matchresult'
        unique_together = (('website', 'code'),)
