from django.db import models

# Create your models here.

class User(models.Model):
    Username = models.CharField(max_length=45)
    Password = models.CharField(max_length=45)
    Email = models.CharField(max_length=200)
    def __str__(self):
        return self.Username


class Organization(models.Model):
    Name = models.CharField(max_length=80)
    Description = models.TextField()
    def __str__(self):
        return self.Name

class Member(models.Model):
    Name = models.CharField(max_length=80)
    Organization = models.ForeignKey(Organization)
    User = models.ForeignKey(User)
    def __str__(self):
        return self.Name

class Position(models.Model):
    Name = models.CharField(max_length=80)
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
    Receiver = models.ForeignKey(User)
    Issuer = models.ForeignKey(Member)
    Content = models.TextField()
    TS=models.TimeField(default='CURRENT_TIMESTAMP')


class Post(models.Model):
    Title=models.TextField()
    Creator = models.ForeignKey(Member)
    timestamp = models.TimeField()
    Content = models.TextField()
    Visible = models.BooleanField(default=True)
    def __str__(self):
        return self.Title


class Order(models.Model):
    Issuer = models.ForeignKey(Member)
    Post = models.ForeignKey(Post)

