from django import forms
from django.db import models
file_value =''

class UploadFileForm(forms.Form):
    file = forms.FileField()
    CHOICES = [('1', 'Public'), ('2', 'Private')]   
    access_level = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES)
    #name = forms.TextInput(attrs={'size': 10, 'title': 'Your name'})
        

class MakeDirForm(forms.Form):
    name = forms.CharField(max_length=300)
    CHOICES = [('1', 'Public'), ('2', 'Private')]   
    access_level = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES)

class MakeFileForm(forms.Form):
    global file_value
    name = forms.CharField(max_length=300)
    print("Input field for text")
    #file_str = readfromglobal()
    #file_value=self.returnValue()
    content = forms.CharField(widget=forms.Textarea, required=False)
    #content = models.CharField(default='abc')
    CHOICES_lvl = [('1', 'Public'), ('2', 'Private')]   
    access_level = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES_lvl)

    def returnValue(self):
        return 'temp'

def file_value(kb):
    global file_value
    print('Modifying file value'+kb)
    file_value=kb

class editFileForm(forms.Form):
    #name = forms.CharField(max_length=300)
    #print("Input field for text")
    #file_str = readfromglobal()
    #file_value=self.returnValue()
    
    lines ='Error'
    with open('C:\\Users\jeffe\\Projects\\ComputerSecurity\\CMSC-626-project\\DAlphaFS\\DAlphaFS\\readme.txt') as f:
        lines = f.read()
        
    print('lines are'+lines)
    #name = forms.TextInput(attrs={'size': 10, 'title': 'Your name'})
    #name.render('name', 'A name')
    #content = forms.CharField(widget=forms.Textarea, required=False,initial=lines)
    content = forms.CharField(widget=forms.Textarea(attrs={'autocomplete':'off'}))
    #content = forms.CharField(widget=forms.Textarea(attrs={'autocomplete':'off'}))

class ModifyPermissionForm(forms.Form):
    #
    #forms.CharField(label=file_path,disabled=True)
    CHOICES_lvl = [('1', 'Public'), ('2', 'Private')]   
    access_level = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES_lvl)
    

class renameForm(forms.Form):
    new_name = forms.CharField(max_length=300)

class messageForm(forms.Form):
    msg_key = forms.CharField(max_length=300)
    #pass

