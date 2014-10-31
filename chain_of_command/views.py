from django.shortcuts import render
from chain_of_command import models, forms
from django.http import Http404
from django.contrib.auth.decorators import login_required


def organization_list(request):
    """Render a page showing all of the organizations
    :param request: The network request."""
    user = request.user
    if user.is_authenticated():
        lgnabl = True
    else:
        lgnabl = None
    latest_org_list = models.Organization.objects.all()
    context = {"user": user,
               "loginable": lgnabl, "orgs": latest_org_list}
    return render(request, 'Org_list.html', context)
    # Create your views here.


def organization_view(request, org_id):
    """Render a page showing most of the relevant information about
    organizations
    :param request: The network request.
    :param org_id: The id of the organization.
    :return A response containing the rendered page."""
    user = request.user
    can_see_provisional = False
    can_delete = False
    if user.is_authenticated():
        lgnabl = True
        mship = models.Member.objects.filter(User_id=user.id,
                                             Organization_id=org_id)
        can_see_provisional = len(mship) > 0
        for valid_membership in mship:
            for position in valid_membership.position_set.all():
                print(position.Name)
                print(position.Organization_id)
                if position.Name == 'admin':
                    can_delete = True
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
                   "loginable": lgnabl,
                   'canseeprovisional': can_see_provisional,
                   'candelete': can_delete})


def registration_form(request):
    """Renders a registration page that allows a user to register
    :param request:
    """
    from django.contrib.auth.forms import UserCreationForm
    from django.http import HttpResponseRedirect

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/user")
    else:
        user_create_form = UserCreationForm()
        return render(request, 'generic_form.html',
                      {"form": user_create_form, "form_action": "/register",
                       "form_method": "POST"})


@login_required
def position_display(request, org_id):
    """
    Displays the positions in an organization, assuming that the logged in
    user is a member of said organization
    :param org_id: The id of the organization in question
    :param request: The httprequest of the user in general
    """
    user = request.user
    user_id = user.id
    mem = models.Member.objects.filter(User_id=user_id, Organization_id=org_id)
    user = object()
    for i in mem:
        for j in i.position_set.all():
            if j.CanEditPrivileges:
                user = j
    org = models.Organization.objects.get(pk=org_id)
    if user.is_authenticated():
        lgnabl = True
    else:
        lgnabl = None
    if len(mem) > 0:
        showing = models.Position.objects.filter(Organization_id=org_id)
        return render(request, 'position_view.html',
                      {'positions': showing, 'Organization_name': org.Name,
                       "user": user, "loginable": lgnabl, 'usr': user})
    else:
        return "<html><head></head><body>Silly person, you can't read " \
               "that.</body></html>"


@login_required()
def edit_position(request, org_id, pos_id):
    """Renders a page and or handles a request to edit positions associated
    with an organization
    :param request: The network request.
    :param org_id: The organization id.
    :param pos_id: The id of the position in question."""
    from django.shortcuts import redirect

    form = forms.PositionForm(org_id,
                              instance=models.Position.objects.get(pk=pos_id))
    user_id = request.user.id
    mem = models.Member.objects.filter(User_id=user_id, Organization_id=org_id)
    canbehere = False
    for member in mem:
        for position in member.position_set.all():
            if position.CanEditPrivileges:
                canbehere = True
                break
        if canbehere:
            break
    if canbehere:
        if request.method == "GET":
            print(dir(form))
            return render(request, 'generic_form.html',
                          {'form': form, 'Form_Title': "Edit position",
                           "form_action": "",
                           "form_method": 'POST',
                           'user': request.user,
                           'loginable': request.user.is_authenticated()})
        else:
            form_object = forms.PositionForm(org_id, request.POST,
                                             instance=
                                             models.Position.objects.get(
                                                 pk=pos_id))
            if form_object.is_valid():
                form_object.save()
    return redirect('/list_org')


