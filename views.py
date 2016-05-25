from django.shortcuts               import render, get_object_or_404, redirect
from django.utils                   import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models     import User
from .models                        import Circle,     Person,      Event
from .forms                         import CircleForm, PersonForm,  EventForm

from decimal import *
getcontext()
Context(prec=28, rounding=ROUND_HALF_EVEN, Emin=-999999, Emax=999999,
        capitals=1, flags=[], traps=[Overflow, DivisionByZero,
        InvalidOperation])
getcontext().prec = 4

@login_required
def circle_list(request):
  circles = Circle.objects.all().order_by('full_name')
  return render(request, 'diaryandcontacts/circle_list.html', {'circles': circles})

@login_required
def circle_process(request, function="update", pk='0'):
  if function                                 == 'insert':
    pass
  else:
    circle                                     = get_object_or_404(Circle, pk=pk)
                                              # i.e. function in ['detail', 'update', 'repeat', 'deleteperm']

  if request.method                           == "POST":                # i.e. have arrived here from 'diaryandcontacts/circle_input_form.html'

    if function                               in ['insert', 'repeat']:
      form                                    = CircleForm(request.POST)
    else:
      form                                    = CircleForm(request.POST, instance=circle)
                                              # i.e. function == 'update'
                                              # function in ['detail', 'deleteperm'] don't go here

    if form.is_valid():
      circle                                   = form.save(commit=False)

      user                                    = User.objects.get(id=request.user.id)

      circle.author_name                     = user.username
      circle.author                          = user

      circle.save()
      form.save_m2m()


      return redirect('diaryandcontacts.views.circle_list')

    else:                                                                                  # i.e. form is not valid, ask user to resubmit it
      return render(request, 'diaryandcontacts/circle_input_form.html', {'form': form})

  else:                                                                                    # i.e. request.method == "GET":
    if function                               == 'insert':
      form = CircleForm()
      return render(request, 'diaryandcontacts/circle_input_form.html', {'form': form})
    elif function                             == 'deleteperm':
      circle.delete()
      return redirect('diaryandcontacts.views.circle_list')
    elif function                             == 'detail':
      return render(request, 'diaryandcontacts/circle_detail.html', {'circle': circle})
                                                                                            # no data input, just buttons
    else:                                                                               # i.e. function in ['update','repeat']
      form = CircleForm(instance=circle)
      return render(request, 'diaryandcontacts/circle_input_form.html', {'form': form})                   # ask user for circle details

@login_required
def person_list(request):
  persons = Person.objects.all().order_by('second_name')
  return render(request, 'diaryandcontacts/person_list.html', {'persons': persons})

@login_required
def person_process(request, function="update", pk='0'):
  if function                                 == 'insert':
    pass
  else:
    person                                    = get_object_or_404(Person, pk=pk)
                                              # i.e. function in ['detail', 'update', 'repeat', 'deleteperm']
  if request.method                           != "POST":                                   # i.e. request.method == "GET":

    if function                               == 'insert':
      form = PersonForm()
      return render(request, 'diaryandcontacts/person_input_form.html', {'form': form})
    elif function                           == 'deleteperm':
      person.delete()
      return redirect('diaryandcontacts.views.person_list')
    elif function                           == 'detail':
      circles_list = []
      for circle in person.circles.all():
        circles_list.append(circle.full_name)
      circles_string   = ', '.join(circles_list)
      return render(request, 'diaryandcontacts/person_detail.html', {'person': person, 'circles':circles_string})
                                                                                            # no data input, just buttons
    else:                                                                               # i.e. function in ['update','repeat']
      form = PersonForm(instance=person)
      return render(request, 'diaryandcontacts/person_input_form.html', {'form': form})                   # ask user for person details
  else:                                                                                    # i.e. request.method == "POST":

    if function                               in ['insert', 'repeat']:
      form                                    = PersonForm(request.POST)
    else:
      form                                    = PersonForm(request.POST, instance=person)
                                              # i.e. function == 'update'
                                              # function in ['detail', 'deleteperm'] don't go here

    if form.is_valid():
      person                                  = form.save(commit=False)

      user                                    = User.objects.get(id=request.user.id)

      person.author_name                      = user.username
      person.author                           = user

      person.save()
      form.save_m2m()

      return redirect('diaryandcontacts.views.person_list')

    else:                                                                                  # i.e. form is not valid, ask user to resubmit it
      return render(request, 'diaryandcontacts/person_input_form.html', {'form': form})






def event_list(request, periodsought='current'):
  stored_event_date = '2000-01-01'
  if periodsought == 'current':
    events = Event.objects.filter(is_live=True,event_date__gte=timezone.now()).order_by('event_date')
  else:
    events = Event.objects.exclude(is_live=True,event_date__gte=timezone.now()).order_by('-event_date')
  for event in events:
    current_event_date = event.event_date
    if event.event_date == stored_event_date:
      event.event_date = ''
    stored_event_date = current_event_date

  return render(request, 'diaryandcontacts/event_list.html', {'events': events, 'periodsought': periodsought})

