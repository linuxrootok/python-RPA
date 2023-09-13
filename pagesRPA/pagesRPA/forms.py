from django.contrib import admin
from django.forms import widgets
from django.forms import TextInput, Select
from django.db import models

from django import forms
from django_admin_json_editor import JSONEditorWidget

from django.views.generic.edit import CreateView, UpdateView
#from django_json_widget.widgets import JSONInput, JSONTextarea


# 自定义 Widget
class XPathWidget(widgets.MultiWidget):
    def __init__(self, attrs=None):
        super().__init__([
            TextInput(attrs=attrs),
            Select(attrs=attrs, choices=[('and', 'and'), ('or', 'or')]),
            TextInput(attrs=attrs),
        ])
    
    def decompress(self, value):
        if value:
            return value.split(' ')
        return ['', '', '']
    
    def format_output(self, rendered_widgets):
        return '<div class="xpath-group">{}</div>'.format(''.join(rendered_widgets))



class MyForm(forms.Form):
    value = forms.IntegerField()


