from django.shortcuts import render
from chain_of_command import models
from django.http import Http404
from django.template import RequestContext, loader


def Organization_List(request):
    latest_org_list = models.Organization.objects.all()
    context = {'latest_org_list': latest_org_list}
    return render(request, 'Org_list.html', context)
    # Create your views here.

def OrganizationView(request,org_id):
    try:
        org=models.Organization.objects.get(pk=org_id)
        #print(dir(org.member_set.all()))
        mem=org.member_set.order_by('Name')
    except models.Organization.DoesNotExist:
        raise Http404
    return render(request,'org_view.html',{'Org':org,'mem':mem})