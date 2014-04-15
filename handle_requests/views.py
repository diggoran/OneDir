from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from filetransfers.api import prepare_upload
from handle_requests.forms import UploadForm


@csrf_exempt
def derp(request):
    # print "Hello"
    view_url = reverse('handle_requests.views.derp')
    if request.method == 'POST':
        # print "Hello!"

        # post = request.POST.copy()
        # print post
        # temp = post['key2']
        # print "2"
        # post['key2'] = temp.strip('<ul>')
        # print "3"
        print request.POST
        print request.FILES
        form = UploadForm(request.POST, request.FILES)
        # print form
        # print form.Meta.__dict__
        # form = UploadForm(str(form).replace('<ul class="errorlist"><li>This field is required.</li></ul>', '', 1))
        # print "Hello?"
        print form
        print form.Meta.__dict__
        form.save()
        # print "Hello!"
        return HttpResponseRedirect(view_url)
    # print "Hello"
    upload_url, upload_data = prepare_upload(request, view_url)
    # print "Hello!"
    form = UploadForm()
    # print "Hello!!!"
    return render(request, 'handle_requests/upload.html',
        {'form': form, 'upload_url': upload_url, 'upload_data': upload_data})


# @csrf_exempt
# def derp(request):
#     if request.method == 'POST':
#         # print request.body
#         # print request.POST
#         # form = DocumentForm(request.POST, request.FILES)
#         # print "Hello"
#         # if form.is_valid():
#         print "Hello?"
#         newdoc = Document(docfile = request.FILES['docfile'])
#         print "Hello!"
#         print newdoc
#             # newdoc.save()
#     return render(request, 'handle_requests/derp.html')