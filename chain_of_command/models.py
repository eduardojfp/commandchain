from django.db import models

# Create your models here.

class User(models.Model):
    Username = models.CharField(max_length=45)
    Password = models.CharField(max_length=45)
    Email = models.CharField(max_length=200)


class Organization(models.Model):
    Name = models.CharField(max_length=80)
    Description = models.TextField()


class Member(models.Model):
    Name = models.CharField(max_length=80)
    Organization = models.ForeignKey(Organization)
    User = models.ForeignKey(User)
