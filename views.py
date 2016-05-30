from django.shortcuts               import render, get_object_or_404, redirect
#from django.utils                   import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models     import User
from .models                        import Person
from .forms                         import UpdateMemberForm, UserOptionsForm, InsertMemberForm, InsertContactForm, \
                                    PasswordForm, DisplaynameForm
from mysite.settings                import IS_CLUB

    #status == 05      is a contact, not a member, does not have a login and can only be added to an event by a member
    #status == 10      can view event dates and titles. This is only used for user 'default', which is someone viewing the site without logging in
    #status == 15      also can view event details. This can be used for 'default' user on some sites. May also be used for some logged in users.
    #status == 20      also can book into and out of events
    #status == 30      also can put events on the programme and update/delete their own events
    #status == 35      also can add members
    #status == 40      also can view more user details and update/delete any event
    #status == 50      also can change whether fullmember
    #status == 60      also can remove members and make any update

# functions which do not update the database
# and don't require a pk as they don't refer to an specific record
@login_required
def member_list(request):
    activeuser                              =  User.objects.get(id=request.user.id)
    activeperson                            =  Person.objects.get(username=activeuser.username)
    persons                             =  Person.objects.all().order_by('display_name')
    return render(request, 'users/member_list.html', {'persons': persons, 'activeperson': activeperson, 'IS_CLUB': IS_CLUB})

'''
@login_required
def contact_list(request):
    persons                             =  Person.objects.filter(status=5).order_by('display_name')
    return render(request, 'users/contact_list.html', {'persons': persons, 'activeperson': activeperson, 'IS_CLUB': IS_CLUB})
'''

# functions which do not update the database
# but do require a pk as they refer to an existing record
def member_detail(request, pk):
  activeuser                            =  User.objects.get(id=request.user.id)
  activeperson                          =  Person.objects.get(username=activeuser.username)
  person                                =  get_object_or_404(Person, pk=pk)     # get details of person to be updated/displayed/deleted
  #user                                  =  User.objects.get(username=person.username)
  if activeperson.status                >= 60:
    can_update                          =  True
  else:
    can_update                          =  False
  if activeperson.status                >= 60 \
  or person.authorname                  == activeperson.username:
    can_remove                          =  True
  else:
    can_remove                          =  False
  return render(request, 'users/member_detail.html', {'person': person, 'activeperson': activeperson, 'can_update':can_update,'can_remove':can_remove})

'''
def contact_detail(request, pk):
  person                                =  get_object_or_404(Person, pk=pk)     # get details of person to be updated/displayed/deleted
  #user                                  =  User.objects.get(username=person.username)
  return render(request, 'users/contact_detail.html', {'person': person})
'''

# functions which update the database using parameters in the url, without using forms
# but do not require a pk as they refer to activeuser
@login_required
def unsubscribe(request, confirmed):
  if confirmed                 == 'no':
    return render(request, 'users/unsubscribe.html', {})
  else:
    activeuser                 =  User.objects.get(id=request.user.id)    # get details of activeuser
    activeperson               =  Person.objects.get(username=activeuser.username)
    activeuser.delete()
    activeperson.delete()
    unsubscribed               =  True
    #return redirect('django.contrib.auth.views.logout')
    return render(request, 'users/unsubscribe_confirmed.html', {'unsubscribed': unsubscribed})
    #return redirect('django.contrib.auth.views.logout')

# functions which update the database using parameters in the url, without using form
# and do require a pk as they refer to a user who is not, generally, the activeuser
@login_required
def member_delete(request, pk, confirmed):
  if confirmed                 == 'no':
    return render(request, 'users/member_delete.html', {'pk': pk})
  else:
    activeuser                 =  User.objects.get(id=request.user.id)    # get details of activeuser
    activeperson               =  Person.objects.get(username=activeuser.username)
    person                     =  get_object_or_404(Person, pk=pk)     # get details of person to be updated/displayed/deleted
    if activeperson.status     >= 60                              \
    or person.authorname       == activeperson.username:
      person.delete()
      try:
        user                       =  User.objects.get(username=person.username)
        user.delete()
      except:
        pass
    return redirect('users.views.member_list')

'''
@login_required
def contact_delete(request, pk, confirmed):
  if confirmed                 == 'no':
    return render(request, 'users/contact_delete.html', {'pk': pk})
  else:
    person                     =  get_object_or_404(Person, pk=pk)     # get details of person to be updated/displayed/deleted
    person.delete()
    return redirect('users.views.contact_list')
'''

@login_required
def promote(request, pk):
  activeuser                 =  User.objects.get(id=request.user.id)    # get details of activeuser
  activeperson               =  Person.objects.get(username=activeuser.username)
  person                     =  get_object_or_404(Person, pk=pk)     # get details of person to be updated/displayed/deleted
  if activeperson.status                >= 50                              \
  and person.fullmember                 == False:
    person.fullmember                   =  True
    person.authorname                   =  ''
    person.save()                                                                   # update user record with extra details
    #form.save_m2m()
    return redirect('users.views.member_list')

