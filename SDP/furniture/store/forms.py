from django import forms

# Create your forms here.

class ContactForm(forms.Form):
	name = forms.CharField(max_length = 50)
	phone_number = forms.CharField(max_length = 50)
	email_address = forms.EmailField(max_length = 150)
	height = forms.CharField(max_length = 50)
	width = forms.CharField(max_length = 50)
	depth = forms.CharField(max_length = 50)
	material = forms.CharField(max_length = 50)
	color = forms.CharField(max_length = 50)
	message = forms.CharField(widget = forms.Textarea, max_length = 2000)