@login_required()
def create_position(request, org_id):
    """Renders a page with a new position form, and handles the creation.
    :param request: The network request.
    :param org_id: The organization id."""
    from django.shortcuts import redirect

    form = forms.PositionForm(org_id)
    user_id = request.user.id
    mem = models.Member.objects.filter(User_id=user_id, Organization_id=org_id)
    canbehere = False
    for i in mem:
        for j in i.position_set.all():
            if j.CanEditPrivileges:
                canbehere = True
                break
        if canbehere:
            break
    if canbehere:
        if request.method == "GET":
            print(dir(form))
            return render(request, 'generic_form.html',
                          {'form': form, 'Form_Title': "Create Position",
                           "form_action": "",
                           "form_method": 'POST',
                           'user': request.user,
                           'loginable': request.user.is_authenticated()})
        else:
            position_form = forms.PositionForm(org_id, request.POST)
            if position_form.is_valid():
                position_form.save()
            return redirect('/org/%s/positions' % org_id)
    return redirect('/list_org')


def user_page(request):
    """
    Render a user control page.
    :param request: The network request.
    :return: A response containing the user control panel.
    """
    user = request.user
    if hasattr(user, 'member_set'):
        assoc_members = user.member_set.all()
    else:
        assoc_members = None
    if user.is_authenticated():
        lgnabl = True
    else:
        lgnabl = None
    return render(request, "user_view.html",
                  {"user": user, "assoc_members": assoc_members,
                   "loginable": lgnabl})


def logout_page(request):
    from django.contrib.auth import logout

    logout(request)
    return render(request, "logout.html")


def login(request):
    """Render a login page.
    :param request: A network request.
    :return: A response that is either a redirect to the user control panel
    or the page the user was previously on."""
    from django.contrib.auth import authenticate, login
    from django.shortcuts import redirect

    if request.GET is not None and 'next' in request.GET:
        if request.GET['next'] is not None:
            redirect = request.GET['next']
        else:
            # otherwise redirect to the user control panel
            redirect = "/user"
    else:
        # otherwise redirect to the user control panel
        redirect = '/user/'
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        # Don't need to check if this exists because the form should have
        # been filled with a default redirection leading to the user.
        if 'next' in request.POST:
            redirect = request.POST['next']
        else:
            redirect = '/user'
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect(redirect)
            else:
                return redirect('/login/')
        else:
            return redirect('/login/?next=%s' % request.path)
    else:
        return render(request, 'login.html', {'next': redirect})


@login_required()
def create_organization(request):
    """
    Render a form for creating a new organization
    :param request: A network request.
    :return: A response to either redirect to the new organization, or the
    form itself.
    """
    from django.shortcuts import redirect

    if request.method == "GET":
        return render(request, "generic_form.html",
                      {"user": request.user,
                       "loginable": request.user.is_authenticated(),
                       'form': forms.OrganizationForm(),
                       'form_action': '/org/create/',
                       'form_method': 'POST'})
    else:
        org_form = forms.OrganizationForm(request.POST)
        if org_form.is_valid():
            descr = org_form.cleaned_data['Description']
            oname = org_form.cleaned_data['Name']
            mname = org_form.cleaned_data['MemberName']
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
    """
    Renders a page with a form for creating a new post
    :param request: The network request.
    :param member_id: The id of the member object(in the database)
    :return: Either a rendered web page, or a redirect to the new post
    """
    from datetime import datetime
    from django.shortcuts import redirect

    if request.user.member_set.get(pk=member_id) is not None:
        if request.method == 'POST':
            new_post_form = forms.PostForm(request.POST)
            if new_post_form.is_valid():
                title = new_post_form.cleaned_data['Title']
                creator = models.Member.objects.get(pk=member_id)
                content = new_post_form.cleaned_data['Content']
                timestamp = datetime.now()
                visible = new_post_form.cleaned_data['Visible']
                new_post = models.Post(Title=title, Creator=creator,
                                       Content=content,
                                       timestamp=timestamp, Visible=visible)
                new_post.save()
                return redirect('/post/%s/view' % str(new_post.id))
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
    """
    Render a post if the user has permission to view it.
    :param request: The network request.
    :param post_id: The id of the post object to render.
    :return: A response rendering a post(if it exists).
    """

    def can_view_post(user, pid):
        post_ = models.Post.objects.get(pk=pid)
        for member in user.member_set.all():
            if member.Organization_id == post_.Creator.Organization_id:
                return True
        return False

    post = models.Post.objects.get(pk=post_id)
    if not post.Visible:
        if can_view_post(request.user, post_id):
            return render(request, 'view_post.html',
                          {'title': post.Title, 'Content': post.Content,
                           'user': request.user,
                           'loginable': request.user.is_authenticated()})
        else:
            return render(request, 'Error.html',
                          {'error_summary': 'Not visible',
                           'error_details': 'You must have permission to view '
                                            'this post'})
    else:
        return render(request, 'view_post.html',
                      {'title': post.Title, 'Content': post.Content,
                       'user': request.user,
                       'loginable': request.user.is_authenticated()})


