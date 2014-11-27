from chain_of_command import forms, models

__author__ = 'awhite'


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