#import datetime
from django.db                              import models
from django.utils                           import timezone
from django.contrib.auth.models             import User

class Person(models.Model):
  username                = models.CharField(max_length=20)
  display_name            = models.CharField(max_length=30)
  password                = models.CharField(max_length=30)
  fullmember              = models.BooleanField()
  status                  = models.IntegerField()
  authorname              = models.CharField(max_length=20,blank = True, null = True)
  detailcolor             = models.CharField(max_length=7)
  attendeescolor          = models.CharField(max_length=7)
  backgroundcolor         = models.CharField(max_length=7)
  last_login              = models.DateTimeField(blank = True, null = True)
  def __str__(self):
    return str(self.username)