@login_required
def demote(request, pk):
  activeuser                 =  User.objects.get(id=request.user.id)    # get details of activeuser
  activeperson               =  Person.objects.get(username=activeuser.username)
  person                     =  get_object_or_404(Person, pk=pk)     # get details of person to be updated/displayed/deleted
  if activeperson.status                >= 50                              \
  and person.fullmember                 == True:
    person.fullmember                   =  False
    person.authorname                   =  ''
    person.save()                                                                   # update user record with extra details
    #form.save_m2m()
    return redirect('users.views.member_list')




# functions which update the database in two stages,  using forms
# but don't require a pk as they don't refer to an existing record
@login_required
def member_insert(request):
  activeuser                            =  User.objects.get(id=request.user.id)    # get details of activeuser
  activeperson                          =  Person.objects.get(username=activeuser.username)
  if activeperson.status                >= 35:
    can_insert                          = True
  else:
    can_insert                          = False
  if request.method                     != "POST": # i.e. method == "GET":
    if can_insert:
      form = InsertMemberForm()                                               # get a blank InsertPersonForm
      return render(request, 'users/member_new.html', {'form': form})
    else:
      return redirect('events.views.event_list')
  else:                                 # i.e method == 'POST'
    form                                = InsertMemberForm(request.POST)                     # get a InsertPersonForm filled with details of new user
    if form.is_valid()\
    and can_insert:
      person                                = form.save(commit=False)                 # extract details from user for
      person.fullmember                     = False
      person.status                         =  20
      person.detailcolor                    = '#0000C0'
      person.attendeescolor                 = '#00C000'
      person.backgroundcolor                = '#F3FFF3'
      person.authorname                     = activeperson.username
      user = User.objects.create_user(person.username, 'a@a.com', person.password)  # create user record from form
      user.first_name                       = person.display_name
      user.save()
      person.save()                                                                   # update user record with extra details
      form.save_m2m()
      return redirect('users.views.member_list')
    else:                                                                        # i.e. form is not valid, ask activeuser to resubmit it
      return render(request, 'users/insert_update.html', {'form': form})

@login_required
def contact_insert(request):

  if request.method                     != "POST": # i.e. method == "GET":
    form = InsertContactForm()                                               # get a blank InsertPersonForm
    return render(request, 'users/contact_new.html', {'form': form})
  else:                                 # i.e method == 'POST'
    form                                = InsertContactForm(request.POST)                     # get a InsertPersonForm filled with details of new user
    if form.is_valid():
      person                                = form.save(commit=False)                 # extract details from user for
      person.username                       = 'nologin'
      person.fullmember                     = False
      person.status                         =  5
      person.save()                                                                   # update user record with extra details
      form.save_m2m()
      return redirect('users.views.contact_list')
    else:                                                                        # i.e. form is not valid, ask activeuser to resubmit it
      return render(request, 'users/contact_new.html', {'form': form})




# functions which update the database in two stages,  using forms
# but do not require a pk as they refer to activeuser
@login_required
def password(request):
  if request.method                           != "POST": # i.e. method == "GET":
    form = PasswordForm()
    #get a UpdatePersonForm filled with details of Profile to be upd
    return render(request, 'users/password.html', {'form': form})
  else:                                       # i.e method == 'POST'
    form                                      = PasswordForm(request.POST)
    if form.is_valid():
      activeuser                              =  User.objects.get(id=request.user.id)    # get details of activeuser
      password                                = form.cleaned_data['password']
      activeuser.set_password(password)
      activeuser.save()
      return redirect('events.views.event_list')
    else:                                                                        # i.e. form is not valid, ask activeuser to resubmit it
      return render(request, 'users/insert_update.html', {'form': form})

@login_required
def display_name(request):
  activeuser                 =  User.objects.get(id=request.user.id)    # get details of activeuser
  activeperson               =  Person.objects.get(username=activeuser.username)
  if request.method                           != "POST": # i.e. method == "GET":
    form = DisplaynameForm(initial = {'display_name': activeperson.display_name})
    # get a UpdatePersonForm filled with details of Profile to be upd
    return render(request, 'users/displayname.html', {'form': form})                # ask activeuser for details of new/updated user
  else:
    form                     = DisplaynameForm(request.POST)
    if form.is_valid():
      activeperson.display_name                 = form.cleaned_data['display_name']
      activeperson.save()
      activeuser.first_name                     = form.cleaned_data['display_name']
      activeuser.save()
      return redirect('users.views.member_list')
    else:                                                                        # i.e. form is not valid, ask activeuser to resubmit it
      return render(request, 'users/insert_update.html', {'form': form})


