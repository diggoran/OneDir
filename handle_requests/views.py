from django.shortcuts import render, get_object_or_404, render_to_response
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from filetransfers.api import prepare_upload, serve_file
from handle_requests.forms import UploadForm
from handle_requests.models import UploadModel
from django.contrib.auth import authenticate, login, logout
from onedir_app.models import Connection, Modification, File
from django.template import RequestContext
import os
from rest_framework.authtoken.models import Token
import json
from django.http import HttpResponse
from django.conf import settings

def check_auth(username, password, request):
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            return user.id
    return -1

@csrf_exempt
def upload_handler(request):
    context = RequestContext(request)
    view_url = reverse('handle_requests.views.upload_handler')
    print view_url
    username = request.POST['username']
    password = request.POST['password']
    file_name = request.POST['file_name']
    size = request.POST['size']
    path = request.POST['path']
    user_id = check_auth(username, password, request)
    print "USER ID: " + str(user_id)
    if(user_id!=-1):
        if request.method == 'POST':
            form = UploadForm(request.POST, request.FILES)
            print request.FILES
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(view_url)
            else:
                print "Invalid"
        upload_url, upload_data = prepare_upload(request, view_url)
        print upload_url
        print upload_data
        form = UploadForm()
        file_object = File(name=file_name, path = path, user_id = user_id, size=size )
        file_object.save()
        print file_object
        mod = Modification(file_id = file_object.pk, user_id = user_id, mod_type='add')
        mod.save()
        print mod
        return render(request, 'handle_requests/upload.html',
                      {'form': form, 'upload_url': upload_url, 'upload_data': upload_data})
    else:
        return render(request, 'status.html', {'status': 'failure'})


def download_handler(request, file):
    uploads = UploadModel.objects.filter(file=file)
    return serve_file(request, uploads[0].file, save_as=True)

@csrf_exempt
def delete_handler(request):
    context = RequestContext(request)
    username = request.POST['user_name']
    password = request.POST['password']
    path = request.POST['path']
    file_name = request.POST['file_name']
    user_id = check_auth(username, password, request)
    full_file_path = username + '/' + path + '/' + file_name
    #full_file_path = 'tba5jb/derp/something.txt'
    print "USER ID: " + str(user_id)
    if(user_id!=-1):
        if request.method == 'POST':
            #upload = get_object_or_404(UploadForm, file=full_file_path )
            #upload.file.delete()
            #upload.delete()
            print file_name
            print path
            os.remove(os.path.join(settings.MEDIA_ROOT, full_file_path))
            file_object = File.objects.filter(name = file_name, path = path)[0]
            file_pk = file_object.pk
            file_object.delete()
            mod = Modification(file_id = file_pk, user_id = user_id, mod_type='delete' )
            mod.save()
        return render(request, 'status.html', {'status': 'success'})
    else:
        return render(request, 'status.html', {'status': 'failure'})


@csrf_exempt
def login_handler(request):
    context = RequestContext(request)
    username = request.POST['username']
    password = request.POST['password']
    print username + ", " + password
    user = authenticate(username=username, password=password)
    status="None"
    key1 = ""
    if user is not None:
        if user.is_active:
            print "Active User"
            login(request, user)
            status = "success"
            print request.user.is_authenticated()
            # token = Token.objects.get(user=user)
            # print token.key
            # key1=token.key
            cxn = Connection(user_id=user.id)
            cxn.save()
            # Redirect to a success page.
        else:
            status = "failure"
    else:
        status = "failure"
    print status
    print get_client_ip(request)
    #print request.META['HTTP_X_FORWARDED_FOR']
    return render_to_response('login_result.html', {'status': status, 'token': key1}, context)

@csrf_exempt
def logout_handler(request):
    context = RequestContext(request)
    #print request.auth
    print request.user
    if request.user.is_authenticated():
        logout(request)
        status= "success"
    else:
        status= "no login"
    return render_to_response('logout_result.html', context)

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
        print "In here"
    else:
        ip = request.META.get('REMOTE_ADDR')
        print "In else"  
    return ip

@csrf_exempt
def latest_changes(request):
    #timestamp = request.POST['timestamp']
    #latest_mods = Modification.objects.filter(time_stamp__gte=timestamp, user_id = 1)
    file_objects = File.objects.filter(user_id=1)
    file_paths = []
    username = "admin"
    for f in file_objects:
        file_paths.append(str(f.path + '/' + f.name))
    print file_paths
    response_data = {}
    response_data['files'] = file_paths
    return HttpResponse(json.dumps(response_data), content_type="application/json")
