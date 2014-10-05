__author__ = 'awhite'

from chain_of_command.models import Organization, Member, Post
from django.contrib.auth.models import User


def get_viewable_posts(org_id, user_id=None):
    """
    Get all of the posts which  a user is able to view
    :rtype : list
    :param org_id: The id of the Organization
    :param user_id: The id of the User, or None, if the user is unregistered
    :return: A list of posts visible to the User
    """
    viewable = []
    org = Organization.objects.get(pk=org_id)
    member_in_org = False
    if user_id is not None:
        for j in User.objects.get(pk=user_id):
            for q in j.member_set.all():
                if q.Organization_id == org_id and not q.Provisional :
                    member_in_org = True
    for i in org.member_set.all():
        for post in i.post_set.all():
            if post.Visible or member_in_org:
                viewable.append(post)
    return viewable