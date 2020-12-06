from django import forms
from .models import Topic
from .models import Entry

class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ["text"]
        labels = {"text":""}


class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ["text"]
        labels = {"text":""}
        # A widget is an HTML element, such as a single-line text box,
        # multi-line text area, or drop-down list.
        # customize the nput widget for the field "text" so the text area
        # will be 80 columns wide instead of the default 40
        widgets = {"text": forms.Textarea(attrs = {"cols": 80})}

