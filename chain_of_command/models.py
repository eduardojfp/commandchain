from django.db import models
from django.conf import settings
from ckeditor.fields import RichTextField
# Create your models here.
AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')


class Organization(models.Model):
    """
    The model for Organizations.
    """
    Name = models.CharField(max_length=80, unique=True)
    Description = RichTextField()
    objects = models.Manager()

    def __str__(self):
        return self.Name


class Member(models.Model):
    """
    A model for organization-dependant membership
    """
    Name = models.CharField(max_length=80)
    Organization = models.ForeignKey(Organization)
    User = models.ForeignKey(AUTH_USER_MODEL)
    Provisional = models.BooleanField(default=False)
    objects = models.Manager()

    def __str__(self):
        return self.Name


class Position(models.Model):
    """
    Organization-dependant Position model
    """
    Name = models.CharField(max_length=80)
    Organization = models.ForeignKey(Organization)
    CanGrantMembership = models.BooleanField(default=False)
    CanIssueOrders = models.BooleanField(default=False)
    CanEditOrganization = models.BooleanField(default=False)
    CanEditPrivileges = models.BooleanField(default=False)
    Percolates = models.BooleanField(default=False)
    associated = models.ManyToManyField(Member)
    boss = models.ForeignKey('Position', to_field='id', default=None, null=True,
                             blank=True)
    objects = models.Manager()

    def __str__(self):
        return self.Name


class Hierarchy(models.Model):
    """
    This is an obsolete thing which ought to make this worthwhile.
    """
    issuer = models.ForeignKey(Position, related_name="Fi")
    receiver = models.ForeignKey(Member)
    objects = models.Manager()


class Message(models.Model):
    """
    Interuser messaging for membership
    """
    Receiver = models.ForeignKey(AUTH_USER_MODEL)
    Issuer = models.ForeignKey(Member)
    Content = models.TextField()
    TS = models.TimeField(auto_now_add=True)
    IsRead = models.BooleanField(default=False)
    objects = models.Manager()


class Post(models.Model):
    """
    Woo, basic CMS system.
    """
    Title = models.TextField()
    Creator = models.ForeignKey(Member)
    timestamp = models.TimeField(auto_now=True)
    Content = RichTextField()
    Visible = models.BooleanField(default=True)
    objects = models.Manager()

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return self.Title


class Order(models.Model):
    """
    The model associated with orders.
    """
    objects = models.Manager()
    Issuer = models.ForeignKey(Member)
    P = models.ForeignKey(Position, default=0)
    Post = models.ForeignKey(Post)
    Deadline = models.DateTimeField(auto_now_add=True, null=True)
