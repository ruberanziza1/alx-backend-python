from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth.models import User


@login_required
def delete_user(request):
    user = request.user
    logout(request)  # log them out first
    user.delete()
    return redirect("home")  # redirect to home page or login page
