#import datetime
from django.db                              import models
#from django.utils                           import timezone
from django.contrib.auth.models             import User

class Person(models.Model):
  username                = models.CharField(max_length=20)
  display_name            = models.CharField(max_length=30)
  password                = models.CharField(max_length=30)
  fullmember              = models.BooleanField()
  status                  = models.IntegerField()
  authorname              = models.CharField(max_length=20,blank = True, null = True)
  reversevideo            = models.BooleanField(default=False)
  datecolor               = models.CharField(max_length=20, default='black')
  detailcolor             = models.CharField(max_length=20, default='#0000C0')
  attendeescolor          = models.CharField(max_length=20, default='#00C000')
  backgroundcolor         = models.CharField(max_length=20, default='#F3FFF3')
  datecolor_rev           = models.CharField(max_length=20, default='white')
  detailcolor_rev         = models.CharField(max_length=20, default='aqua')
  attendeescolor_rev      = models.CharField(max_length=20, default='lawngreen')
  backgroundcolor_rev     = models.CharField(max_length=20, default='black')
  last_login              = models.DateTimeField(blank = True, null = True)
  def __str__(self):
    return str(self.username)





