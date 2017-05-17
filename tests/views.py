from django.shortcuts import render


def simple_view(request):
    return render(request, 'page.html')
