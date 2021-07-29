from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect


@login_required
def index(request):
    if request.user:
        id = request.user.id
        return redirect(f'/user/{id}')
