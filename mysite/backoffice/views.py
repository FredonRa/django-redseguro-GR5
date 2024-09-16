from django.shortcuts import render

# Create your views here.
def crud(req):
    return render(req, 'crud.admin.html')