from django.shortcuts import render
from chain_of_command import models
from django.http import Http404
from django.contrib.auth.decorators import permission_required
from django.template import RequestContext, loader


def Organization_List(request):
    latest_org_list = models.Organization.objects.all()
    context = {'latest_org_list': latest_org_list}
    return render(request, 'Org_list.html', context)
    # Create your views here.


def OrganizationView(request, org_id):
    try:
        org = models.Organization.objects.get(pk=org_id)
        # print(dir(org.member_set.all()))
        mem = org.member_set.order_by('Name')
    except models.Organization.DoesNotExist:
        raise Http404
    return render(request, 'org_view.html', {'Org': org, 'mem': mem})


def position_display(request, org_id):
    print("hi there")
    UID = request.user.id
    mem = models.Member.objects.filter(User_id=UID, Organization_id=org_id)
    org = models.Organization.objects.get(pk=org_id)
    if len(mem) > 0:
        showing = models.Position.objects.filter(Organization_id=org_id)
        return render(request, 'position_view.html',
                      {'positions': showing, 'Organization_name': org.Name})
    else:
        return "<html><head></head><body>Silly boy, you can't read that.</body></html>"