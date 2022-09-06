import os

from django.contrib.auth.views import LoginView
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.template.loader import render_to_string
from django.template.response import TemplateResponse
from django.utils.encoding import force_bytes
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views import View
from chatApp import settings
from django.core.paginator import Paginator

from django.contrib.auth.decorators import login_required

from .forms import UploadForm, FileModelForm, FileFilterForm, UserRegistrationForm, LoginUserForm, WritehelpForm, \
    WhiteHelpFileForm
from .models import chatMessages, FeedFile, UploadFile, Writehelp, WhiteHelpFile
from django.contrib.auth import get_user_model, login
from django.contrib.auth.models import User as UserModel, User
from django.db.models import Q
import json,datetime
from django.core import serializers
from django.contrib.auth.tokens import default_token_generator as token_generator

# Create your views here.
from .tokens import account_activation_token
from django.core.mail import EmailMessage


@login_required
def home(request):
    User = get_user_model()
    users = User.objects.all()
    chats = {}
    if request.method == 'GET' and 'u' in request.GET:
        # chats = chatMessages.objects.filter(Q(user_from=request.user.id & user_to=request.GET['u']) | Q(user_from=request.GET['u'] & user_to=request.user.id))
        chats = chatMessages.objects.filter(Q(user_from=request.user.id, user_to=request.GET['u']) | Q(user_from=request.GET['u'], user_to=request.user.id))
        chats = chats.order_by('date_created')
    context = {
        "page":"home",
        "users":users,
        "chats":chats,
        "chat_id": int(request.GET['u'] if request.method == 'GET' and 'u' in request.GET else 0)
    }
    print(request.GET['u'] if request.method == 'GET' and 'u' in request.GET else 0)
    return render(request,"chat/home.html",context)

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            # form.save()
            # username = form.cleaned_data.get('username')
            # messages.success(request,f'Account successfully created!')
            # return redirect('chat-login')
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            context = {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            }
            message = render_to_string('chat/registration/activate.html', context=context, )
            mail_subject = 'Activate your blog account.'
            # to_email = form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, message, to=[user.email])
            email.send()
            return redirect('confirm_email.html')

        # context = {
        #     "page":"register",
        #     "form" : form
        # }
    else:
        # context = {
        #     "page":"register",
        #     "form" : UserRegistrationForm()
        # }
        form = UserRegistrationForm()
    return render(request,"chat/registration/register.html", {'form':form})

@login_required
def profile(request):
    context = {
        "page":"profile",
    }
    return render(request,"chat/profile.html",context)

def get_messages(request):
    chats = chatMessages.objects.filter(Q(id__gt=request.POST['last_id']),Q(user_from=request.user.id, user_to=request.POST['chat_id']) | Q(user_from=request.POST['chat_id'], user_to=request.user.id))

    new_msgs = []
    for chat in list(chats):
        data = {}
        data['id'] = chat.id
        data['user_from'] = chat.user_from.id
        data['user_to'] = chat.user_to.id
        data['message'] = chat.message
        data['date_created'] = chat.date_created.strftime("%b-%d-%Y %H:%M")
        print(data)
        new_msgs.append(data)
    return HttpResponse(json.dumps(new_msgs), content_type="application/json")

def send_chat(request):
    resp = {}
    User = get_user_model()
    if request.method == 'POST':
        post =request.POST
        u_from = UserModel.objects.get(id=post['user_from'])
        u_to = UserModel.objects.get(id=post['user_to'])
        # messages = request.user.received.all()
        # pk_list = messages.values_list('user_from__pk',flat=True).distinct()
        # correspondents = get_user_model().objects.filter(pk__in=pk_list)
        insert = chatMessages(user_from=u_from,user_to=u_to,message=post['message'])
        try:
            insert.save()
            resp['status'] = 'success'
        except Exception as ex:
            resp['status'] = 'failed'
            resp['mesg'] = ex
    else:
        resp['status'] = 'failed'

    return HttpResponse(json.dumps(resp), content_type="application/json")
    # return TemplateResponse(request, 'chat/home.html', {'correspondents':correspondents}, content_type="application/json")
    # return render(json.dumps(resp), 'chat/home.html', content_type="application/json")




def uploadFile(request):
    if request.method == "POST":
        # Fetching the form data
        form = UploadForm(request.POST)
        file_form = FileModelForm(request.POST, request.FILES)
        files = request.FILES.getlist('file')  # field name in model
        if form.is_valid() and file_form.is_valid():
            document = form.save(commit=False)
            document.user = request.user
            document.save()
            for f in files:
                file_instance = FeedFile(file=f, feed=document)
                file_instance.save()

        # Saving the information in the database
            return redirect('chat-home')
    else:
        form = UploadForm()
        file_form = FileModelForm()

    return render(request, "chat/files/post.html", {
        'form': form,
        'file_form':file_form,
    })



