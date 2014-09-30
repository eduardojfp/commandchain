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
    context = {"user": U,
               "loginable": lgnabl, "orgs": latest_org_list}
    return render(request, 'Org_list.html', context)
    # Create your views here.


def OrganizationView(request, org_id):
    U = request.user
    UID = U.id
    canseeProvisional = False
    if U.is_authenticated():
        lgnabl = True
        mship = models.Member.objects.filter(User_id=U.id,
                                             Organization_id=org_id)
        canseeProvisional = len(mship) > 0
    else:
        lgnabl = None
    try:
        org = models.Organization.objects.get(pk=org_id)
        # print(dir(org.member_set.all()))
        mem = org.member_set.order_by('Name')
        print(dir(mem[0]))
    except models.Organization.DoesNotExist:
        raise Http404
    return render(request, 'org_view.html',
                  {'Org': org, 'mem': mem,
                   "loginable": lgnabl, 'canseeprovisional': canseeProvisional})


def registration_form(request):
    """Renders a registration page that allows a user to register"""
    from django.contrib.auth.forms import UserCreationForm
    from django.http import HttpResponseRedirect

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return HttpResponseRedirect("/user")
    else:
        u = UserCreationForm()
        return render(request, 'generic_form.html',
                      {"form": u, "form_action": "/register",
                       "form_method": "POST"})


@login_required
def position_display(request, org_id):
    """
    Displays the positions in an organization, assuming that the logged in
    user is a member of said organization
    """
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
    if hasattr(U, 'member_set'):
        assoc_members = U.member_set.all()
    else:
        assoc_members = None
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
        if 'next' in request.POST:
            l = request.POST['next']
        else:
            l = '/user'
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
        return render(request, "generic_form.html",
                      {"user": request.user,
                       "loginable": request.user.is_authenticated(),
                       'form': forms.OrganizationForm(),
                       'form_action': '/org/create/',
                       'form_method': 'POST'})
    else:
        g = forms.OrganizationForm(request.POST)
        if g.is_valid():
            descr = g.cleaned_data['Description']
            oname = g.cleaned_data['Name']
            mname = g.cleaned_data['MemberName']
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


@login_required
def create_post(request, member_id):
    from datetime import datetime
    from django.shortcuts import redirect

    if request.user.member_set.get(pk=member_id) is not None:
        if request.method == 'POST':
            c = forms.PostForm(request.POST)
            if c.is_valid():
                title = c.cleaned_data['Title']
                creator = models.Member.objects.get(pk=member_id)
                content = c.cleaned_data['Content']
                timestamp = datetime.now()
                visible = c.cleaned_data['Visible']
                q = models.Post(Title=title, Creator=creator, Content=content,
                                timestamp=timestamp, Visible=visible)
                q.save()
                return redirect('/post/%s/view' % str(q.id))
        else:
            return render(request, "generic_form.html",
                          {'form': forms.PostForm, 'Form_Title': "create post",
                           "form_action": "/post/%s/create" % str(member_id),
                           "form_method": 'POST',
                           'user': request.user,
                           'loginable': request.user.is_authenticated()})
    else:
        return render(request, 'Error.html',
                      {'error_summary': 'cannae post there',
                       'error_details': 'You may not post as a member whose '
                                        'life you cannot control',
                       'user': request.user,
                       'loginable': request.user.is_authenticated()})


def view_post(request, post_id):
    def canViewPost(user, pid):
        p = models.Post.objects.get(pk=pid)
        for x in user.member_set.all():
            if x.Organization_id == p.Creator.Organization_id:
                return True
        return False

    p = models.Post.objects.get(pk=post_id)
    if not p.Visible:
        if canViewPost(request.user, post_id):
            return render(request, 'view_post.html',
                          {'title': p.Title, 'Content': p.Content,
                           'user': request.user,
                           'loginable': request.user.is_authenticated()})
        else:
            return render(request, 'Error.html',
                          {'error_summary': 'NOt visible',
                           'error_details': 'You must have permission to view '
                                            'this post'})
    else:
        return render(request, 'view_post.html',
                      {'title': p.Title, 'Content': p.Content,
                       'user': request.user,
                       'loginable': request.user.is_authenticated()})


@login_required()
def edit_post(request, post_id):
    from datetime import datetime
    from django.shortcuts import redirect

    i = models.Post.objects.get(pk=post_id)
    m = request.user.member_set.get(pk=i.Creator_id)
    if m is not None:
        if request.method == 'GET':
            return render(request, "generic_form.html",
                          {'form': forms.PostForm(instance=i),
                           'Form_Title': "create post",
                           "form_action": "/post/%s/edit" % str(post_id),
                           "form_method": 'POST',
                           'user': request.user,
                           'loginable': request.user.is_authenticated()})
        else:
            c = forms.PostForm(request.POST)
            if c.is_valid():
                i.Content = c.cleaned_data['Content']
                i.save()
            return redirect('/post/%s/view' % str(i.id))


@login_required()
def apply_to_org(request):
    from django.shortcuts import redirect

    if request.method == "GET":
        org_id = request.GET['org_id']
        form = forms.Org_applicationForm()
        return render(request, 'generic_form.html',
                      {'form': form, 'Form_Title': 'Applying to org',
                       'form_action': '/org/apply/', 'form_method': 'POST',
                       'user': request.user,
                       'loginable': request.user.is_authenticated()})
    else:
        form = forms.Org_applicationForm(request.POST)
        if form.is_valid():
            nm = models.Member(Organization=form.cleaned_data["Organization"])
            nm.Name = form.cleaned_data['member_name']
            nm.User_id = request.user.id
            nm.Provisional = True
            nm.save()
            return redirect("/user")