def events_hardcoded(request):
  return render(request, 'diaryandcontacts/events_hardcoded.html', {})

@login_required
def event_process(request, function="update", pk='0'):
  if function                                 == 'insert':
    pass
  else:
    event                                     = get_object_or_404(Event, pk=pk)
                                              # i.e. function in ['detail', 'update', 'repeat',
                                              #'restore', 'bookinto', 'leave', 'delete', 'deleteperm']

  if request.method                           != "POST":                # i.e. request.method == "GET":
    if function                               == 'insert':
      form = EventForm()
      return render(request, 'diaryandcontacts/event_input_form.html', {'form': form})
      # ask user for event details
    else:
      # decide which period of events to display afterwards
      if event.event_date                     <  timezone.localtime(timezone.now()).date():
        periodsought                          =  'notcurrent'
        event_status_now                      =  'past'
      elif event.is_live                      == False:
        periodsought                          =  'notcurrent'
        event_status_now                      =  'deletednonpast'
      else:
        periodsought                          =  'current'
        event_status_now                      =  'live'



      if function                             == 'deletetemp':
        event.is_live                         =  False
        event.save()
        return redirect('diaryandcontacts.views.event_list', periodsought)
      elif function                           == 'deleteperm':
        event.delete()
        return redirect('diaryandcontacts.views.event_list', periodsought)
      elif function                           == 'bookinto':
        updated_attendee = User.objects.get(username = request.user)
        event.attendees.add(updated_attendee)
        event.save()
        return redirect('diaryandcontacts.views.event_list', periodsought)
      elif function                           == 'leave':
        updated_attendee = User.objects.get(username = request.user)
        event.attendees.remove(updated_attendee)
        event.save()
        return redirect('diaryandcontacts.views.event_list', periodsought)
      elif function                           == 'restore':
        event.is_live                         = True
        event.save()
        periodsought                          = 'current'
        return redirect('diaryandcontacts.views.event_list', periodsought)
      elif function                           == 'detail':
        persons_list = []
        for person in event.persons.all():
            persons_list.append(person.full_name)
        persons_string   = ', '.join(persons_list)
        return render(request, 'diaryandcontacts/event_detail.html', {'event': event, 'event_status_now': event_status_now, 'persons':persons_string})
                                                                                            # no data input, just buttons
      else:                                                                               # i.e. function in ['update','repeat']
        form = EventForm(instance=event)
        return render(request, 'diaryandcontacts/event_input_form.html', {'form': form})                   # ask user for event details

  else:                                                                   # i.e. request.method == "POST":                 
    if function                               in ['insert', 'repeat']:
      form                                    = EventForm(request.POST)
    else:
      form                                    = EventForm(request.POST, instance=event)
                                              # i.e. function == 'update'
                                              # function in ['detail', 'restore','bookinto', 'leave', 'delete', 'deleteperm'] don't go here

    if form.is_valid():
      event                                   = form.save(commit=False)

      if event.event_date                     < timezone.localtime(timezone.now()).date():
        periodsought                          = 'notcurrent'
      else:
        periodsought                          = 'current'

      user                                    = User.objects.get(id=request.user.id)

      event.author_name                     = user.username
      event.author                          = user

      event.save()
      form.save_m2m()

      return redirect('diaryandcontacts.views.event_list', periodsought)

    else:                                                                                  # i.e. form is not valid, ask user to resubmit it
      return render(request, 'diaryandcontacts/event_input_form.html', {'form': form})












@login_required
def contact_list(request):
  contacts = Person.objects.all().order_by('second_name')
  return render(request, 'diaryandcontacts/contact_list.html', {'contacts': contacts})

@login_required
def contact_process(request, function="update", pk='0'):
  if function                                 == 'insert':
    pass
  else:
    contact                                    = get_object_or_404(Person, pk=pk)
                                              # i.e. function in ['detail', 'update', 'repeat', 'deleteperm']
  if request.method                           == "POST":                # i.e. have arrived here from 'diaryandcontacts/contact_input_form.html'

    if function                               in ['insert', 'repeat']:
      form                                    = PersonForm(request.POST)
    else:
      form                                    = PersonForm(request.POST, instance=contact)
                                              # i.e. function == 'update'
                                              # function in ['detail', 'deleteperm'] don't go here

    if form.is_valid():
      contact                                  = form.save(commit=False)

      user                                    = User.objects.get(id=request.user.id)

      contact.author_name                      = user.username
      contact.author                           = user

      contact.save()
      form.save_m2m()

      return redirect('diaryandcontacts.views.contact_list')

    else:                                                                                  # i.e. form is not valid, ask user to resubmit it
      return render(request, 'diaryandcontacts/contact_input_form.html', {'form': form})

  else:                                                                                    # i.e. request.method == "GET":
    if function                               == 'insert':
      form = PersonForm()
      return render(request, 'diaryandcontacts/contact_input_form.html', {'form': form})
    elif function                           == 'deleteperm':
      contact.delete()
      return redirect('diaryandcontacts.views.contact_list')
    elif function                           == 'detail':
      circles_list = []
      for circle in person.circles.all():
        circles_list.append(circle.full_name)
      circles_string   = ', '.join(circles_list)
      return render(request, 'diaryandcontacts/contact_detail.html', {'contact': contact, 'circles':circles_string})
                                                                                            # no data input, just buttons
    else:                                                                               # i.e. function in ['update','repeat']
      form = PersonForm(instance=contact)
      return render(request, 'diaryandcontacts/contact_input_form.html', {'form': form})                   # ask user for contact details

