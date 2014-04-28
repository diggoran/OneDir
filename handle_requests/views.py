from django.shortcuts import render, get_object_or_404, render_to_response
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from filetransfers.api import prepare_upload, serve_file
from handle_requests.forms import UploadForm
from handle_requests.models import UploadModel
from django.contrib.auth import authenticate, login
from django.template import RequestContext
import os

@csrf_exempt
def upload_handler(request):
    view_url = reverse('handle_requests.views.upload_handler')
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(view_url)
    upload_url, upload_data = prepare_upload(request, view_url)
    form = UploadForm()
    return render(request, 'handle_requests/upload.html',
                  {'form': form, 'upload_url': upload_url, 'upload_data': upload_data})


def download_handler(request, file):
    uploads = UploadModel.objects.filter(file=file)
    return serve_file(request, uploads[0].file, save_as=True)


def delete_handler(request, pk):
    if request.method == 'POST':
        upload = get_object_or_404(UploadForm, pk=pk)
        upload.file.delete()
        upload.delete()
    return HttpResponseRedirect(reverse('upload.views.upload_handler'))


@csrf_exempt
def login_handler(request):
    context = RequestContext(request)
    username = request.POST['username']
    password = request.POST['password']
    print username + ", " + password
    user = authenticate(username=username, password=password)
    status="None"
    if user is not None:
        if user.is_active:
            print "Active User"
            login(request, user)
            status = "success"
            # Redirect to a success page.
        else:
            status = "failure"
    else:
        status = "failure"
    print status
    return render_to_response('login_result.html', {'status': status}, context)
