from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from filetransfers.api import prepare_upload, serve_file
from handle_requests.forms import UploadForm
from handle_requests.models import UploadModel
from django.contrib.auth import authenticate, login


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


def download_handler(request, pk):
    # upload = get_object_or_404(UploadModel, pk=pk)
    upload = UploadModel.objects.filter(pk=pk)[0]
    return serve_file(request, upload.file, save_as=True)


def delete_handler(request, pk):
    if request.method == 'POST':
        upload = get_object_or_404(UploadForm, pk=pk)
        upload.file.delete()
        upload.delete()
    return HttpResponseRedirect(reverse('upload.views.upload_handler'))


@csrf_exempt
def login_handler(request):
    username = request.POST['username']
    password = request.POST['password']
    print username + ", " + password
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            print "Active User"
            login(request, user)
            print "Logged In"
            # Redirect to a success page.
        else:
            print "Disabled Account"
    else:
        print "Invalid Login"
    return HttpResponseRedirect(reverse('upload.views.upload_handler'))