@login_required
def user_options(request, whence, type='get', color='black' ):
  activeuser                 =  User.objects.get(id=request.user.id)    # get details of activeuser
  activeperson               =  Person.objects.get(username=activeuser.username)
  if request.method          != "POST": # i.e. method == "GET":
    if type                  == 'get':
      form = UserOptionsForm(instance = activeperson)
      return render(request, 'users/useroptions.html', {'form': form, 'activeperson': activeperson, 'whence': whence})                # ask activeuser for details of new/updated user
    else:
      if activeperson.reversevideo           == False:
        if type                              == 'date':
          activeperson.datecolor             = color
        elif type                            == 'detail':
          activeperson.detailcolor           = color
        elif type                            == 'attendees':
          activeperson.attendeescolor        = color
        elif type                            == 'background':
          activeperson.backgroundcolor       = color
        elif type                            == 'reverse':
          activeperson.reversevideo          = True
        else:
          return redirect('useroptions', 'get', 'get', whence)
      elif activeperson.reversevideo         == True:
        if type                              == 'date':
          activeperson.datecolor_rev         = color
        elif type                            == 'detail':
          activeperson.detailcolor_rev       = color
        elif type                            == 'attendees':
          activeperson.attendeescolor_rev    = color
        elif type                            == 'background':
          activeperson.backgroundcolor_rev   = color
        elif type                            == 'forward':
          activeperson.reversevideo          = False
        else:
          return redirect('useroptions', 'get', 'get', whence)
      else:
        return redirect('useroptions', 'get', 'get', whence)

      activeperson.save()
      if type                          in ['reverse', 'forward']:
        return redirect('useroptions', 'get', 'get', whence)
      else:
        if whence == 'events':
          return redirect('events.views.event_list')
        elif whence == 'users':
          return redirect('users.views.member_list')

  else:
    form                     = UserOptionsForm(request.POST)
    if form.is_valid():
      activeperson.display_name                 = form.cleaned_data['display_name']
      activeperson.save()
      activeuser.first_name                     = form.cleaned_data['display_name']
      activeuser.save()
      return redirect('events.views.event_list')
    else:                                                                        # i.e. form is not valid, ask activeuser to resubmit it
      return render(request, 'users/useroptions.html', {'form': form, 'whence': whence})

# functions which update the database in two stages,  using forms
# and do require a pk as they refer to a user who is not, generally, the activeuser
@login_required
def member_amend(request, pk):
  activeuser                            =  User.objects.get(id=request.user.id)    # get details of activeuser
  activeperson                          =  Person.objects.get(username=activeuser.username)
  person                                =  get_object_or_404(Person, pk=pk)     # get details of person to be updated/displayed/deleted
  user                                  =  User.objects.get(username=person.username)

  if request.method                     != "POST": # i.e. method == "GET":
    form = UpdateMemberForm(instance=person)                                # get a UpdatePersonForm filled with details of Profile to be upd
    return render(request, 'users/member_amended.html', {'form': form})                # ask activeuser for details of new/updated user
  else:                                 # i.e method == 'POST'
    form                                = UpdateMemberForm(request.POST, instance=person)
    if form.is_valid()\
    and activeperson.status             >= 60:
      person                            = form.save(commit=False)                 # extract details from user form
      user.first_name                   = person.display_name
      user.save()
      person.save()                                                                   # update user record with extra details
      form.save_m2m()
      return redirect('users.views.member_list')
    else:                                                                        # i.e. form is not valid, ask activeuser to resubmit it
      return render(request, 'users/member_amended.html', {'form': form})

'''
@login_required
def contact_amend(request, pk):
  #activeuser                            =  User.objects.get(id=request.user.id)    # get details of activeuser
  #activeperson                          =  Person.objects.get(username=activeuser.username)
  person                                =  get_object_or_404(Person, pk=pk)     # get details of person to be updated/displayed/deleted
  #user                                  =  User.objects.get(username=person.username)

  if request.method                     != "POST": # i.e. method == "GET":
    form = UpdateContactForm(instance=person)                                # get a UpdatePersonForm filled with details of Profile to be upd
    return render(request, 'users/member_amended.html', {'form': form})                # ask activeuser for details of new/updated user
  else:                                 # i.e method == 'POST'
    form                                = UpdateContactForm(request.POST, instance=person)
    if form.is_valid():
      person                            = form.save(commit=False)                 # extract details from user form
      person.save()                                                                   # update user record with extra details
      form.save_m2m()
      return redirect('users.views.contact_list')
    else:                                                                        # i.e. form is not valid, ask activeuser to resubmit it
      return render(request, 'users/contact_amended.html', {'form': form})
'''


