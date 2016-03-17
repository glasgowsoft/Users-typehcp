from django.shortcuts               import render, get_object_or_404, redirect
from django.utils                   import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models     import User
from .models                        import Person
from .forms                         import PersonForm

    #status == 0       not logged on
    #status == 10      casual member, or full member that the program has not yet verified
    #status == 20      full member
    #status == 30      event organizer - not on committee
    #status == 40      committee         not treasurer or organizer
    #status == 50      treasurer
    #status == 60      organizer

def user_list(request):
    persons                                 =  Person.objects.all().order_by('display_name')

    activeuser                              =  User.objects.get(id=request.user.id)
    activeperson                            =  Person.objects.get(username=activeuser.username)
    return render(request, 'users/list.html', {'persons': persons, 'activeperson': activeperson})
    #return render(request, 'users/list.html', {'persons': persons, 'activeperson.status': activeperson.status})

    '''
    activeperson.status                     = 0
    if request.user.is_authenticated():
        activeuser                               =  User.objects.get(id=request.user.id)
        activeperson.status                 = 10
        try:
            activeperson                    =  Person.objects.get(username=activeuser.username)
            activeperson.status             =  activeperson.status              # should always go here
        except:
            pass
    if activeperson.status                  >= 20:
        return render(request, 'users/list.html', {'users': users, 'activeperson.status': activeperson.status})    # should always go here
    else:
        pass
    '''

@login_required
def user_process(request, pk='0', function="update"):

  activeuser                 =  User.objects.get(id=request.user.id)    # get details of activeuser
  activeperson               =  Person.objects.get(username=activeuser.username)
  if function                in ['detail', 'update', 'deleteperm']:
    person                   =  get_object_or_404(Person, pk=pk)     # get details of person to be updated/displayed/deleted
    user                     =  User.objects.get(username=person.username)
    if activeperson.status                >= 60                              \
    or person.authorname                  == activeperson.username:
      can_process_this_user               = True 
    else:
      can_process_this_user               = False    
    '''
    error_message                             = 'not found'
    try:  
      user                                    =  User.objects.get(username=person.username)
      error_message                           = user.username
    except:
      return render(request, 'users/user_detail.html', {'error_message': error_message })  
    '''



  '''
  activeperson.status        = 10    
  try:
    activeperson             =  Person.objects.get(username=activeuser.username)
    activeperson.status      =  activeperson.status               # should always go here
  except:
    pass
  '''


  if request.method                           != "POST": # i.e. have arrived here from 'usersinsert_update.html', request.method == "GET":
    if function                               == 'deleteperm':
      user.delete()
      return redirect('users.views.user_list')                                          # give to activeuser list of users
    elif function                             == 'detail':
      return render(request, 'users/user_detail.html', {'person': person, 'can_process_this_user': can_process_this_user})         
      # give to activeuser person info, and offer them buttons
    elif function                             == 'insert':
      form = PersonForm()                                                                 # get a blank PersonForm
      return render(request, 'users/insert_update.html', {'form': form})                # ask activeuser for details of new/updated user
    else:                                     # i.e. function == 'update'
      form = PersonForm(instance=person)                                # get a personForm filled with details of Profile to be upd
      return render(request, 'users/insert_update.html', {'form': form})                # ask activeuser for details of new/updated user
  else:                  # i.e method == 'POST'
    if function          == 'insert':
      form               = PersonForm(request.POST)                        # get a PersonForm filled with details of new user 
      stored_status      = 0
    else:                # i.e. function == 'update'.
      form               = PersonForm(request.POST, instance=person)      # get a PersonForm filled with details of updated user
      stored_status      = person.status    
                                            
    if form.is_valid():
      person                     = form.save(commit=False)                 # extract details from user form





      can_process_this_user                   = False
      if function                             == 'insert':
        if activeperson.status                >= 40:
          user = User.objects.create_user(person.username, 'a@a.com', person.password)  # create user record from form
          can_process_this_user               = True   
      elif function                           == 'update':
        if activeperson.status                >= 60                              \
        or person.authorname                  == activeperson.username:
          user.username                       = person.username
          #user.email                          = person.email
          user.save()
          can_process_this_user               = True   
      if can_process_this_user                == True:
        if                                                                       \
        activeperson.status                   <  60                              \
        and person.status                     >= 40                              \
        or                                                                       \
        activeperson.status                   <  50                              \
        and person.status                     == 10                              \
        and stored_status                     > 10                               \
        or                                                                       \
        activeperson.status                   <  50                              \
        and person.status                     < 10                               \
        and stored_status                     == 10:
          person.status                       = stored_status 
        person.authorname                     = activeperson.username
        person.password                       = 'password'   
        person.save()                                                                   # update user record with extra details
        form.save_m2m()
        return redirect('users.views.user_list')
      else:                                 # i.e. activeuser is not authorized to insert/update user
        return render(request, 'users/insert_update.html', {'form': form})         
        
    else:                                                                        # i.e. form is not valid, ask activeuser to resubmit it
      return render(request, 'users/insert_update.html', {'form': form})



