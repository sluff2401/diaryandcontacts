from django.db import models
from django.utils import timezone

class Circle(models.Model):
    full_name                            = models.CharField     (max_length=40)
    def __str__(self):
        return self.full_name

class Person(models.Model):
    full_name                            = models.CharField     (max_length=40)
    second_name                          = models.CharField     (max_length=20)
    name_in_meetup                       = models.CharField     (max_length=40, blank=True, null=True)
    name_in_twitter                      = models.CharField     (max_length=40, blank=True, null=True)
    email                                = models.CharField     (max_length=40, blank=True, null=True)
    phone_a                              = models.CharField     (max_length=15, blank=True, null=True)
    phone_b                              = models.CharField     (max_length=15, blank=True, null=True)
    phone_c                              = models.CharField     (max_length=15, blank=True, null=True)
    circles                              = models.ManyToManyField    ('Circle', blank=True, null=True)
    hcp                                  = models.BooleanField  (default=False)
    plus                                 = models.BooleanField  (default=False)
    esg                                  = models.BooleanField  (default=False)
    wltmf                                = models.BooleanField  (default=False)
    it                                   = models.BooleanField  (default=False)
    notes                                = models.TextField     (blank=True, null=True)
    created_date                         = models.DateTimeField (default=timezone.now)
    published_date                       = models.DateTimeField (blank=True, null=True)
    def publish(self):
        self.published_date = timezone.now()
        self.save()
    def __str__(self):
        return self.full_name

class Event(models.Model):
    event_date                           = models.DateField          (default=timezone.now)
    reference                            = models.CharField          (max_length=200, blank=True, default='')
    persons                              = models.ManyToManyField    ('Person', blank=True)
    #employers                            = models.ManyToManyField    ('Employer', blank=True)
    notes                                = models.TextField          (blank=True, null=True)
    created_date                         = models.DateTimeField      (default=timezone.now)
    published_date                       = models.DateTimeField      (blank=True, null=True)
    is_live                              = models.NullBooleanField       (default=True,null=True)
    def publish(self):
        self.published_date = timezone.now()
        self.save()
    def __str__(self):
        return self.reference
