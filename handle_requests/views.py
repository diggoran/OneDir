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
from django.contrib.auth.models import User


def check_auth(username, password, request):
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            return user.id
    return -1


@csrf_exempt
def upload_handler(request):
    view_url = reverse('handle_requests.views.upload_handler')
    # print view_url
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user_id = check_auth(username, password, request)
        # print "USER ID: " + str(user_id)
        if user_id is not -1:
            file_name = request.POST['file_name']
            size = request.POST['size']
            path = request.POST['path']
            form = UploadForm(request.POST, request.FILES)
            # print request.FILES
            # print request.POST
            form.save()
            file_object = File(name=file_name, path = path, user_id = user_id, size=size )
            file_object.save()
            mod = Modification(file_id = file_object.pk, user_id = user_id, mod_type='add')
            mod.save()
            return render(request, 'status.html', {'status': 'upload successful'})
        else:
            return render(request, 'status.html', {'status': 'login failure'})
    form = UploadForm()
    upload_url, upload_data = prepare_upload(request, view_url)
    # print upload_url
    # print upload_data
    return render(request, 'handle_requests/upload.html',
                  {'form': form, 'upload_url': upload_url, 'upload_data': upload_data})


def download_handler(request, username_path_file):
    if username_path_file.count('/') is 1:
        username_path_file = username_path_file.replace('/', '/./')
    uploads = UploadModel.objects.filter(file=username_path_file)
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
    # print "USER ID: " + str(user_id)
    if user_id is not -1:
        if request.method == 'POST':
            #upload = get_object_or_404(UploadForm, file=full_file_path )
            #upload.file.delete()
            #upload.delete()
            # print file_name
            # print path
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
def add_dir_handler(request):
    context = RequestContext(request)
    username = request.POST['username']
    password = request.POST['password']
    path = request.POST['path']
    filename = request.POST['file_name']
    user_id = check_auth(username, password, request)
    full_file_path = os.path.join(username, path, filename)
    #full_file_path = 'tba5jb/derp/something.txt'
    # print "USER ID: " + str(user_id)
    if user_id is not -1:
        if request.method == 'POST':
            #upload = get_object_or_404(UploadForm, file=full_file_path )
            #upload.file.delete()
            #upload.delete()
            # print path
            os.mkdir(os.path.join(settings.MEDIA_ROOT, full_file_path))
            mod = Modification(file_id = -1, user_id = user_id, mod_type='add_directory' )
            mod.save()
        return render(request, 'status.html', {'status': 'success'})
    else:
        return render(request, 'status.html', {'status': 'failure'})


@csrf_exempt
def del_dir_handler(request):
    context = RequestContext(request)
    username = request.POST['username']
    password = request.POST['password']
    path = request.POST['path']
    filename = request.POST['file_name']
    user_id = check_auth(username, password, request)
    if path != '':
        full_file_path = username + '/' + path + '/' + filename
    else:
        full_file_path = username + '/' + filename
    #full_file_path = 'tba5jb/derp/something.txt'
    # print "USER ID: " + str(user_id)
    if user_id is not -1:
        if request.method == 'POST':
            #upload = get_object_or_404(UploadForm, file=full_file_path )
            #upload.file.delete()
            #upload.delete()
            # print path
            os.removedirs(os.path.join(settings.MEDIA_ROOT, full_file_path))
            mod = Modification(file_id = -1, user_id = user_id, mod_type='del_directory' )
            mod.save()
        return render(request, 'status.html', {'status': 'success'})
    else:
        return render(request, 'status.html', {'status': 'failure'})


@csrf_exempt
def login_handler(request):
    context = RequestContext(request)
    username = request.POST['username']
    password = request.POST['password']
    # print username + ", " + password
    user = authenticate(username=username, password=password)
    key1 = ''
    status = 'failure'
    if user is not None:
        if user.is_active:
            # print "Active User"
            login(request, user)
            status = 'success'
            # print request.user.is_authenticated()
            if not os.path.isdir(os.path.join(settings.MEDIA_ROOT, username)):
                os.mkdir(os.path.join(settings.MEDIA_ROOT, username))
            # token = Token.objects.get(user=user)
            # print token.key
            # key1=token.key
            cxn = Connection(user_id=user.id)
            cxn.save()
            # Redirect to a success page.
    # print status
    # print get_client_ip(request)
    #print request.META['HTTP_X_FORWARDED_FOR']
    return render_to_response('login_result.html', {'status': status, 'token': key1}, context)


@csrf_exempt
def logout_handler(request):
    context = RequestContext(request)
    #print request.auth
    # print request.user
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
        # print "In here"
    else:
        ip = request.META.get('REMOTE_ADDR')
        # print "In else"
    return ip


@csrf_exempt
def latest_changes(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        #timestamp = request.POST['timestamp']
        user_id = check_auth(username, password, request)
        # print "USER ID: " + str(user_id)
        if user_id is not -1:
            #latest_mods = Modification.objects.filter(user_id=user_id, time_stamp__gte=timestamp)
            file_objects = File.objects.filter(user_id=user_id)#, time_stamp__gte=timestamp)
            file_paths = []
            for f in file_objects:
                if f.path == '.':
                    file_paths.append(f.name)
                else:
                    file_paths.append(os.path.join(f.path, f.name))
            response_data = {'files': file_paths}
            # print json.dumps(response_data)
            return HttpResponse(json.dumps(response_data), content_type="application/json")
        else:
            return render(request, 'status.html', {'status': 'login failure'})
    return render(request, 'index.html')


@csrf_exempt
def pass_change_handler(request):
    username = request.POST['username']
    new_password = request.POST['newpassword']
    user = User.objects.get(username = username)
    user.set_password(new_password)
    user.save()
    # print "PASSWORD:" + user.password
    return render(request, 'status.html', {'status': 'success'})