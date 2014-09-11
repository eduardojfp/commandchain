from django.shortcuts import render
from chain_of_command.models import Organization
from django.template import RequestContext, loader


def Organization_List(request):
    latest_org_list = Organization.objects.all()
    context = {'latest_org_list': latest_org_list}
    return render(request, 'Org_list.html', context)
    # Create your views here.