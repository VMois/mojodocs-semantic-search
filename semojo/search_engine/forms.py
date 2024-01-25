from django import forms


class QueryForm(forms.Form):
    template_name = 'search_form.html'
    content = forms.CharField(label='Content', max_length=100)
