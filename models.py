#import datetime
from django.db                              import models
from django.utils                           import timezone
from django.contrib.auth.models             import User

class Person(models.Model):
  #user                    = models.OneToOneField('auth.User')
  username                = models.CharField(max_length=20,default='a')
  display_name            = models.CharField(max_length=30,default='a')
  email                   = models.EmailField(default='a@gmail.com')
  password                = models.CharField(max_length=30,default='a')
  authorname              = models.CharField(max_length=20,default='a')
  #user_author             = models.ForeignKey('auth.User', related_name='userauthor')
  status                  = models.IntegerField(default=0)
  date_joined             = models.DateField(default=timezone.now)
  landline                = models.CharField(max_length=13,blank=True,null=True)
  mobile                  = models.CharField(max_length=13,blank=True,null=True)
  postal_address          = models.CharField(max_length=200,blank=True,null=True)
  notes                   = models.TextField(blank=True,null=True)
  last_login              = models.DateTimeField(default=timezone.now)
  created_date            = models.DateTimeField(default=timezone.now)
  def __str__(self):
    return str(self.username)







