from django.shortcuts               import render, get_object_or_404, redirect
from django.utils                   import timezone
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
  

@login_required
def user_process(request, pk='0', function="update"):

  activeuser                 =  User.objects.get(id=request.user.id)    # get details of activeuser
  activeperson               =  Person.objects.get(username=activeuser.username)
  if function                in ['password', 'displayname']:
    person                   =  activeperson
    user                     =  activeuser
  elif function              != 'insert':
    person                   =  get_object_or_404(Person, pk=pk)     # get details of person to be updated/displayed/deleted
    user                     =  User.objects.get(username=person.username)

    if activeperson.status                >= 60:
      can_update                          = True 
    else:
      can_update                          = False   
    if activeperson.status                >= 60                              \
    or person.authorname                  == activeperson.username:
      can_remove                          = True 
    else:
      can_remove                          = False   
    if activeperson.status                >= 50                              \
    and person.fullmember                 == False:
      can_promote                         = True 
    else:
      can_promote                         = False   
    if activeperson.status                >= 50                              \
    and person.fullmember                 == True                            \
    and person.status                     <  40:
      can_demote                          = True 
    else:
      can_demote                          = False   
  # info to be passed to insert_update.html
  # activeperson.status
  # ?activeperson.username == person.username i.e. 'self' record
  # ?activeperson.username == person.authorname i.e. 'author' record
  # ? insert or update
  if request.method                           != "POST": # i.e. method == "GET":

    # arrives at 'detail' from 'users/list.html'
    if function                               == 'detail':
      return render(request, 'users/user_detail.html', \
      {'person': person, 'can_remove': can_remove, 'can_promote': can_promote, 'can_demote': can_demote, 'can_update': can_update})  

    # arrives at 'insert', 'password', 'displayname' from 'events/list.html'
    elif function                             == 'insert':
      form = InsertPersonForm()                                               # get a blank InsertPersonForm
      return render(request, 'users/insert_update.html', {'form': form})    
                                                                              # ask activeuser for details of new/updated user
    elif function                             == 'password':            
      form = PasswordForm()                     
      # get a UpdatePersonForm filled with details of Profile to be upd
      return render(request, 'users/password.html', {'form': form})  
    elif function                             == 'displayname':
      form = DisplaynameForm(initial = {'display_name': person.display_name})         
      # get a UpdatePersonForm filled with details of Profile to be upd
      return render(request, 'users/displayname.html', {'form': form})                # ask activeuser for details of new/updated user
      
       
    # arrives at 'deleteperm', 'promote', 'demote', 'update' from 'users/user_detail.html'
    elif function                             == 'deleteperm':
      user.delete()
      person.delete()
      return redirect('users.views.user_list')                                # give to activeuser list of users
    elif function                             == 'promote':
      person.fullmember                       =  True
      person.authorname                       =  'Full'
      person.save()                                                                   # update user record with extra details
      #form.save_m2m()
      return redirect('users.views.user_list')   
    elif function                             == 'demote':
      person.fullmember                       =  False
      person.authorname                       =  ''
      person.save()                                                                   # update user record with extra details
      #form.save_m2m()
      return redirect('users.views.user_list')    
    else:                                     # i.e. function == 'update'
      form = UpdatePersonForm(instance=person)                                # get a UpdatePersonForm filled with details of Profile to be upd
      return render(request, 'users/insert_update.html', {'form': form})                # ask activeuser for details of new/updated user

  else:                  # i.e method == 'POST'
    if function          == 'insert':
      form               = InsertPersonForm(request.POST)                     # get a InsertPersonForm filled with details of new user 
      if form.is_valid():
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
    elif function        == 'displayname':
      form               = DisplaynameForm(request.POST)
      if form.is_valid():
        person.display_name                 = form.cleaned_data['display_name']
        person.save() 
        user.first_name                     = form.cleaned_data['display_name']
        user.save()                                                            
        return redirect('users.views.user_list')  
      else:                                                                        # i.e. form is not valid, ask activeuser to resubmit it
        return render(request, 'users/insert_update.html', {'form': form})
    elif function        == 'password':
      form               = PasswordForm(request.POST)
      if form.is_valid():
        password                            = form.cleaned_data['password']
        user.set_password(password)
        user.save()                                                              
        return redirect('events.views.event_list')    
      else:                                                                        # i.e. form is not valid, ask activeuser to resubmit it
        return render(request, 'users/insert_update.html', {'form': form})
    else:                # i.e. function == 'update'.
      form               = UpdatePersonForm(request.POST, instance=person)    # get a UpdatePersonForm filled with details of updated user
      if form.is_valid():
        person                                = form.save(commit=False)                 # extract details from user form
        user.first_name                       = person.display_name
        user.save()
        person.save()                                                                   # update user record with extra details
        form.save_m2m()
        return redirect('users.views.user_list')
      else:                                                                        # i.e. form is not valid, ask activeuser to resubmit it
        return render(request, 'users/insert_update.html', {'form': form})

