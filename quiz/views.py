from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

def index(request):
    if request.user.is_authenticated:
        return redirect('select')
    return render(request, 'index.html')

@login_required
def select(request):
    return render(request, 'select.html')




