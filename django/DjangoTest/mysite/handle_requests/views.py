from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def derp(request):
    if request.method == 'POST':
        print request.body
    return render(request, 'handle_requests/derp.html')
