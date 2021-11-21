from django import forms


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
    name = forms.CharField(max_length=300)
    content = forms.CharField(widget=forms.Textarea, required=False)
    CHOICES_lvl = [('1', 'Public'), ('2', 'Private')]   
    access_level = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES_lvl)

class ModifyPermissionForm(forms.Form):
    #
    #forms.CharField(label=file_path,disabled=True)
    CHOICES_lvl = [('1', 'Public'), ('2', 'Private')]   
    access_level = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES_lvl)
    

