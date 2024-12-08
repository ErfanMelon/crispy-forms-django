from django import forms
from datetime import datetime
from django.urls import reverse_lazy
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from .models import User 

class MyBaseForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title = self.__class__.__name__
        self.description = self.__class__.__doc__
    def getTitle(self):
        return self.__class__.__name__
    def getDescription(self):
        return self.__class__.__doc__
class UniversityForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        # self.helper.form_action = reverse_lazy('index')
        # self.helper.form_method = 'POST'
        self.helper.form_id = 'university-form'
        self.helper.attrs = {
            'hx-post': reverse_lazy('index'),
            'hx-target': '#university-form',
            'hx-swap': 'outerHTML'
        }
        self.helper.add_input(Submit('submit', 'Submit'))
    
    subject = forms.ChoiceField(
        choices=User.Subjects.choices,
        widget=forms.Select(attrs={
            'hx-get': reverse_lazy('check-subject'),
            'hx-target': '#div_id_subject',
            'hx-trigger': 'change'
        })
    )
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'max': datetime.now().date()}))

    class Meta:
        model = User
        fields = ('username', 'password', 'date_of_birth', 'subject')
        widgets = {
            'password': forms.PasswordInput(),
            'username': forms.TextInput(attrs={
                'hx-get': reverse_lazy('check-username'),
                'hx-target': '#div_id_username',
                'hx-trigger': 'keyup[target.value.length > 3]'
            })
        }

    def clean_username(self):
        username = self.cleaned_data['username']
        if len(username) <= 3:
            raise forms.ValidationError("Username is too short")
        return username

    def clean_subject(self):
        subject = self.cleaned_data['subject']
        if User.objects.filter(subject=subject).count() > 3:
            raise forms.ValidationError("There are no spaces on this course")
        return subject


    def save(self, commit=True):
        """ Hash user's password on save """
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

class ExampleForm(MyBaseForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-exampleForm'
        self.helper.form_class = 'form'
        self.helper.form_method = 'post'
        self.helper.form_action = 'example'

        self.helper.add_input(Submit('submit', 'Submit'))

    like_website = forms.TypedChoiceField(
        label = "Do you like this website?",
        choices = ((1, "Yes"), (0, "No")),
        coerce = lambda x: bool(int(x)),
        widget = forms.RadioSelect,
        initial = '1',
        required = True,
    )

    favorite_food = forms.CharField(
        label = "What is your favorite food?",
        max_length = 80,
        required = True,
    )

    favorite_color = forms.CharField(
        label = "What is your favorite color?",
        max_length = 80,
        required = True,
    )

    favorite_number = forms.IntegerField(
        label = "Favorite number",
        required = False,
    )

    notes = forms.CharField(
        label = "Additional notes or feedback",
        required = False,
    )
    def save(self):
        print(self.cleaned_data);

class ContactForm(MyBaseForm):
    """This form used to collect customer info which used to contact them !"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()

    name = forms.CharField(
        max_length=100,
        label="Your Name",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your name'})
    )
    email = forms.EmailField(
        label="Your Email",
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'})
    )
    message = forms.CharField(
        label="Your Message",
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Type your message'})
    )