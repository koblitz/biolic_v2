from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.shortcuts import render_to_response,render
from django.template import RequestContext
from usuarios.forms import RegistrationForm
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import login
from django.core.urlresolvers import reverse
from django.contrib.auth import login,logout
def outlog(request):
	logout(request)
	return render_to_response('index.html')
def logar(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST) # Veja a documentacao desta funcao
        if form.is_valid():
            login(request, form.get_user());user=request.user
            return render_to_response("inicio.html",{'user':user})
        else:
            return render_to_response("pecaadm.html")
    return render(request,"logar.html", {"form": AuthenticationForm()})

