from django.db import models
from django.conf import settings
# Create your models here.
AUTH_USER_MODEL=getattr(settings,'AUTH_USER_MODEL','auth.User')
class Organization(models.Model):
    Name = models.CharField(max_length=80)
    Description = models.TextField()
    def __str__(self):
        return self.Name

class Member(models.Model):
    Name = models.CharField(max_length=80)
    Organization = models.ForeignKey(Organization)
    User = models.ForeignKey(AUTH_USER_MODEL)
    def __str__(self):
        return self.Name

class Position(models.Model):
    Name = models.CharField(max_length=80)
    Organization=models.ForeignKey(Organization)
    CanGrantMembership = models.BooleanField(default=False)
    CanIssueOrders = models.BooleanField(default=False)
    CanEditOrganization = models.BooleanField(default=False)
    CanEditPrivileges = models.BooleanField(default=False)
    Percolates = models.BooleanField(default=False)
    associated=models.ManyToManyField(Member)
    def __str__(self):
        return self.Name

class Hierarchy(models.Model):
    issuer = models.ForeignKey(Position,related_name="Fi")
    receiver = models.ForeignKey(Member)


class Message(models.Model):
    Receiver = models.ForeignKey(AUTH_USER_MODEL)
    Issuer = models.ForeignKey(Member)
    Content = models.TextField()
    TS=models.TimeField(default='CURRENT_TIMESTAMP')
    IsRead=models.BooleanField(default=False)


class Post(models.Model):
    Title=models.TextField()
    Creator = models.ForeignKey(Member)
    timestamp = models.TimeField()
    Content = models.TextField()
    Visible = models.BooleanField(default=True)
    def __str__(self):
        return self.Title


class Order(models.Model):
    import datetime
    Issuer = models.ForeignKey(Member)
    Post = models.ForeignKey(Post)
    Deadline = models.DateTimeField(auto_now=True, null=True)