def buy_files(request):
    bdfiles = FeedFile.objects.all().order_by('id')
    paginator = Paginator(bdfiles,10)
    page_number = request.GET.get('page')
    page_obj= paginator.get_page(page_number)
    # bdfiles = UploadFile.objects.all()
    form = FileFilterForm(request.GET)
    if form.is_valid():
        if form.cleaned_data.get("number_course"):
            page_obj = bdfiles.filter(feed__number_course = form.cleaned_data.get("number_course"))
        if form.cleaned_data.get("number_semestr"):
            page_obj = bdfiles.filter(feed__number_semestr = form.cleaned_data.get("number_semestr"))
        if form.cleaned_data.get("subjectt"):
            page_obj = bdfiles.filter(feed__subjectt = form.cleaned_data.get("subjectt"))
        if form.cleaned_data.get("type_materials"):
             page_obj = bdfiles.filter(feed__type_materials = form.cleaned_data.get("type_materials"))
        if form.cleaned_data.get("institute"):
            page_obj = bdfiles.filter(feed__institute = form.cleaned_data.get("institute"))

    return render(request, 'chat/files/buyfile.html', {'bdfiles': bdfiles, 'form':form, 'page_obj':page_obj})


class EmailVerify(View):
    def activate(self, request, uidb64, token):
        user = self.get_user(uidb64)

        if user is not None and token_generator.check_token(user, token):
            user.profile_email_verify = True
            user.save()
            login(request, user)
            return redirect('chat-home')
        return redirect('invalid_verify')

    @staticmethod
    def get_user(uidb64):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist, ValidationError):
            user = None
        return user


def signup(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            context = {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            }
            message = render_to_string('chat/registration/activate.html', context=context, )
            mail_subject = 'Activate your blog account.'
            # to_email = form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, message, to=[user.email])
            email.send()
            return redirect('confirm_email')

    else:
        form = UserRegistrationForm()

    return render(request, 'chat/registration/register.html', {'form': form})




def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # return redirect('home')
        return redirect('nice_verify')
    else:
        return redirect('invalid_verify')


class LoginUser(LoginView):
    form_class = LoginUserForm()
    template_name = 'login.html'

    def get_context(self, *, object_list = None, **kwargs):
        context=super().get_context_data(**kwargs)
        c_def=self.get_user_context(title='Авторизация')
        return dict(list(context.items()) + list(c_def.items()))


def download(request,path):
    file_path = os.path.join(settings.MEDIA_ROOT,path)
    if os.path.exists(file_path):
        with open(file_path,'rb') as fh:
            response = HttpResponse(fh.read(), content_type='application/file')
            response['Content-Disposition'] = 'inline;filename='+os.path.basename(file_path)
            return response
        raise Http404

def show_file(request,file_id):
    file = get_object_or_404(FeedFile,pk=file_id)

    context = {
        'title': file.feed.title,
        'description': file.feed.description,
        'price': file.feed.price,
        'number_course': file.feed.number_course,
        'number_semestr': file.feed.number_semestr,
        'subjectt': file.feed.subjectt,
        'type_materials': file.feed.type_materials,
        'institute': file.feed.institute,
        'id':file_id,
        'file':file,
    }
    return render(request,'chat/files/file.html',context=context)

def show_helps(request,help_id):
    file = get_object_or_404( WhiteHelpFile,pk=help_id)

    context = {
        'titles': file.feed.titles,
        'descriptions': file.feed.descriptions,
        'prices': file.feed.prices,
        'course': file.feed.course,
        'semestr': file.feed.semestr,
        'subjects': file.feed.subjects,
        'institutes': file.feed.institutes,
        'id':help_id,
        'file':file,

    }
    return render(request,'chat/help/help.html',context=context)

def help(request):
    return HttpResponse('Эта страничка для помощи')





def write_help(request):
    if request.method == "POST":
        # Fetching the form data
        form = WritehelpForm(request.POST)
        file_form = WhiteHelpFileForm(request.POST, request.FILES)
        files = request.FILES.getlist('file')  # field name in model
        if form.is_valid() and file_form.is_valid():
            document = form.save(commit=False)
            document.user = request.user
            document.save()
            for f in files:
                file_instance = WhiteHelpFile(file=f, feed=document)
                file_instance.save()

        # Saving the information in the database
            return redirect('chat-home')
    else:
        form = WritehelpForm()
        file_form = WhiteHelpFileForm()

    return render(request, "chat/help/write_help.html", {
        'form': form,
        'file_form':file_form,
    })


def find_help(request):
    bdfiles = WhiteHelpFile.objects.all().order_by('id')
    paginator = Paginator(bdfiles,10)
    page_number = request.GET.get('page')
    page_obj= paginator.get_page(page_number)
    context = {
        'bdfiles': bdfiles,
        'page_obj': page_obj,
    }
    # bdfiles = UploadFile.objects.all()
    # form = FileFilterForm(request.GET)
    # if form.is_valid():
    #     if form.cleaned_data.get("number_course"):
    #         bdfiles = bdfiles.filter(feed__number_course=form.cleaned_data.get("number_course"))
    #     if form.cleaned_data.get("number_semestr"):
    #         bdfiles = bdfiles.filter(feed__number_semestr=form.cleaned_data.get("number_semestr"))
    #     if form.cleaned_data.get("subjectt"):
    #         bdfiles = bdfiles.filter(feed__subjectt=form.cleaned_data.get("subjectt"))
    #     if form.cleaned_data.get("type_materials"):
    #         bdfiles = bdfiles.filter(feed__type_materials=form.cleaned_data.get("type_materials"))
    #     if form.cleaned_data.get("institute"):
    #         bdfiles = bdfiles.filter(feed__institute=form.cleaned_data.get("institute"))

    return render(request, 'chat/help/find_help.html', context=context)