from .form import RegistrationForm
from django.shortcuts import render,redirect
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from django.views import View
  


class RegistrationView(View):
	def get(self, request):
		form = RegistrationForm()
		return render(request, 'register.html', {'form':form})

	def post(self, request):
		form = RegistrationForm(request.POST)
		if form.is_valid():
			print("Valid form")
			messages.success(request, "Registration successful")
			form.save()
		return render(request, 'register.html', {'form': form})




def aboutus(request):
    return render(request, 'aboutus.html')

def contact(request):
    return render(request,'contact.html')