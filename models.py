#import datetime
from django.db                              import models
#from django.utils                           import timezone
from django.contrib.auth.models             import User
from django.utils                           import timezone
#from django.contrib.auth.models             import User

class Person(models.Model):
  username                = models.CharField(max_length=20)
  display_name            = models.CharField(max_length=30)
  meetup_name                       = models.CharField     (max_length=40, blank=True, null=True)
  twitter_name                      = models.CharField     (max_length=40, blank=True, null=True)
  email                                = models.CharField     (max_length=40, blank=True, null=True)
  phone_a                              = models.CharField     (max_length=15, blank=True, null=True)
  phone_b                              = models.CharField     (max_length=15, blank=True, null=True)
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
  notes                                = models.TextField     (blank=True, null=True)
  last_login              = models.DateTimeField(blank = True, null = True)
  created_date                         = models.DateTimeField (default=timezone.now)
  published_date                       = models.DateTimeField (blank=True, null=True)
  def publish(self):
    self.published_date = timezone.now()
    self.save()
  #def display_name(self):
    #return self.display_name
  def __str__(self):
    return str(self.username)





<<<<<<< HEAD
=======




>>>>>>> ef65b362f63604a6466aec9e6b8915e7dc318826
