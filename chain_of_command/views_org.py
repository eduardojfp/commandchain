from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render
from chain_of_command import forms, models

__author__ = 'awhite'


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