@login_required()
def edit_post(request, post_id):
    """
    Render a response with a post.
    :param request: The network request.
    :param post_id: The post id.
    """
    from django.shortcuts import redirect

    post = models.Post.objects.get(pk=post_id)
    if post is None:
        return render(request, "generic_form.html",
                      {'error_summary': 'There is no post with that id',
                       'error_detail': 'This post does not exist, perhaps the '
                                       'post was deleted'})
    allowed_member = request.user.member_set.get(pk=post.Creator_id)
    if allowed_member is not None:
        if request.method == 'GET':
            return render(request, "generic_form.html",
                          {'form': forms.PostForm(instance=post),
                           'Form_Title': "create post",
                           "form_action": "/post/%s/edit" % str(post_id),
                           "form_method": 'POST',
                           'user': request.user,
                           'loginable': request.user.is_authenticated()})
        else:
            post_form = forms.PostForm(request.POST)
            if post_form.is_valid():
                post.Content = post_form.cleaned_data['Content']
                post.save()
            return redirect('/post/%s/view' % str(post.id))


@login_required()
def apply_to_org(request):
    """
    Renders a form or processes a request to join an organization.
    :param request: The network request
    :return: Either a redirect or a form.
    """
    from django.shortcuts import redirect

    if request.method == "GET":
        org_id = request.GET['org_id']
        form = forms.OrgApplicationForm()
        return render(request, 'generic_form.html',
                      {'form': form, 'Form_Title': 'Applying to org',
                       'form_action': '/org/apply/', 'form_method': 'POST',
                       'user': request.user,
                       'loginable': request.user.is_authenticated()})
    else:
        form = forms.OrgApplicationForm(request.POST)
        if form.is_valid():
            new_member = models.Member(
                Organization=form.cleaned_data["Organization"])
            new_member.Name = form.cleaned_data['member_name']
            new_member.User_id = request.user.id
            new_member.Provisional = True
            new_member.save()
            return redirect("/user")


@login_required()
def delete_org(request, org_id):
    from django.shortcuts import redirect

    user = request.user
    can_delete = False
    if user.is_authenticated():
        mship = models.Member.objects.filter(User_id=user.id,
                                             Organization_id=org_id)
        for member in mship:
            for position in member.position_set.all():
                print(position.Name)
                print(position.Organization_id)
                if position.Name == 'admin':
                    can_delete = True
    if can_delete:
        models.Organization.objects.get(pk=org_id).delete()
        return redirect('/list_org')
    else:
        return render(request, 'Error.html', {'error_summary': 'Invalid access',
                                              'error_details': 'You must be '
                                                               'the '
                                                               'administrator '
                                                               'of the '
                                                               'organization '
                                                               'to delete it'})
