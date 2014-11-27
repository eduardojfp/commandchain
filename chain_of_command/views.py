from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from chain_of_command import models, forms


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
    from django.shortcuts import redirect as redir

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
                return redir(redirect)
            else:
                return redirect('/login/')
        else:
            return redirect('/login/?next=%s' % request.path)
    else:
        return render(request, 'login.html', {'next': redirect})


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
def list_orders(request):
    q = request.user.member_set.all()
    plist = []
    olist = []
    for i in q:
        for x in models.Position.objects.filter(associated=i):
            plist.append(x)
            print(dir(x))
            for z in x.order_set.all():
                olist.append(z)

    return render(request ,"order_list.html", {'user': request.user,
                                    'loginable': request.user.is_authenticated(),
                                    "plist": plist,
                                    'olist': olist})