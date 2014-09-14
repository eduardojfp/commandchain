from django.shortcuts import render
from chain_of_command import models, forms
from django.http import Http404
from django.contrib.auth.decorators import login_required
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


@login_required
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

    if request.GET is not None and 'next' in request.GET:
        if request.GET['next'] is not None:
            l = request.GET['next']
        else:
            # otherwise redirect to the user control panel
            l = "/user"
    else:
        # otherwise redirect to the user control panel
        l = '/user/'
    if request.method == "POST":
        u = request.POST["username"]
        p = request.POST["password"]
        # Don't need to check if this exists because the form should have
        # been filled with a default redirection leading to the user.
        l = request.POST['next']
        user = authenticate(username=u, password=p)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect(l)
            else:
                return redirect('/login/')
        else:
            return redirect('/login/?next=%s' % request.path)
    else:
        return render(request, 'login.html', {'next': l})


@login_required()
def create_organization(request):
    from django.shortcuts import redirect

    if request.method == "GET":
        return render(request, "create_organization.html",
                      {"user": request.user,
                       "loginable": request.user.is_authenticated()})
    else:
        descr = request.POST['organization_description']
        oname = request.POST['organization_name']
        mname = request.POST['member_name']
        org = models.Organization(Name=oname, Description=descr)
        org.save()
        pos = models.Position(Name="admin", Organization_id=org.id,
                              CanGrantMembership=True, CanIssueOrders=True,
                              CanEditOrganization=True,
                              CanEditPrivileges=True)
        pos.save()
        mem = models.Member(Name=mname, Organization_id=org.id,
                            User_id=request.user.id)
        mem.save()
        pos.associated.add(mem)
        pos.save()
        return redirect('/org/%d/' % org.id)