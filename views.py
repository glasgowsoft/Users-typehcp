from django.shortcuts               import render, get_object_or_404, redirect
#from django.utils                   import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models     import User
from .models                        import Person
from .forms                         import UpdatePersonForm, InsertPersonForm, PasswordForm, DisplaynameForm

    #status == 0       not logged on
    #status == 20      can view event list and book into/out of events
    #status == 30      also can put events on the programme
    #status == 35      also can add prospectives
    #status == 40      committee, also can view more user details
    #status == 50      treasurer, also can change whether fullmember
    #status == 60      organizer, also can remove members and make any update

# functions which do not update the database
# and don't require a pk as they don't refer to an specific record
@login_required
def user_list(request):
    activeuser                              =  User.objects.get(id=request.user.id)
    activeperson                            =  Person.objects.get(username=activeuser.username)
    committee                               =  Person.objects.filter(status__gte = 40).order_by('display_name')
    if activeperson.status                  >= 40:
        committee                           =  Person.objects.filter(status__gte = 40).order_by('display_name')
        full                                =  Person.objects.filter(fullmember = True, status__lt = 40).order_by('display_name')
        members                             =  Person.objects.filter(fullmember = False).order_by('display_name')
        return render(request, 'users/list.html', \
        {'committee': committee, 'full': full, 'members': members, 'activeperson': activeperson})
    elif activeperson.fullmember:
        full                                =  Person.objects.filter(fullmember = True, status__lte = 60).order_by('display_name')
        members                             =  Person.objects.filter(fullmember = False).order_by('display_name')
        return render(request, 'users/list.html', {'full': full, 'members': members, 'activeperson': activeperson})
    else:
        members                             =  Person.objects.all().order_by('display_name')
        return render(request, 'users/list.html', {'members': members, 'activeperson': activeperson})

# functions which do not update the database
# but do require a pk as they refer to an existing record
def user_detail(request, pk):
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
  return render(request, 'users/user_detail.html', {'person': person,'can_update':can_update,'can_remove':can_remove})

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
def user_delete(request, pk, confirmed):
  if confirmed                 == 'no':
    return render(request, 'users/delete.html', {'pk': pk})
  else:
    activeuser                 =  User.objects.get(id=request.user.id)    # get details of activeuser
    activeperson               =  Person.objects.get(username=activeuser.username)
    person                     =  get_object_or_404(Person, pk=pk)     # get details of person to be updated/displayed/deleted
    user                       =  User.objects.get(username=person.username)
    if activeperson.status     >= 60                              \
    or person.authorname       == activeperson.username:
      user.delete()
      person.delete()
      return redirect('users.views.user_list')

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
    return redirect('users.views.user_list')

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
    return redirect('users.views.user_list')




# functions which update the database in two stages,  using forms
# but don't require a pk as they don't refer to an existing record
@login_required
def user_insert(request):
  activeuser                            =  User.objects.get(id=request.user.id)    # get details of activeuser
  activeperson                          =  Person.objects.get(username=activeuser.username)
  if activeperson.status                >= 35:
    can_insert                          = True
  else:
    can_insert                          = False
  if request.method                     != "POST": # i.e. method == "GET":
    if can_insert:
      form = InsertPersonForm()                                               # get a blank InsertPersonForm
      return render(request, 'users/insert_update.html', {'form': form})
    else:
      return redirect('events.views.event_list')
  else:                                 # i.e method == 'POST'
    form                                = InsertPersonForm(request.POST)                     # get a InsertPersonForm filled with details of new user
    if form.is_valid()\
    and can_insert:
      person                                = form.save(commit=False)                 # extract details from user for
      person.fullmember                     = False
      person.status                         =  20
      person.authorname                     = activeperson.username
      user = User.objects.create_user(person.username, 'a@a.com', person.password)  # create user record from form
      user.first_name                       = person.display_name
      user.save()
      person.save()                                                                   # update user record with extra details
      form.save_m2m()
      return redirect('users.views.user_list')
    else:                                                                        # i.e. form is not valid, ask activeuser to resubmit it
      return render(request, 'users/insert_update.html', {'form': form})

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
      return redirect('users.views.user_list')
    else:                                                                        # i.e. form is not valid, ask activeuser to resubmit it
      return render(request, 'users/insert_update.html', {'form': form})

# functions which update the database in two stages,  using forms
# and do require a pk as they refer to a user who is not, generally, the activeuser
@login_required
def user_update(request, pk):
  activeuser                            =  User.objects.get(id=request.user.id)    # get details of activeuser
  activeperson                          =  Person.objects.get(username=activeuser.username)
  person                                =  get_object_or_404(Person, pk=pk)     # get details of person to be updated/displayed/deleted
  user                                  =  User.objects.get(username=person.username)

  if request.method                     != "POST": # i.e. method == "GET":
    form = UpdatePersonForm(instance=person)                                # get a UpdatePersonForm filled with details of Profile to be upd
    return render(request, 'users/insert_update.html', {'form': form})                # ask activeuser for details of new/updated user
  else:                                 # i.e method == 'POST'
    form                                = UpdatePersonForm(request.POST, instance=person)
    if form.is_valid()\
    and activeperson.status             >= 60:
      person                            = form.save(commit=False)                 # extract details from user form
      user.first_name                   = person.display_name
      user.save()
      person.save()                                                                   # update user record with extra details
      form.save_m2m()
      return redirect('users.views.user_list')
    else:                                                                        # i.e. form is not valid, ask activeuser to resubmit it
      return render(request, 'users/insert_update.html', {'form': form})
