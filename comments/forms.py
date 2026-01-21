from django import forms

class CommentForm(forms.Form):
    content_type = forms.IntegerField(widget=forms.HiddenInput)
    object_id = forms.IntegerField(widget=forms.HiddenInput)
    content = forms.CharField(label='', widget=forms.Textarea)