def event_list(request, periodsought='current'):
  stored_event_date = '2000-01-01'
  if periodsought == 'current':
    events = Event.objects.filter(is_live=True,event_date__gte=timezone.now()).order_by('event_date')
  else:
    events = Event.objects.exclude(is_live=True,event_date__gte=timezone.now()).order_by('-event_date')
  for event in events:
    current_event_date = event.event_date
    if event.event_date == stored_event_date:
      event.event_date = ''
    stored_event_date = current_event_date

  return render(request, 'diaryandcontacts/event_list.html', {'events': events, 'periodsought': periodsought})

def events_hardcoded(request):
  return render(request, 'diaryandcontacts/events_hardcoded.html', {})

@login_required
def event_process(request, function="update", pk='0'):
  if function                                 == 'insert':
    pass
  else:
    event                                     = get_object_or_404(Event, pk=pk)
                                              # i.e. function in ['detail', 'update', 'repeat',
                                              #'restore', 'bookinto', 'leave', 'delete', 'deleteperm']

  if request.method                           == "POST":                # i.e. have arrived here from 'diaryandcontacts/event_input_form.html'

    if function                               in ['insert', 'repeat']:
      form                                    = EventForm(request.POST)
    else:
      form                                    = EventForm(request.POST, instance=event)
                                              # i.e. function == 'update'
                                              # function in ['detail', 'restore','bookinto', 'leave', 'delete', 'deleteperm'] don't go here

    if form.is_valid():
      event                                   = form.save(commit=False)

      if event.event_date                     < timezone.localtime(timezone.now()).date():
        periodsought                          = 'notcurrent'
      else:
        periodsought                          = 'current'

      user                                    = User.objects.get(id=request.user.id)

      event.author_name                     = user.username
      event.author                          = user

      event.save()
      form.save_m2m()

      return redirect('diaryandcontacts.views.event_list', periodsought)

    else:                                                                                  # i.e. form is not valid, ask user to resubmit it
      return render(request, 'diaryandcontacts/event_input_form.html', {'form': form})

  else:                                                                                    # i.e. request.method == "GET":
    if function                               == 'insert':
      form = EventForm()
      return render(request, 'diaryandcontacts/event_input_form.html', {'form': form})
      # ask user for event details
    else:
      # decide which period of events to display afterwards
      if event.event_date                     <  timezone.localtime(timezone.now()).date():
        periodsought                          =  'notcurrent'
        event_status_now                      =  'past'
      elif event.is_live                      == False:
        periodsought                          =  'notcurrent'
        event_status_now                      =  'deletednonpast'
      else:
        periodsought                          =  'current'
        event_status_now                      =  'live'



      if function                             == 'deletetemp':
        event.is_live                         =  False
        event.save()
        return redirect('diaryandcontacts.views.event_list', periodsought)
      elif function                           == 'deleteperm':
        event.delete()
        return redirect('diaryandcontacts.views.event_list', periodsought)
      elif function                           == 'bookinto':
        updated_attendee = User.objects.get(username = request.user)
        event.attendees.add(updated_attendee)
        event.save()
        return redirect('diaryandcontacts.views.event_list', periodsought)
      elif function                           == 'leave':
        updated_attendee = User.objects.get(username = request.user)
        event.attendees.remove(updated_attendee)
        event.save()
        return redirect('diaryandcontacts.views.event_list', periodsought)
      elif function                           == 'restore':
        event.is_live                         = True
        event.save()
        periodsought                          = 'current'
        return redirect('diaryandcontacts.views.event_list', periodsought)
      elif function                           == 'detail':
        contacts_list = []
        for contact in event.persons.all():
            contacts_list.append(contact.full_name)
        contacts_string   = ', '.join(contacts_list)
        return render(request, 'diaryandcontacts/event_detail.html', {'event': event, 'event_status_now': event_status_now, 'contacts':contacts_string})
                                                                                            # no data input, just buttons
      else:                                                                               # i.e. function in ['update','repeat']
        form = EventForm(instance=event)
        return render(request, 'diaryandcontacts/event_input_form.html', {'form': form})                   # ask user for event details




@login_required
def contact_detail(request, pk):

  contact                                    = get_object_or_404(Person, pk=pk)

  circles_list = []
  for circle in person.circles.all():
    circles_list.append(circle.full_name)
  circles_string   = ', '.join(circles_list)
  return render(request, 'diaryandcontacts/contact_detail.html', {'contact': contact, 'circles':circles_string})
                                                                                            # no data input, just buttons
