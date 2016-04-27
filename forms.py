from django import forms
from .models import Circle, Person, Event
from django.forms.widgets import CheckboxSelectMultiple

class CircleForm(forms.ModelForm):
    class Meta:
        model = Circle
        fields = ('full_name',)
class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ('full_name', 'second_name', 'name_in_meetup', 'name_in_twitter', 'email', 'phone_a', 'phone_b', 'phone_c', 'circles', 'notes')
    def __init__(self, *args, **kwargs):
        super(PersonForm, self).__init__(*args, **kwargs)
        self.fields["circles"].widget = CheckboxSelectMultiple()
        self.fields["circles"].queryset = Circle.objects.all()
class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ('event_date', 'reference', 'persons', 'notes')
    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        self.fields["persons"].widget = CheckboxSelectMultiple()
        self.fields["persons"].queryset = Person.objects.all()


