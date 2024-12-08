from django.contrib.auth import login
from django.http import HttpResponse
from django.shortcuts import render
from crispy_forms.templatetags.crispy_forms_filters import as_crispy_field
from django.shortcuts import redirect
from django.template.context_processors import csrf
from crispy_forms.utils import render_crispy_form


from core.forms import *

# Create your views here.
def index(request):
    if request.method == 'GET':
        context = {'form': UniversityForm()}
        return render(request, 'index.html', context)
    
    elif request.method == 'POST':
        form = UniversityForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            template = render(request, 'profile.html')
            template['Hx-Push'] = '/profile/'
            return template

        ctx = {}
        ctx.update(csrf(request))
        form_html = render_crispy_form(form, context=ctx)
        return HttpResponse(form_html)


def check_username(request):
    form = UniversityForm(request.GET)
    context = {
        'field': as_crispy_field(form['username']),
        'valid': not form['username'].errors
    }
    return render(request, 'partials/field.html', context)

def check_subject(request):
    form = UniversityForm(request.GET)
    context = {
        'field': as_crispy_field(form['subject']),
        'valid': not form['subject'].errors
    }
    return render(request, 'partials/field.html', context)
def example_form(request):
    if request.method == 'GET':
        context = {'form': ExampleForm()}
        return render(request, 'form/exampleform.html', context)
    elif request.method == 'POST':
        form = ExampleForm(request.POST or None)
        if form.is_valid():
            # You could actually save through AJAX and return a success code here
            form.save()
            return redirect('index')
        ctx = {}
        ctx.update(csrf(request))
        form_html = render_crispy_form(form, context=ctx)
        return render(request,'form/exampleform.html',{'form':form}); # {'success': False, 'form_html': form_html}


def contact(request):
    if request.method == 'GET':
        form = ContactForm()
        context = {'form' : form }
        return render(request,'form/baseform.html',context)