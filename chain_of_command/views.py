from django.shortcuts import render
from chain_of_command import models, forms
from django.http import Http404

from django.template import RequestContext, loader


def Organization_List(request):
    U = request.user
    UID = U.id
    if U.is_authenticated():
        lgnabl = True
    else:
        lgnabl = None
    latest_org_list = models.Organization.objects.all()
    context = {'latest_org_list': latest_org_list,
               "loginable": lgnabl}
    return render(request, 'Org_list.html', context)
    # Create your views here.


def OrganizationView(request, org_id):
    U = request.user
    UID = U.id
    if U.is_authenticated():
        lgnabl = True
    else:
        lgnabl = None
    try:
        org = models.Organization.objects.get(pk=org_id)
        # print(dir(org.member_set.all()))
        mem = org.member_set.order_by('Name')
    except models.Organization.DoesNotExist:
        raise Http404
    return render(request, 'org_view.html',
                  {'Org': org, 'mem': mem,
                   "loginable": lgnabl})


def position_display(request, org_id):
    """
    Displays the positions in an organization, assuming that the logged in
    user is a member of said organization
    """
    print("hi there")
    U = request.user
    UID = U.id
    mem = models.Member.objects.filter(User_id=UID, Organization_id=org_id)
    org = models.Organization.objects.get(pk=org_id)
    if U.is_authenticated():
        lgnabl = True
    else:
        lgnabl = None
    if len(mem) > 0:
        showing = models.Position.objects.filter(Organization_id=org_id)
        return render(request, 'position_view.html',
                      {'positions': showing, 'Organization_name': org.Name,
                       "user": U, "loginable": lgnabl})
    else:
        return "<html><head></head><body>Silly person, you can't read " \
               "that.</body></html>"


def user_page(request):
    U = request.user
    UID = U.id
    assoc_members = U.member_set.all()
    print(dir(assoc_members[0]))
    if U.is_authenticated():
        lgnabl = True
    else:
        lgnabl = None
    return render(request, "user_view.html",
                  {"user": U, "assoc_members": assoc_members,
                   "loginable": lgnabl})


def logout_page(request):
    from django.contrib.auth import logout

    logout(request)
    return render(request, "logout.html")


def login(request):
    from django.contrib.auth import authenticate, login
    from django.shortcuts import redirect

    if request.method == "POST":
        u = request.POST["username"]
        p = request.POST["password"]
        user = authenticate(username=u, password=p)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('/user')
            else:
                return redirect('/list_org/')
    else:
        return render(request, 'login.html')