# Django-starter

## Create venv and activate
- `.\.venv\Scripts\activate`

## Create requirements.txt and install packages
`touch requirements.txt`

- Add required packages
Django
pillow
django-cleanup
django-allauth
django-htmx

- then install `pip install -r requirements.txt`
`pip install --upgrade pip`
`pip3 freeze --local > requirements.txt`

## start project `a_core` and setup DB
- `django-admin startproject a_core .`
- `python manage.py migrate`
- `python manage.py runserver`

## Create home page app `a_home`
- `python manage.py startapp a_home`
- Add it to INSTALLED_APPS in setting.py
- create view in a_home/views.py:
    def home_view(request):
    return render(request,'home.html')
- add path to views in root urls.py as:
    `from a_home.views import *`
    path('', home_view, name="home"),

## Add html files in templates dir
- `mkdir templates`
- register 'templates' dir in TEMPLATES var of settings.py 
- `'DIRS': [BASE_DIR / 'templates'],`
- File 1: base.html with code: https://github.com/andyjud/django-starter-assets
- create subfolder `templates/includes` and add these files:
- File 2: move `<messages>` into new includes/messages.html add `{% include 'includes/messages.html' %}` where it was
- File 3: move `<header>` into new includes/header.html add `{% include 'includes/header.html' %}` where it was
- create subfolder `templates/layout` and add these files:
- File 4: move `<content>` into new layout/blank.html add `{% block content %}` and `{% endblock %}`   where it was
- in blank.html: add `{% extends 'base.html' %}`, `<content>` between `{% block content %}` and `{% endblock %}`   
- File 5: create `home.html` in templates dir
- in home.html add: add `{% extends 'layouts/blank.html' %}`, `{% block content %}` and `{% endblock %}`   


## Create static folder in root dir
- `mkdir static`
- add static folder settings.py 
- add below STATIC_URL as `STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static'), ]`

## Create user profile pages
- create app `a_users` with: `python manage.py startapp a_users`
- add app to INSTALLED_APPS in settings.py
- create a model in models.py `Profille`
- Run `makemigrations` and `migrate`
- Register add in the admin.py wit view in admnin interface
- `admin.site.register(Profile)`

## Create signals.py  to create new profiles when users register.
- Create file `a_users/signals.py`
- Add code for creating user
- register `signals.py` in the `apps.py`
- by adding : `def ready(self):import a_users.signals` unser class `AUsersConfig`

## Create superuser to access admin panel
- `python manage.py createsuperuser`
- pass username, email and passwords
- start the server `python manage.py runserver`

## Add avatar and username variable in `templates/includes/header.html`
- add {{ user.profile.avatar }} to img src
- add {{ user.profile.name }} replacing 'username' text

## Create a profile page in views.py
- add code:
def profile_view(request):
    profile = request.user.profile
    return render(request, 'a_users/profile.html', {'profile':profile})
- folder in `a_users/templates/a_users`
- add `profile.html` with code: https://github.com/andyjud/django-starter-assets/blob/main/profile.html
- create path in root urls `path('profile/', include('a_users.urls')),`
- NB remember to import `include` next to `path`
- Create `urls.py` in app folder `a_users/urls.py`
- add code:
from django.urls import path
from a_users.views import *

urlpatterns =[
    path('',profile_view, name='profile'),
]
- add new url in `header.html`in href of 'My Profile' as `{% url 'profile' %}`
- `runserver`and check updates
- NB: ensure `{% block}` has the same block name, template its extending from e.g. 'layout' 

## Create edit profile page
- create a `forms.py` in `a_users` app folder
- add code:
from django.forms import ModelForm
from django import forms
from .models import Profile


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        exclude = ['user']
        widgets = {
            'image': forms.FileInput(),
            'displayname': forms.TextInput(attrs={'placeholder': 'Add display name'}),
            'info': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Add information'})
        }
- create a view for edit profile in views.py
- add code:
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import *

def profile_view(request):
    profile = request.user.profile
    return render(request, 'a_users/profile.html', {'profile':profile})

@login_required
def profile_edit_view(request):
    form = ProfileForm(isinstance=request.user.profile)
    return render(request, 'a_users/profile_edit.html', {'form':form})

- create `profile_edit.html` file in app templates
- add code: https://github.com/andyjud/django-starter-assets/blob/main/profile_edit.html
- add path in call `urls.py` as `path('edit/', profile_edit_view, name='profile-edit'),`
- updated href in the `header.html` in 'Edit Profile'

## Create a new layout `box.html` in `templates/layouts`
- create file: `box.html`
- add code: https://github.com/andyjud/django-starter-assets/blob/main/box.html
- change `{% extends %}` from `blank.hmtl` to `box.html`

## Add functionality to save form to database
- in `profile_edit_view` in app views.py add code:
if request.method == 'POST':
    form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
    if form.is_valid():
        form.save()
        return redirect('profile')
- import `redirect` next to `render`
- add media folder to store uploaded user files
- create folder `media` in root dir 
- add 'media' to settings.py
- add below STATICFILES_DIRS
MEDIA_URL = 'media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
- Add path to the root `urls.py`
imports:
from django.conf.urls.static import static
from django.conf import settings
add code below `urlpatterns =[]`:
# only used in development
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
- refresh page and test 
- Add django cleanup to delete duplicated images
- in the INSTALLED_APPS, add code above custom apps
`'django_cleanup.apps.CleanupConfig',`

## Setup user logout - allauth
- refer: https://docs.allauth.org/en/latest/installation/quickstart.html
- in `settings.py`:
add `AUTHENTICATION_BACKENDS` below `MIDDLEWARE`:
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend'
]

add allauth as in `INSTALLED_APPS` above custom apps:
'allauth',
'allauth.account',
'allauth.socialaccount',

add allauth middleware in `MIDDLEWARE`:
'allauth.account.middleware.AccountMiddleware',

add accounts path to the root `urls.py`:
path('accounts/',  include('allauth.urls')),

- Run migration to impelement changes
`python manage.py migrate`

- add logout href 'Log Out' to `header.html` as `{% url 'account_logout' %}`
- `runserver` and test logout

## Style logout page
create dir `templates/allauth/layouts`
add `base.html` file and add code:
{% extends 'layouts/box.html' %}

{%block class %}allauth{% endblock %}

{% block content %}
{% endblock %}

## Add login link in `header.html`
- add login href 'Login' to `header.html` as `{% url 'account_login' %}`
- add configrs to `settings.py` at the bottom:
LOGIN_REDIRECT_URL = '/'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_REQUIRED= True

## Override notification pop-ups for login/logout
- create folder in `templates/account/messages`
- add file `logged_in.txt` and `logged_out.txt`

## Add sign-up link in `header.html`
- add sign-up href 'Sign up' to `header.html` as `{% url 'account_signup' %}?next={% url 'profile-onboarding' %}`
- `?next=` directs user to the `profile-onboarding` page
- add `profile-onboarding` page to app `urls.py`:
`path('onboarding/', profile_edit_view, name='profile-onboarding'),`

- in `profile_edit_view` in `a_users/views.py` add:
if request.path == reverse('profile-onboarding'):
    onboarding = True
else:
    onboarding = False

- add `'onboarding':onboarding` to rendered context object
- import reverse `from django.urls import reverse`

- in `profile_edit.html` revise `<h1>` element:
{% if onboarding %}
<h1 class="mb-4">Complete your Profile</h1>
{% else %}
<h1 class="mb-4">Edit your Profile</h1>
{% endif %}

- in `profile_edit.html` revise `cancel` button in `<form>` element:
{% if onboarding %}
<a class="button button-gray ml-1" href="{% url 'home' %}">Skip</a>
{% else %}
<a class="button button-gray ml-1" href="{{ request.META.HTTP_REFERER }}">Cancel</a>
{% endif %}

## Ensure only lower case username in DB
- in `a_users/signals.py` add:
@receiver(pre_save,sender=User)
def user_presave(sender, instance, **kwargs):
    if instance.username:
        instance.username = instance.username.lower()

- import `pre_save` next to `post_save`

## Create path to access profiles by `@kakaort`
- in root `urls.py` add path as:
`path('@<str:username>/', profile_view, name="profile"),`
- import `profile_view`: `from a_users.views import profile_view`
- in `profile_view` of `a_users/profile_view` in views.py: 
- import `get_object_or_404` next to `redirect`; import `from django.contrib.auth.models import User`
- Add `username=None` as input arg into `profile_view()`
full revised code:
def profile_view(request, username=None):
    if username:
        profile = get_object_or_404(User, username=username).profile
    else:
        try:
            profile = request.user.profile
        except:
            redirect('account_login')
            
    return render(request, 'a_users/profile.html', {'profile':profile})

- if user trying to access 'profile' url while not logged in, gets redirected to login

## Setup the `settings` page:
- create a view `profile_settings_view` in a_users/views.py:
@login_required
def profile_settings_view(request):
    return render(request, 'a_users/profile_settings.html')

- create `profile_settings.html` in `a_users/templates`:
- add code: https://github.com/andyjud/django-starter-assets/blob/main/profile_settings.html
- create path in `a_users/urls.py`:
path('settings/', profile_settings_view, name='profile-settings'),
- Add urls to `header.html`

## Add the `edit` link in `profile_settings.html` using htmx:
- ensure `django-htmx` package is installed else `pip install django-htmx`
- add `django-htmx` to INSTALLED_APPS in settings.py, above custom apps
- add `django_htmx.middleware.HtmxMiddleware` to INSTALLED_APPS in settings.py, bottom of list
- add an edit email form in `forms.py` and add:
class EmailForm(ModelForm):
    email = forms.EmailField(required=True)

    class Meta:
        model= User
        fields = ['email']
- NB `from django.contrib.auth.models import User`
- create a view for the form
@login_required
def profile_emailchange(request):

    if request.htmx:
        form = EmailForm(instance=request.user)
        return render(request, 'partials/email_form.html', {'form':form})
    
    return redirect('home')
- if htmx request, pass the snippet to front end 

- Create `partials/email_form.html` in root template dir
add code: `https://github.com/andyjud/django-starter-assets/blob/main/email_form.html`

- Create path in app `urls.py`:
path('emailchange/', profile_emailchange, name='profile-emailchange'),

- Add htmx code in `profile_settings.html`:
- replace `href=""` in the Edit '<a>' element and add htmx attributes:
hx-get="{% url 'profile-emailchange' %}"
hx-target="#email-address"
hx-swap="innerHTML"
- include a `cursor-pointer` class

- Add code to saved data to database:
-import messages: `from django.contrib import messages`
add code and check if email already exists else `save()`.
    if request.method == "POST":
        form = EmailForm(request.POST, instance=request.user)

        if form.is_valid():

            # Check if the email already exists 
            email= form.cleaned_data['email']
            if User.objects.filter(email=email).exclude(id=request.user.id).exists():
                messages.warning(request, f"{email} is already in use.")
                return redirect('profile-settings')
            
            form.save()

- in `signals.py` with `user_postsave()` 
- import `from allauth.account.models import EmailAddress`
add below `if created:`:
    else:
        #update allauth emailaddresse if exist else create one
        try:
            email_address = EmailAddress.objects.get_primary(user)

            if email_address.email !=user.email:
                email_address.email= user.email
                email_address.verified= False
                email_address.save()
            
        except:
            EmailAddress.objects.create(
                user = user,
                email =user.email,
                primary = True,
                verified = False
            )

- back to `singals.py`:
- import `from allauth.account.utils import send_email_confirmation`
- add below `form.save` in `profile_emailchange()` of app `views.py`
    # Then send confirmation email
    send_email_confirmation(request, request.user)

    return redirect('profile-settings')

else:
    messages.warning(request, "Form not valid")
    return redirect('profile-settings')


## Enable the `verify` link in `profile_settings.html`
- in views.py add code:
@login_required
def profile_emailverify(request):
    send_email_confirmation(request, request.user)
    return redirect('profile-settings')

- add path is app `urls.py`:
`path('emailverify/', profile_emailverify, name='profile-emailverify'),`

- add url in `profile_settings.html`:
- add `{% url 'profile-emailverify' %}` in 'Verify' "<a>" href attribute

## Setup profile delete
- in the app `views.py`:
@login_required
def profile_delete_view(request):
    return render(request, 'a_users/profile_delete.html')

- create `a_users/profile_delete.html` file
add code: `https://github.com/andyjud/django-starter-assets/blob/main/profile_delete.html`

- add path to app `urls.py`:
`path('delete/', profile_delete_view, name='profile-delete'),`

- Add url to `profile_settings.html`:

- add functionality to `profile_delete_view` in `views.py`:
- import: `from django.contrib.auth import logout`
add code:
    user =request.user
    if request.method == "POST":
        logout(request)
        user.delete()
        messages.success(request, 'Account deleted, what a pity')
        return redirect('home')

## Add 404 page
- add `404.html` to root templates folder
- add code: `https://github.com/andyjud/django-starter-assets/blob/main/404.html`
- test by changing `DEBUG` to False in settings.py
- add `ALLOWED_HOSTS`: `'127.0.0.1',` for dev only

## Start new app - a_rtchat
- `python manage.py startapp a_rtchat`
- add app to `INSTALLED_APPS`
- add view in `a_rtchat/views.py`
def chat_view(request):
    return render(request,'a_rtchat/chat.html')
- create `chat.html` in app templates
`templates/a_rtchat/chat.html`
add code: https://github.com/andyjud/realtime-chat/blob/main/chat.html
- Create app `urls.py`
add code:
from django.urls import path 
from .views import *

urlpatterns = [
    path('',chat_view, name="home"),
]
- Note: named home as its in the home page
- include in root `urls.py`
- replaces `path('', home_view, name="home"),` with:

## Create models for DB
- in app `models.py` add:
class ChatGroup(models.Model):
    group_name = models.CharField(max_length=128,unique=True)

    def __str__(self):
        return self.group_name
- `ChatGroup` stores all the chatrooms (trps)
- import `from django.contrib.auth.models import User`
- add new model to store group messages
class GroupMessage(models.Model):
    group = models.ForeignKey(ChatGroup,related_name='chat_messages', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.CharField(max_length=300)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author.username} : {self.body}"

    class Meta:
        ordering = ['-created']

- register models in the `admin.py` to display in admin panel. add:
from django.contrib import admin
from .models import ChatGroup, GroupMessage

admin.site.register(ChatGroup)
admin.site.register(GroupMessage)

- Run `makemigrations` and `migrate`
`python manage.py makemigrations`
`python manage.py migrate`

- Create `superuser` to access admin panel
`python manage.py createsuperuser`
e.g. 'admin'

- go to admin panel and login as superuser
- create a chat group `add Chat groups` - e.g. public-chat
- add Group message, select `public-chat` as group, `admin` as user, enter a message
- add another user under `Users`, pass username and password
- add Group message, select `public-chat` as group, `vegeta` as user, enter a message

## Display messages from DB
- add code in `chat_view` of `a_rtchat/views.py`
revive code to:
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import ChatGroup

@login_required
def chat_view(request):
    chat_group = get_object_or_404(ChatGroup, group_name="public-chat")
    chat_messages = chat_group.chat_messages.all()[:30]
    
    return render(request,'a_rtchat/chat.html', {'chat_messages':chat_messages})

- `@login_required` ensures only logged in users can view messages
- `chat_group.chat_messages` is from the foregin key in `GroupMessage` model

- Add code in `chat.html` to display messages
`{% for message in chat_messages reversed %}
{% if message.author == user %}
<`li class="user">
{% else %}
<`li class="receiver">
{% endif %}
{% endfor %}`
- Use `User` properties to access `username` and `avatar`


## Configure form to send messages
- create `forms.py` in app `a_rtchat`
-  Add code:
from django.forms import ModelForm
from django import forms
from .models import *

class ChatMessageCreateForm(ModelForm):
    class Meta:
        model =GroupMessage
        fields =['body']
        widgets = {
            'body': forms.TextInput(attrs={'placeholder': 'Add message...', 'class':'p-4 text-black', 'maxlength': '300', 'autofocus':True})
        }

- `from django import forms` works similar to crispy_forms
- import forms in `views.py`: `from .forms import *`
- create a form instance: `form = ChatMessageCreateForm()` in `chat_view()`
- add code to change submission `chat_views`:
- import `redirect` next to `render`
def chat_view(request):
    chat_group = get_object_or_404(ChatGroup, group_name="public-chat")
    chat_messages = chat_group.chat_messages.all()[:30]
    form = ChatMessageCreateForm()

    if request.method == "POST":
        form = ChatMessageCreateForm(request.POST)

        if form.is_valid:
            message = form.save(commit=False)
            message.author = request.user
            message.group = chat_group
            message.save()
            redirect('home')

    return render(request,'a_rtchat/chat.html', {'chat_messages':chat_messages,'form':form})

- add form to `chat.html` template 
- replace fields in the `<from>` element with `{{ form }}`
- include `{% csrf_token %}` field above the `forms` in template

## Add HTMX to prevent reloads on every message
- replace `medthod` attribute of `<form>` with:
hx-post="{% url 'home' %}"
hx-target="#chat_messages"
hx-swap="beforeend">
- `chat_messages` in `hx-target="#chat_messages"` refers to id of `<ul>` element

- in chat_view
- replace `if request.method=="POST"` with `if request.htmx`
- replace `return redirect('home')`  with:
context = {
                'message':message,
                'user': request.user
            }
return render(request,'a_rtchat/partials/chat_message_p.html',context)

- create `a_rtchat/partials/chat_message_p.html` in app templates folder
- add code:
{% include 'a_rtchat/partials/chat_message_p.html' %}

- in the `chat.html`, move the `{% if message.author ==  user %}` into new file `chat_messages.html` (same level as `chat.html`)
- add code to include it in `chat.html`: `{% include 'a_rtchat/chat_message.html' %}` 

- Issue: the form field doesn't clear the text
- Use javascript to clear or hyper script
- go to: `https://hyperscript.org/` and copy the script tag:
`<script src="https://unpkg.com/hyperscript.org@0.9.14"></script>`
- add script in `base.html`

in `chat.html` in the `<form>` attributes add:
`_="on htmx:afterRequest reset() me"`
-refesh and test

## Add aesthetic for message appearance:
- in `a_rtchat/partials/chat_message_p.html`
wrap the `{% inclde ... %}` in a `<div>` to animate it:
<!-- <div class="fade-in-up">
{% include 'a_rtchat/chat_message.html' %}
</div>

<style>
    @keyframes fadeInAndUp {
        from {opacity: 0; transform: translateY(12px);}
        to {opacity: 1; transform: translateY(0);}
    }

    .fade-in-up {
        animation: fadeInAndUp 0.6s ease;
    }
</style> -->

## implement auto-scroll to display latest message(JS)
- add `<script>` tag in `chat.html` inside `{% block javascript %}`
{% block javascript %}
<`script>
    function scrollToBottom() {
        const container = document.getElementById('chat_container');
        container.scrollTop = container.scrollHeight;
    }
    scrollToBottom()
<`/script>
{% endblock %}
- NB: add `{% block javascript %}` to `base.html`
- call the function when new message comes in partials:
`<script>scrollToBottom()</script>`

# Upgrade to channels and websockets

## install channels
- `pip install -U 'channels[daphne]'`
- `pip freeze --local > requirements.txt`
- Add `daphne` to INSTALLED_APP as first app
- below `WSGI_APPLICATION = 'a_core.wsgi.application'` add (could comment it out)
ASGI_APPLICATION = 'a_core.asgi.application' # which connects to `asgi.py` file

## Setup websocket connect using asgi web server
- add a router to handle websocket in addition to http requests
- in `a_core/asgi.py` in root project folder revise code:
import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from channels.auth import AuthMiddlewareStack

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'a_core.settings')

django_asgi_app = get_asgi_application()

from a_rtchat import routing

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(URLRouter(routing.websocket_urlpatterns))
    ),
})

- create file `a_rtchat/routing.py`
- add code:
from django.urls import path
from .consumers import *

websocket_urlpatterns = [
    path("ws/chatroom/<chatroom_name>", ChatroomConsumer.as_asgi()),
]

- create file `a_rtchat/consumers.py`
- add code:
from channels.generic.websocket import WebsocketConsumer

class ChatroomConsumer(WebsocketConsumer):

    def connect(self):
        self.accept()

## Install websockets extension
- go to `https://htmx.org/extensions/ws/`
- get the code and add it to `base.html`:
`<script src="https://unpkg.com/htmx.org/dist/ext/ws.js" defer></script>`
- To include extension in the `chat.html` template:
- replace the htmx attribute in the `<form>` element:
hx-post="{% url 'home' %}"
hx-target="#chat_messages"
hx-swap="beforeend"
- in place add:
hx-ext="ws"
ws-connect="/ws/chatroom/public-chat"
ws-send

## Adjust consumers.py to enable form functionality 
- In the `_="on htmx:afterRequest reset() me"` attribute in `<form>` of `chat.html`
revise to `_="on htmx:wsAfterSend reset() me"`

from channels.generic.websocket import WebsocketConsumer
from django.shortcuts import get_object_or_404
import json
from .models import *


class ChatroomConsumer(WebsocketConsumer):

    def connect(self):
        self.user = self.scope['user']
        self.chatroom_name = self.scope['url_route']['kwargs']['chatroom_name']
        self.chatroom = get_object_or_404(
            ChatGroup, group_name=self.chatroom_name)
        self.accept()

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        body = text_data_json['body']
        
        message = GroupMessage.objects.create(
            body = body,
            author = self.user,
            group = self.chatroom
        )

- revise partials `chat_message_p.html`:
wrap all code with a div: `<div id="chat_messages" hx-swap-oob="beforeend"></div>`

## Add channel layer
- in `settings.py` below `ASGI_APPLICATION` add:
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer',
    }
}

- in `consumers.py` add logic:

## Counting No. of users 'online'
- count channels in a channel layer
- workaround (development only) - create a property on DB to store mannually counted channels
- in the `ChatGroup` model of `models.py` add:
`users_online = models.ManyToManyField(User, related_name='online_in_groups', blank= True)`
- Run `makemigration` and `migrate` to include new field

## Add logic use `users_online`
- `ChatroomConsumer` in `consumers.py` :
- in `def connect():` - if user is not in the users_online add them
- in `def disconnect():` - if user is in the users_online remove them
- call a function to update online count `update_online_count()`
- on `online_count = self.chatroom.users_online.count()` subtract 1 to exclude self
- added functions:
def update_online_count(self):
    online_count = self.chatroom.users_online.count()
    event =  {
        "type": "online_count_handler",
        "online_count":online_count,
    }

    async_to_sync(self.channel_layer.group_send)(self.chatroom_name,event)

def online_count_handler(self, event):

    online_count = event['online_count']
    context= {
        "online_count":online_count,
    }
    html = render_to_string("a_rtchat/partials/online_count.html",context=context)
    self.send(text_data=html)

- create `a_rtchat/partials/online_count.html`partial
- `hx-swap-oob="outerHTML"` added to indicated a whole html element will be swapped
- 'fadeInScale' animation included for aesthetics#
- `{% if else endif %}` used to style dot conditionally depending on user count online
add code:
<span id="online-count" hx-swap-oob="outerHTML" class="pr-1 fade-in-scale">
    {{ online_count }}

    <style>
        @keyframes fadeInScale {
            from {opacity: 0; transform: scale(4);}
            to {opacity: 1; transform: scale(1);}
        }
        .fade-in-scale {
            animation: fadeInScale 0.6s ease;
        }
    </style>
</span>
{% if online_count %}
<div id="online-icon" class="absolute top-2 left-2 rounded-full bg-green-500 p-1.5"></div>
{% else %}
<div id="online-icon" class="absolute top-2 left-2 rounded-full bg-gray-500 p-1.5"></div>
{% endif %}

# Using redis:
- Redis is an in-memmory data structure that can be used as:
    - Cache (RAM for storage)
    - Database (RAM and RDB snapshots)
    - Message Broker (pub/sub)
- make apps faster
- sits between app and database (postgres)
- app looks in redis storage first before querying database
- data are stored key-value pair
- Redis not open source anymore (can be used as open source for non-paid services), alternatives:
- 1) Valkey (fork of redis by linux foundation) backed by AWS and Google Cloud
- 2) Garnet (by microsoft)
- 3) KeyDB (by snap Inc.)
- Installing Redis locally:
- MacOs - via `homebrew`
- Windows - via WSL (Windows Subsystem for Linux)
- Linux - direct installation

## Connect appliaction to redis DB, hosted by web service providers e.g. railway
- add config setting in `settings.py`
- install channels-redis: `pip install channels-redis`
`pip3 freeze --local > requirements.txt`
- check official doc site `https://pypi.org/project/channels-redis/`
- copy the `CHANNEL_LAYERS` config and paste below existing `CHANNEL_LAYERS` in `settings.py`
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [('127.0.0.1', 6379)]
        }
    }
}

- For Railway:

- For Heroku:
1) refer - `https://redis.io/learn/create/heroku/portal`
    - on Heroku, navigate to `Settings` tab
    - In the `Config Vars` add:
    - `REDIS_ENDPOINT_URI` with the values of your end point e.g `redis-***.azure.cloud***`
    - `REDIS_PASSWORD` with the values of your secret password


2) Creating Redis free account:
    - go to `https://redis.io/try-free/`
    - signup using social (google/github) or email and password
    - In the `Create your database` page, select the `Essentials` for free database
    - Under Cloud vendor, select your prefered vendor (AWS, Google Cloud or Microsoft Azure)
    - Select Region and click `Get started`
    - Once setup, refer to and database setp and retrieving credentials `https://redis.io/docs/latest/operate/rc/rc-quickstart/`
    - To connect to a database - go to `Security` section of the page by scrolling down within the `Configuration` tab
    - Copy sectret password and username (could be "default")
    - take not of the `public endpoint` in the `General` section
    - within the section click `connect`
    - choose `Redis CLI`
    - copy the `URL` after `redis-cli -u`, should start with `redis://default:**`
    - create an envronment variable `REDIS_URL` and save it to env.py 
    - import and add it to `CHANNEL_LAYERS` object
    - comment-out `InMemoryChannelLayer` channel_layers and test
    - not longer using gunicorn:
    - Add two line:
    `web: daphne a_core.asgi:application --port $PORT --bind 0.0.0 -v2`
    `chatworker: python manage.py runworker --settings=a_core.settings -v2`

3) Deploying on Heroku
ref: Deploy Django + Channels + Redis + Heroku + Daphne `https://www.youtube.com/watch?v=zizzeE4Obc0`
- create an app
- navigate to `Resources`
- Under `Add-ons` search for `Heorku Redis`
- For plan name, select `Hobby Dev - Free` the `Provision`
- Go to `Deploy` tab and GitHub
- Connect your repo
- in VS code, setup required Heroku files e.g `Procfile` with contents:
 `web: daphne chat.asgi:application --port $PORT --bind 0.0.0 -v2` #'chat' is the root project, 'v2' console logs
 `chatworker: python manage.py runworker --settings=chat.settings -v2` #'chat' is the root project
- add `runtime.txt` file with python version e.g. `python-3.12`

# Setup cloudindary:
## install cloudinary packages:
`pip3 install cloudinary~=1.36.0 dj3-cloudinary-storage~=0.0.6 urllib3~=1.26.15`
`pip3 freeze --local > requirements.txt`

## Step 1: Install required packages
`pip3 install cloudinary~=1.36.0 dj3-cloudinary-storage~=0.0.6 urllib3~=1.26.15`
`pip3 freeze --local > requirements.txt`

## Step 2: Sign up for a cloudinary account
- email or google account at `https://cloudinary.com/users/register_free`
- From `Cloudinary Dashboard` click on the `Go to API Keys`
- copy `CLOUDINARY_URL=cloudinary://<your_api_key>:<your_api_secret>@dltmrnhmx`

- Add os.environ to eny.py
`os.environ.setdefault("CLOUDINARY_URL", "cloudinary://<your_api_key>:<your_api_secret>@dltmrnhmx")`

- refer to `https://cloudinary.com/blog/managing-media-files-in-django`

## Step 3: Add cloudinary_storage and cloudinary to INSTALLED_APPS in my_project/setting.py
- `cloudinary_storage` must be added below `django.contrib.staticfiles`
- `cloudinary` added above the first custom app, below summernote if it exists
- Add `config`
import cloudinary
import cloudinary.uploader
import cloudinary.api

cloudinary.config( 
  	cloud_name = os.environ.get("CLOUDINARY_NAME"),
  	api_key = os.environ.get("CLOUDINARY_API_KEY"),
  	api_secret = os.environ.get("CLOUDINARY_SECRET_KEY")
)

## Step 4: Update blog app to use Cloudinary
- Import CloudinaryField in blog/models.py
`from cloudinary.models import CloudinaryField`

## Step 5: Add field in the Post model to store image for each post
- added below author field `featured_image = CloudinaryField('image', default='placeholder')`

## Step 6: Run makemigrations and migrates
- if changing already existing filed run `python manage.py migrate a_users zero` and delete migration versions
`python manage.py makemigrations`
`python manage.py migrate`

## Step 7: Add DTL loop within from image-container in the blog/templates/blog/index.html
- Add `{% load static %}` at the top, below `{% extends ...%}`
    `{% if "placeholder" in post.featured_image.url %}
    <img class="card-img-top" src="{% static 'images/default.jpg' %}"
        alt="placeholder image">
    {% else %}
    <img class="card-img-top" src=" {{ post.featured_image.url }}" alt="{{ post.title }}">
    {% endif %}`

- Code so far: https://github.com/Code-Institute-Solutions/django-blog-sourcecode/tree/main/13-where-to-put-things/13.2-storing-images-on-cloudinary
- Change DEBUG to False and save all files
- Git add, commiit and push
    `git add --all`
    `git commit -m "enable serving of image files"`
    `git push origin main`

## Step 8: Add CLOUDINARY_URL to ConfigVars in Heroku
- Create a key value pair and copy contents in the env.py
- `Deploy Branch` and check the updates

# Deployment notes:

1) Define environmental variables:
    - `DATABASE_URL` set to url link in env.py
    - `SECRET_KEY` set to url link in env.py
    - `CLOUDINARY_URL` set to url link in env.py
    - `REDIS_URL` set to url link in env.py
    - `IS_DEVELOPMENT` set to 0
    - `CLOUDINARY_NAME` set to value in env.py
    - `CLOUDINARY_API_KEY` set to value in env.py
    - `CLOUDINARY_SECRET_KEY` set to value in env.py

2) Set DEBUG to False for production
- `DEBUG = (os.getenv('IS_DEVELOPMENT', 'False') == 'True')`

3) Configure Postgres database
- using enviromnetal variables
`pip3 install dj-database-url~=0.5 psycopg2~=2.9`
`pip3 freeze --local > requirements.txt`

- add `CSRF_TRUSTED_ORIGINS` below DB settings
CSRF_TRUSTED_ORIGINS = [
    "https://*.codeinstitute-ide.net/",
    "https://*.herokuapp.com"
]

4) Configure redis for production
if ENVIRONMENT == 'production':
        CHANNEL_LAYERS = {
        'default': {
            'BACKEND': 'channels_redis.core.RedisChannelLayer',
            'CONFIG': {
                'hosts': [(REDIS_URL)]
            }
        }
    }
else:
    CHANNEL_LAYERS = {
        'default': {
            'BACKEND': 'channels.layers.InMemoryChannelLayer',
        }
    }

5) Add static files
- `pip3 install whitenoise~=5.3.0`
- include the `whitenoise.middleware.WhiteNoiseMiddleware` in `MIDDLEWARE` object of `setting.py`
- 2nd from the top

6) Media files configi // or Cloudinary setup

7) Github account repo


8) Add webserver and `ALLOWED_HOSTS` in `settings.py`
- add `CRSF_TRUSTED_ORIIGINS`
- `'.herokuapp.com',` include in `ALLOWED_HOSTS`
9) add start command in `Procfile`
`daphne a_core.asgi:application -b 0.0.0.0 -p $PORT`

10) Add `runtime.txt` file specifying version
`python 3.12.8`
- changed to `.python-version` with `3.12`

11) Add ALLOWED

12) Run Collectstatic
in `setting.py` add `STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')`
`python manage.py collectstatic`

13) Update requirements
`pip3 freeze --local > requirements.txt`

14) Git add, commit and push

15) Delplyoy on Heroku
- run CLI:
- `heroku login`
-  confirm login in browser
- run log print `heroku logs --app warriors-chat -t`
- `warriors-chat` is the app name in heroku
- `-t` - give continous logs

# Add json file for chats
- in `a_rtchat/admin.py` add to display user with their ids
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'displayname', 'id')

admin.site.register(Profile, ProfileAdmin)

- run `python manage.py migrate a_users zero` and delete migration files
- run `makemigrations` and `migrate`
- in admin panel, create the group `public-chat`
- add file `a_rtchat/fixtures/chats.json`
- add `a_rtchat/fixtures/` to `.gitignore`
- Add content in the format of the `a_rtchat/models.py GroupMessage`
- use `username` instead of `id`
- format:
[
    {"model": "a_rtchat.groupmessage", "pk": 1, "fields": {"group": 1, "author": ["goku"], "body": "Did you see how I unlocked Ultra Instinct? That was epic!", "created": "2024-06-13T10:00:00Z"}},

    {},...

]
- To load the posts.json file to the database run:
`python manage.py loaddata chats`
- refresh and test

# Creating Private chats

## Modify a_rtchat model
- `pip install shortuuid`
- `pip3 freeze --local > requirements.txt`
- in in `ChatGroup` model of `a_rtchat/models.py`
- add `default=shortuuid.uuid` to group_name field
- add new field: `members = models.ManyToManyField(User, related_name='chat_groups', blank=True)`
- can be blank as public-chat has no members
- add new field: `is_private = models.BooleanField(default=False)`
- run `makemigrations` and `migrate`

## Create front-end elements to start private chat
- in `a_users/templates/profile.html` add:
    {% if profile.user != user %}
    <a href="{% url 'start-chat' profile.user.username %}" class="button">Chat with me</a>
    {% endif %}
- display button when view profile other users only

## Configure urls
- create 'start-chat' and 'chatroom' urls in `a_rtchat/urls.py`:
    path('chat/<username>',get_or_create_chatroom, name="start-chat"),
    path('chat/room/<chatroom_name>',chat_view, name="chatroom"),
- `get_or_create_chatroom` checks if 'chatroom' already exist else create new one
- if exist, user is directed to second view `chatroom`

## Configure views
- add `get_or_create_chatroom` in `a_rtchat/views.py`
- import `from django.contrib.auth.models import User`
- the view take `username` as an argument
- if current user and passed `username` are equal, redirect to `home` view
- else, get user with `username`
- get all current user's private chats
- loop through all user's private chats, check if other_user is in any of them
- redirect user to retrived chatroom, pass group_name as argument for 'chatroom' view
- if there are no private chatrooms with the other user, create one
- redirect user to created chatroom, pass group_name as argument for 'chatroom' view
@login_required
def get_or_create_chatroom(request, username):
    if request.user.username == username:
        return redirect('home')
    
    other_user = User.objects.get(username=username)
    my_chatrooms = request.user.chat_groups.filter(is_private=True)

    if my_chatrooms.exists():
        for chatroom in my_chatrooms:
            if other_user in chatroom.members.all():
                return redirect('chatroom', chatroom.group_name)
   
    chatroom = ChatGroup.objects.create(is_private=True)
    chatroom.members.add(other_user, request.user)

    return redirect('chatroom', chatroom.group_name)

## revise `chat_view` view
- include `chattoom_name='public-chat'` arg in def, default is public-chat 
- create varaibl `other_user`, if chatroom is private, check if user is authorized else raid 404 error
- import `from django.http import Http404`
- loop throuhg members of the group to find `other_user` then break loop
- pass `other_user` to rendered context
- include `chatroom_name` used for websocket connection
- Final revised chat_view():
@login_required
def chat_view(request,chatroom_name='public-chat'):
    chat_group = get_object_or_404(ChatGroup, group_name=chatroom_name)
    chat_messages = chat_group.chat_messages.all()[:30]
    form = ChatMessageCreateForm()

    other_user = None
    if chat_group.is_private:
        if request.user not in chat_group.members.all():
            raise Http404()
        
        for member in chat_group.members.all():
            if member != request.user:
                other_user= member
                break

    if request.htmx:
        form = ChatMessageCreateForm(request.POST)

        if form.is_valid:
            message = form.save(commit=False)
            message.author = request.user
            message.group = chat_group
            message.save()
            context = {
                'message':message,
                'user': request.user
            }
            return render(request,'a_rtchat/partials/chat_message_p.html',context)
        
    context = {
        'chat_messages':chat_messages,
        'form':form,
        'other_user':other_user,
        'chatroom_name': chatroom_name,
        }
    
    return render(request,'a_rtchat/chat.html', context=context)

## adjust `a_rtchat/templates/chat.html`
- in the `<form>` attributes, revise:
`ws-connect="/ws/chatroom/{{ chatroom_name }}"`
- add `{% if other_user %}` condition to display other_user details if private chat
- Display online status of `other_user`, add above `{% if other_user %}`
`<div id="online-icon" class="gray-dot absolute top-2 left-2"></div>`
- defined `gray-dot` in css styles:
.green-dot {
    @apply rounded-full bg-green-500 p-l.5
}
.gray-dot {
    @apply rounded-full bg-gray-500 p-l.5
}
.graylight-dot {
    @apply rounded-full bg-gray-300 p-l.5
}

- update `a_rtchat/templates/partials/online_count.html` htmx partials revised to:
`<div id="online-icon" class="green-dot absolute top-2 left-2"></div>`
- replace multiple subclasses into one `green-dot` or `grey-dot`
- refresh and test 

##  Add all chatrooms for convenience:
- add to header naviation in root `templates/includes/header.html`
- Replace contents of `<li>` in `<li><a href="/">Home</a></li>` with:
<!-- <ul class="hoverlist [&>li>a]:justify-end">
<li><a href="{% url 'home' %}">Public Chat</a></li>
{% for chatroom in user.chat_groups.all %}
    {% if chatroom.is_private %}
        {% for member in chatroom.members.all %}
            {% if member != user %}
            <li><a href="{% url 'chatroom' chatroom.group_name %}">{{ member.profile.name }}</a></li>
            {% endif %}
        {% endfor %}
    {% endif %}
{% endfor %}
</ul> -->

- Create a loop and add all private chat current user is part of, inlcude home url as `Public Chat`
- check if chatroom is private
- for each chatroom, loop through all memeber to get `other_user`
- display `other_user`'s name using `{{ member.profile.name }}` 
- Note the online, shows the currently selected user 

# Create a group chat

## Modify a_rtchat model (incl admin)
- in `a_rtchat/models.py` in ChatGroup model class add:
groupchat_name = models.CharField(max_length=128, null=True,blank=True)
admin = models.ForeignKey(User, related_name='groupchats', blank=True, null=True, on_delete=models.SET_NULL)
- run `makemigrations` and `migrate`
- add link in profile menu: root `templates/includes/header.html`
`<li><a href="{% url 'new-groupchat' %}">Create a Chat</a></li>`
- This creates a list item `Create a Chat` in the menu list

## Create urls for `new-groupchat` urls
- in `a_rtchat/urls.py` add:
`path('chat/new_groupchat/',create_groupchat, name="new-groupchat"),`

## Create view for `create_groupchat` view
@login_required
def create_groupchat(request):
    return render(request, 'a_rtchat/create_groupchat.html')

## Create `a_rtchat/create_groupchat.html` template with contents:
{% extends 'layouts/box.html' %}

{% block content %}

<h1>New Group Chat</h1>

{% endblock %}
- run and test 

## Create a form for new group
- in `a_rtchat/forms.py` add:
class NewGroupForm(ModelForm):
    class Meta:
        model =ChatGroup
        fields =['groupchat_name']
        widgets = {
            'groupchat_name': forms.TextInput(attrs={
                'placeholder': 'Add name...', 
                'class':'p-4 text-black', 
                'maxlength': '300', 
                'autofocus':True})
        }

- include model in `views.py`, updated as
@login_required
def create_groupchat(request):
    form = NewGroupForm()

    context = {
        'form': form
    }
    return render(request, 'a_rtchat/create_groupchat.html',context)

## Display form in template
- in `create_groupchat.html` below `<h1>` add:
<!-- <form method="POST">
    {% csrf_token %}
    {{ form }}
    <button class="mt-2" type="submit">Create Group Chat</button>
</form> -->

## Add logic to save data to database
- in `create_groupchat` of views.py add:
if request.method == "POST":
    form = NewGroupForm(request.POST)
    if form.is_valid():
        new_groupchat = form.save(commit=False)
        new_groupchat.admin = request.user
        new_groupchat.save() 
        new_groupchat.members.add(request.user)
        return redirect('chatroom', new_groupchat.group_name)

## Add aesthetics to groupchat
- Add `chat_group` name to `chat_view` in views.py
include `'chat_group': chat_group,` in the `context` object

- in `a_rtchat/te,mplates/chat.html` add below `<wrapper>`:
<!-- {% if chat_group.groupchat_name %}
<h2>{{ chat_group.groupchat_name }}</h2>
{% endif %} -->

## Display members of a group chat
- within the `{% if other_user %} {% endif %}` tag add:
{% elif chat_group.groupchat_name  %}
<ul class="flex gap-4">
    {% for member in chat_group.members.all %}
    <li>
        <a href="{% url 'profile' member.username %}" class="flex flex-col text-gray-400 items-center justify-center w-20 gap-2">
            <img src="{{ member.profile.avatar }}" class="w-14 h-14 rounded-full object-cover" alt="{{ member.profile.name }}">
            {{ member.profile.name|slice:":10" }}
        </a>
    </li>
    {% endfor %}
</ul>

## Add logic for users to join by link
- in `chat_view` of `views.py` add:
if chat_group.groupchat_name:
    if request.user not in chat_group.members.all():
        chat_group.members.add(request.user)

## Add online tracker to chat group
- in `templates/chat.html`
- add `id="groupchat-members"` to groupchat online members code in `{% elif chat_group.groupchat_name %}`
- copy the `<ul>` element into `a_rtchat/templates/partials/online_count.html` partial
- wrap `<image>` in a div and add dot logic:
<div class="relative">
{% if member in chat_group.users_online.all %}
<div class="green-dot border-2 border-gray-800 absolute bottom-0 right-0"></div>
{% else %}
<div class="gray-dot border-2 border-gray-800 absolute bottom-0 right-0"></div>
{% endif %}
<img src="{{ member.profile.avatar }}" class="w-14 h-14 rounded-full object-cover" alt="{{ member.profile.name }}">
</div>

- inlcude the `chat_group` to the partial handle `online_cound_handler` in `consumers.py`:
include `chat_group` in the rendered contect `"chat_group": self.chatroom`

## Display newly created group in `Chats` dropdown
- root `templates/includes/header.html`:
- Under `<li>` with Public Chat add:
<!-- {% for chatroom in user.chat_groups.all %}
{% if chatroom.groupchat_name %}
<li>
    <a class="leading-5 text-right" href="{% url 'chatroom' chatroom.group_name %}">
        {{ chatroom.groupchat_name|slice:":30" }}
    </a>
</li>
{% endif %}
{% endfor %} -->

## add access Permission for only verified users
- in `chat_view()` of views.py revise `join-by-link` logic to: 
if chat_group.groupchat_name:
    if request.user not in chat_group.members.all():
        if request.user.emailaddress_set.filter(verified=True).exists():
            chat_group.members.add(request.user)
        else:
            messages.warning(request, "You need to verify your email to join the chat!")
            return redirect('profile-settings')
- import `from django.contrib import messages`


## Add admin page to change group name/ remove members
- in `templates/chat.html` revise code below `<wrapper>`:
<!-- {% if chat_group.groupchat_name %}
<div class="flex justify-between">
    <h2>{{ chat_group.groupchat_name }}</h2>
    {% if user == chat_group.admin %}
    <a href="{% url 'edit-chatroom' chat_group.group_name %}">
        <div class="p-2 bg-gray-200 hover:bg-blue-600 rounded-lg group">
            <svg class="fill-gray-500 group-hover:fill-white" width="16" height="16">
                <path
                    d="M11.013 1.427a1.75 1.75 0 0 1 2.474 0l1.086 1.086a1.75 1.75 0 0 1 0 2.474l-8.61 8.61c-.21.21-.47.364-.756.445l-3.251.93a.75.75 0 0 1-.927-.928l.929-3.25c.081-.286.235-.547.445-.758l8.61-8.61Zm.176 4.823L9.75 4.81l-6.286 6.287a.253.253 0 0 0-.064.108l-.558 1.953 1.953-.558a.253.253 0 0 0 .108-.064Zm1.238-3.763a.25.25 0 0 0-.354 0L10.811 3.75l1.439 1.44 1.263-1.263a.25.25 0 0 0 0-.354Z">
                </path>
            </svg>
        </div>
    </a>
    {% endif %} -->

- display the edit icon is `user` is chat_group.admin

## add edit chatroom path in `a_rtchat/urls.py`:
- `path('chat/edit/<chatroom_name>',chatroom_edit_view, name="edit-chatroom"),`

## Add `chatroom_edit_view` to views.py:
@login_required
def chatroom_edit_view(request, chatroom_name):
    return render(request, 'a_rtchat/chatroom_edit.html')

## Create `chatroom_edit.html` and add :
{% extends 'layouts/box.html' %}

{% block content %}
<h1>Edit Chat</h1>
{% endblock %}
- save and test render

## Create edit chatroom form in `forms.py`:
class ChatRoomEditForm(ModelForm):
    class Meta:
        model =ChatGroup
        fields =['groupchat_name']
        widgets = {
            'groupchat_name': forms.TextInput(attrs={
                'class':'p-4 text-lx font-bold mb-4', 
                'maxlength': '300', 
            })
        }

## Update `chatroom_edit.html` with:
<!-- <form method="post">
    {% csrf_token %}
    {{ form }}

    <div class="my-4">
    <h2>Members</h2>
    {% for member in chat_group.members.all %}
    <div class="flex justify-between items-center">
        <div class="flex items-center gap-2 py-2">
            <img class="w-14 h-14 rounded-full object-cover" src="{{ member.profile.avatar }}" />
            <div>
                <span class="font-bold">{{ member.profile.name }}</span> 
                <span class="text-sm font-light text-gray-600">@{{ member.username }}</span>
            </div>
        </div>
        
        {% if member != chat_group.admin %}
        <div class="inline-block pr-4">
            <input type="checkbox" name="remove_members" value="{{ member.id }}" class="relative p-5 cursor-pointer appearance-none rounded-md border after:absolute after:left-0 after:top-0 after:h-full after:w-full after:bg-[url('https://img.icons8.com/ffffff/32/multiply.png')] after:bg-center checked:bg-red-500 hover:ring hover:ring-gray-300 focus:outline-none" />
        </div>
        {% endif %}
    </div> 
    {% endfor %}
    </div>

    <button class="mt-2" type="submit">Update</button>
</form> -->


## Add logic to save edits to database
- in `chatroom_edit_view()` of views.py add:
chat_group = get_object_or_404(ChatGroup, group_name=chatroom_name)
if request.user != chat_group.admin:
    raise Http404()

form = ChatRoomEditForm(instance=chat_group)

if request.method == "POST":
    form = ChatRoomEditForm(request.POST, instance=chat_group)
    if form.is_valid():
        form.save()

        remove_members = request.POST.getlist('remove_members')
        for member_id in remove_members:
            member = User.objects.get(id=member_id)
            chat_group.members.remove(member)
            return redirect('chatroom',  chatroom_name)

- if post and valid then save
- get the ids of checked members 
- loop through list of members, get user object 
- removed for group
- return admin user to group

## Delete chat group
- add link with 'Delete Chatroom' text, pass `chatroom-delete` url and `chat_group.group_name` as group name arg
`<a href="{% url 'chatroom-delete' chat_group.group_name %}" class="inline-block flex justify-end mt-4 text-gray-400 hover:text-red-500" >Delete Chatroom</a>`
- Add path to `chatroom-delete` in urls.py as `path('chat/delete/<chatroom_name>',chatroom_delete_view, name="delete-chatroom"),`
- Add `chatroom_delete_view` view in views.py:
<!-- 
@login_required
def chatroom_delete_view(request, chatroom_name):
    return render(request, 'a_rtchat/chatroom_delete.html', context)
-->
-  Create the template: `chatroom_delete.html`
<!-- {% extends 'layouts/box.html' %}
{% block content %}
<h1>Delete this Chatroom?</h1>
{% endblock %} -->

- Add delete logic to `chatroom_delete_view()`
<!-- @login_required
def chatroom_delete_view(request, chatroom_name):

    chat_group = get_object_or_404(ChatGroup, group_name=chatroom_name)
    if request.user != chat_group.admin:
        raise Http404()

    if request.method == "POST":
        chat_group.delete()
        messages.success(request, 'Chatroom deleted')
        return redirect('home')

    context = {
            'chat_group': chat_group
        }
    return render(request, 'a_rtchat/chatroom_delete.html',context) -->

- Add elements below the `<h1>` element in `chatroom_delete.html`:
<!-- <h2>"{{ chat_group.groupchat_name }}"</h2>
<form method="POST">
    {% csrf_token %}
    <button type="submit" class="button-red mt-4">Yes, delete</button>
    <a href="{{ request.META.HTTP_REFERER }}" class="button button-gray ml-1">Cancel</a>
</form> -->
- `href="{{ request.META.HTTP_REFERER }}"` returns user to last visited page
- Save, refresh and test `delete`

## Add `leave group` feature
- in `chat.hmtl` add:
<!-- {% if chat_group.members.exists %}
<a href="{% url 'chatroom-leave' chat_group.group_name %}">
    {% include 'a_rtchat/partials/modal_chat_leave.html' %}
</a>
{% endif %} -->
- This uses a modal display
- Create a partial `modal_chat_leave.html` and add:
<!-- <div x-data="{ modal_open: false }">
    <div x-show="modal_open">
        <div class="fixed inset-0 bg-gray-800 bg-opacity-80 z-50"></div>
        <div class="fixed inset-0 z-50">
            <div class="flex min-h-full justify-center items-center p-6">
                <div @click.away="modal_open = false" class="rounded-lg bg-white text-left shadow-xl">
                    <h1>Leave this chat?</h1>
                    <form method="POST" action="{% url 'chatroom-leave' chat_group.group_name %}">
                        {% csrf_token %}
                        <button type="submit" class="button-red mt-4">Yes, I want to leave</button>
                        <a @click.away="modal_open = false" class="button button-gray ml-1 cursor-pointer">Cancel</a>
                    </form>
                </div>
            </div>
        </div>
    </div>
</div> -->
- NB: functionlity of this form may be missing 
- Else use a page `chatroom_leave.html`:
<!-- {% extends 'layouts/box.html' %}

{% block content %}

<h1>Leave this Chatroom?</h1>

<h2>"{{ chat_group.groupchat_name }}"</h2>

<form method="POST">
    {% csrf_token %}
    <button type="submit" class="button-red mt-4">Yes, I want to leave</button>
    <a href="{{ request.META.HTTP_REFERER }}" class="button button-gray ml-1">Cancel</a>
</form>

{% endblock %} -->
- Create url `chatroom-leave` in `urls.py`:
`path('chat/leave/<chatroom_name>',chatroom_leave_view, name="chatroom-leave"),`

- create the view `chatroom_leave_view` in `views,py`:
<!-- @login_required
def chatroom_leave_view(request, chatroom_name):

    chat_group = get_object_or_404(ChatGroup, group_name=chatroom_name)
    if request.user not in chat_group.members.all():
        raise Http404()

    if request.method == "POST":
        chat_group.members.remove(request.user)
        messages.success(request, 'You left the Chat')
        return redirect('home')

    context = {
            'chat_group': chat_group
        }
    return render(request, 'a_rtchat/chatroom_leave.html',context) -->

# Activity monitoring - Live tracker

## Create a new group in DB
- create a new group manually in admin panel - `online-status`
- add `user-counter` to the `header.html` template below logo:
- `<div id="online-user-count"></div>`
- add classes to parent div `flex item-center`

## Add new websocket connection
- within `header.html` within 1st `<li>` element add attributes:
hx-ext="ws"
ws-connect="/ws/online-status/"

## Create ws path in `routing.py` ~ `urls.py`:
- add `path("ws/online-status/", OnlineStatusConsumer.as_asgi()),`

## Create consumer class in `consumers.py` ~ `views.py`:
class OnlineStatusConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
- refresh page and check for ws handshake and connect
- Get user from the scope
- define `group_name`, created as `online-status`
- get a `group` object using the `group_name`
- if user is not already in the `users_online`, add them to database
- To connect to connect user all users in real-time, add channel layer using `async_to_sync()`
- after `self.accept()` add a new fn `self.online_status()` to update online statuses
- add `self.disconnect()` method, if user is in users_online, remove them
- Remove user from the channel_layer using `self.channel_layer.group_discard` then run update of online users `online_status()`
- define `online_status_handler` that updates the front end 
- get all online users and exlude current user
- pass the `online_users` var to content, convert  to render strong and send it.
Full code:
class OnlineStatusConsumer(WebsocketConsumer):

    def connect(self):
        self.user = self.scope['user']
        self.group_name = 'online-status'
        self.group = get_object_or_404(ChatGroup, group_name=self.group_name)

        if self.user not in self.group.users_online.all():
            self.group.users_online.add(self.user)
        
        async_to_sync(self.channel_layer.group_add)(
            self.group_name, self.channel_name
        )

        self.accept()
        self.online_status()
    
    def disconnect(self, close_code):
        if self.user in self.group.users_online.all():
            self.group.users_online.remove(self.user)
        
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name, self.channel_name
        )
        self.online_status()
    
    def online_status(self):
        event ={
            'type': 'online_status_handler'
        }
        async_to_sync(self.channel_layer.group_send)(
            self.group_name, event
        )

    def online_status_handler(self,event):
        online_users = self.group.users_online.exclude(id=self.user.id)
        context = {
            'online_users': online_users,
        }

        html = render_to_string("a_rtchat/partials/online_status.html", context=context)
        self.send(text_data=html)

## Create `online_status.html` partial in app templates
- create `a_rtchat/templates/partials/online_status.html` and add code:
<!-- <div id="online-user-count">
    {% if online_users %}
    <span class="bg-red-500 rounded-lg pt-1 pb-2 text-white text-sm ml-4">
    {{ online_users.count }} online
    </span>
    {% endif%}
</div> -->

## Display if user if active in a chatroom
- in `online_status_handler()` of `OnlineStatusConsumer()` of `consumers.py`
- add `public_chat` var to get all online user in this group excluding current user
`public_chat_users = ChatGroup.objects.get(group_name='public-chat').users_online.exclude(id=self.user.id)`
- set `online_in_chats` to True if `public_chat_users` has contents, else false, pass `online_in_chats` to context 
- Issue:the update does not work because ws connection is applied after partials have been passed
- Solution: move the ws-connection of the `footer` element for logged in users, added in `base.html`:
<!-- {% if user.is_authenticated %}
<footer hx-ext="ws" ws-connect="/ws/online-status/"></footer>
{% endif %} -->
- **For private chats:** create a list for `private_chats_with_users`, check all members current users is part of, then filter `is_private = True` chats and exlucde current user
`my_chats = self.user.chat_groups.all()`
`private_chats_with_users = [chat for chat in my_chats.filter(is_private=True) if chat.users_online.exclude(id=self.user.id)]`
- include `private_chats_with_users` to `online_in_chats` condition
- **For group chats:** create a list for `group_chats_with_users`, check all members current users is part of, then filter `groupchat_name__isnull= False` chats and exlucde current user
`group_chats_with_users = [chat for chat in my_chats.filter(groupchat_name__isnull= False) if chat.users_online.exclude(id=self.user.id)]`
- include `group_chats_with_users` to `online_in_chats` condition

## Add online status indicator on dropdown list, show in which chat other users online
- Copy the `<ul>` element for the Chat menu dropdown and paste in `online_status.html` partial
- replace the full `<ul>` with `<ul id="chats-list"></ul>`, ensure id is defined
- For `public chat`, in `online_status.html`, revise in `<li>` element in loop to:
<!-- <li class="relative">
    {% if public_chat_users %}
    <div class="green-dot absolute top-1 left-1"></div>
    {% else %}
    <div class="graylight-dot absolute top-1 left-1"></div>
    {% endif %}
    <a href="{% url 'home' %}">Public Chat</a>
</li> -->
- For `private` and `group` chat, in `online_status.html`, revise in `<li>` element in loop to:
<!-- <li class="relative">
    {% if chatroom.users_online.all and user not in chatroom.users_online.all or chatroom.users_online.count > 1 %}
    <div class="green-dot absolute top-1 left-1"></div>
    {% else %}
    <div class="graylight-dot absolute top-1 left-1"></div>
    {% endif %}
    <a $relevant_content$ </a>
</li> -->

## Add online status indicator on the avatar of users in chatroom
- in the `online_count_handler` of `ChatroomConsumer()` of `consumers.py` add:
`chat_messages = ChatGroup.objects.get(group_name=self.chatroom_name).chat_messages.all()[:30]`
- get the last 30 messages in a chatroom, 
- extract user id from each message, use `set()` to get unique id's only
- `author_ids = set([message.author.id for message in chat_messages])`
- using the ids list `author_ids`, get the user objects `users = User.objects.filter(id__in=author_ids)`
- add `users` to the context
- add indicator to the partial `online_count.html` add:
<!-- {% for user in users %}
    {% if user in chat_group.users_online.all %}
    <div id="user-{{ user.id }}" class="green-dot border-2 border-gray-800 absolute -bottom-1 -right-1"></div>
    {% else %}
    <div id="user-{{ user.id }}" class="gray-dot border-2 border-gray-800 absolute -bottom-1 -right-1"></div>
    {% endif %}
{% endfor %} -->
- add id to differentiate between dusers in a chat

- in `chat_messages.html` template, find user avatar:
- wrap the image tag displaying avatar in a div with class 'relative'
<!-- <div class="relative">
<div id="user-{{ message.author.id }}"></div>  
<img class="w-8 h-8 rounded-full object-cover" src="{{ message.author.profile.avatar }}">
</div> -->

- in the `message_handler` of `ChatroomConsumer()` of `consumers.py` add:
- add`'chat_group': self.chatroom` to the context
- add indicator to the partial `chat_message_p.html` at the bottom:
<!-- {% with user=message.author %}
    {% if user in chat_group.users_online.all %}
    <div id="user-{{ user.id }}" class="green-dot border-2 border-gray-800 absolute -bottom-1 -right-1"></div>
    {% else %}
    <div id="user-{{ user.id }}" class="gray-dot border-2 border-gray-800 absolute -bottom-1 -right-1"></div>
    {% endif %}
{% endwith %} -->
- 

# Sending files 

## Update model class to allow file uploads
- in `models.py`:
- add `blank=True, null=True` to the body field
`body = models.CharField(max_length=300, blank=True, null=True)`
- add field: `file = models.FileField(upload_to='files/', blank=True, null=True)`
- run `makemigrations` and `migrate`

## Upodate html templates
- Update the template `chat.html`
- in the parent div of `<form>` add classes `flex-col gap-4 `
- add another form:
<!-- <form id="chat_file_form" enctype="multipart/form-data" class="flex items-center w-full"
hx-post="{% url 'chat-file-upload' chat_group.group_name %}"
hx-target="#chat_messages"
hx-swap="beforeend
_="on htmx:beforeSend reset() me">
    {% csrf_token %}
    <input type="file" name="file" id="id_file" class="!bg-transparent text-gray-400">
    <button type="submit" class="whiitespace-nowrap !text-sm !py-3 !px-4 h-fit">Submit File</button>
</form> -->
- form send file to `'chat-file-upload'` urls passing `chatroom name` as arg

## Add urls `chat-file-upload`
- add path to app `urls.py`: `path('chat/fileupload/<chatroom_name>',chat_file_upload, name="chat-file-upload"),`

## create view `chat_file_upload`
- create `chat_file_upload` view in `views.py`:
- get the chatgroup using the pssed chatroom_name: `chat_group = get_object_or_404(ChatGroup, group_name=chatroom_name)`
- Check if reqest is htmx post and has files attached: `request.htmx and request.FILES`
- create a new message to the Group chat:
file = request.FILES['file']
    message = GroupMessage.objects.create(
        file= file,
        author = request.user,
        group = chat_group,
    )
- To update/broadcast messae to the users in the chatroom - call channels layers 
- import: `from channels.layers import get_channel_layer`
- get the channel_layer `channel_layer = get_channel_layer()`
- create an event to be run by `message_handler()` from consumers.py
- call the `group_send` function in the async_to_sync()
- add return `HttpResponse`, to prevent errors
- import `from asgiref.sync import async_to_sync`
- import `from django.http import HttpResponse`

## more template adjustment
- Adjust template code to display files in `chat_message.html`:
- replace `{{ message.body }}` with `{% include "a_rtchat/partials/message_content.html" %}` 
- replace in two places within `chat_message.html` template
- create partial file `message_content.html` with code:
<!-- {% if message.body %}
    <span>{{ message.body }}</span>
{% elif message.file %}
    <img src="{{ message.file.url }}" class="max-w-72 min-w-8">
{% endif%} -->
- to adjust auto scroll, add `setTimeout` to `scrollToBottom()` js code in `chat.html` revised code:
function scrollToBottom(time=0) {
        setTimeout(function() {
            const container = document.getElementById('chat_container');
            container.scrollTop = container.scrollHeight;
        }, time);
    }
- add timeout delay to `scrollToBottom()` in the partial  `chat_message_p.html`:
`<script>scrollToBottom(100)</script>`

## Group message: admin panel
- in the admin panel, file show up as none, change to show filename in `models.py`
- import `import os`
- add `filename` property:
@property
def filename(self):
    if self.file:
        return os.path.basename(self.file.name)
    else:
        return None
- refresh and test

## Uploading non-image files
- in the `GroupMessage()` of `models.py` add property:
@property
def is_image(self):
    if self.filename.lower().endswith(('.jpg','jpeg','.png','.gif','.svg','.webp')):
        return True
    else:
        False
- OR user `PIL`:
@property
def is_image(self):
    try:
        image = Image.open(self.file)
        image.verify()
        return True
    except:
        return False

## Add condition to `message_content.html`
- in the `{% elif message.file %}`:
<!-- {% if message.is_image %}
    <img src="{{ message.file.url }}" class="max-w-72 min-w-8">
{% else %}
    &#x1F4Ce; <a class="cursor-pointer italic hover:underline" href="{{ message.file.url }}" download>{{ message.filename }}</a>
{% endif%} -->
- `downlaod` attribute allow file to downloaded on click

# Social logins

## Create social logins template
- create `a_users/templates/social_logins.html`
- add code: `https://github.com/andyjud/social-logins/blob/main/buttons.html`
- include this tempalte in the root template for login and signup
- in root `templates/accounts/login.html` and `.../signup.html`:
- Remove the code below``:
{% if SOCIALACCOUNT_ENABLED %}
    {% include "socialaccount/snippets/login.html" with page_layout="entrance" %}
{% endif %}
- Replace with code: `{% include 'a_users/social_logins.html '%}`
- refresh page to see the buttons

## Setup all Auth
- install:
`pip install "django-allauth[socialaccount]"`
`pip3 freeze --local > requirements.txt`

## Google login/signup
- add `'allauth.socialaccount.providers.google',` to `INSTALLED_APPS`, added below `'allauth.socialaccount'`
- add `SOCIALACCOUNT_PROVIDERS` below `INSTALLED_APPS`
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'APP': {
            'client_id': '',
            'secret': '',
        },
    },
}
- Add env variables: `OAUTH_GOOGLE_CLIENT_ID` and `OAUTH_GOOGLE_SECRET`
- go to `https://console.cloud.google.com/`
- Create new project, pass project name e.g `Awesome Django App` - ensure project is selected
- navigate to `APIs and services`
- Click `OAuth consent screen` and click `Get started`
- Under `Audience` select `External`
- Under `Contact Info` pass your email address
- Agree to policies and click `Create`
- On the left panel (downward arrow), click `Branding`
- Add logo for App
- Add App domain as will be displayed to the user
- Add links to `home page`, `privacy policy` and `Terms of Service` - could be dummy for dev
- Add domain e.g. `example.com` and click `Save`
- On the left panel (downward arrow), click `Clients`
- Click `Create client`
- Application type: `Web application`
- Add Name for client (internal use only)
- Add URI for `Authorised redirect URIs`:
`http://127.0.0.1:8000/accounts/google/login/callback/` (127.0.0.1 or localhost)
- **NB:** replace `http://127.0.0.1:8000` with `https://warriors-chat-ca1113b90a31.herokuapp.com/`
- Click `Create`
- Get the values and update `OAUTH_GOOGLE_CLIENT_ID` and `OAUTH_GOOGLE_SECRET` variale in `env.py`
- in `a_users/template/social_logins.html`, add the url link to href attr for the `Google` link element:
`href="{% provider_login_url 'google' %}"`
- at the top of the page: `{% load socialaccount %}`
- Add `SOCIALACCOUNT_LOGIN_ON_GET=True` at the bottom of `settings.py` to go directly to consent screen
- refresh and test

## Modify redirect after login - `adapters.py`:
- create file `a_users/adapters.py`:
from allauth.account.adapter import DefaultAccountAdapter
from django.shortcuts import resolve_url

class CustomAccountAdapter(DefaultAccountAdapter):
    def get_signup_redirect_url(self, request):
        return resolve_url("profile-onboarding")
- Add `adapters` to `settings.py` at the bottom of file:
`ACCOUNT_ADAPTER = "a_users.adapters.CustomAcoountAdapter"`
- Refresh and test

## Define `SCOPE` and `AUTH_PARAMS` in social app conifg `SOCIALACCOUNT_PROVIDERS`:
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'APP': {
            'client_id': os.environ.get("OAUTH_GOOGLE_CLIENT_ID"),
            'secret': os.environ.get("OAUTH_GOOGLE_SECRET"),
        },
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
            'prompt': 'consent',
        }
    },
}

## connecting exisiting user - social login
- Add `SOCIALACCOUNT_AUTO_SIGNUP = True` at file bottom `settings.py`
- `SOCIALACCOUNT_AUTO_SIGNUP = True` trust that email has been verified by social account service
- `ACCOUNT_UNIQUE_EMAIL = True` no duplicate emails
- `SOCIALACCOUNT_EMAIL_AUTHENTICATION = True` trust email is valid and authenticaed
- `SOCIALACCOUNT_EMAIL_AUTHENTICATION_AUTO_CONNECT = True` creates a link between social account provider and user account
- `SOCIALACCOUNT_EMAIL_VERIFICATION = "none"` - ensure no verification is require for social accounts 
- To automatically verify socialaccount login email - in `adapters.py`:
class SocilaAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        email = sociallogin.account.extra_data.get("email")

        if not email:
            return
        
        if sociallogin.is_existing:
            user = sociallogin.user
            email_address, created = EmailAddress.objects.get_or_create(user=user,email=email)
            if not email_address.verified:
                email_address.verified = True
                email_address.save()
    

    def save_user(self, request, sociallogin, form=None):
        user= super().save_user(request, sociallogin, form)
        email= user.email
        email_address, created = EmailAddress.objects.get_or_create(user=user,email=email)
        if not email_address.verified:
            email_address.verified = True
            email_address.save()
        
        return user
- `sociallogin.is_existing` -checks if user is already associated with a social account
- add this adapter to `settings.py`: 

## GitHub login/signup
- add `'allauth.socialaccount.providers.github',` to `INSTALLED_APPS`, added below `'allauth.socialaccount'`
- Add config object inthe `SOCIALACCOUNT_PROVIDERS`:
'github': {
    'APP': {
        'client_id': os.environ.get("OAUTH_GITHUB_CLIENT_ID"),
        'secret': os.environ.get("OAUTH_GITHUB_SECRET"),
    },
    'AUTH_PARAMS': {
        'prompt': 'consent',
    }
},
- Define `OAUTH_GITHUB_CLIENT_ID` and `OAUTH_GITHUB_SECRET` in the `env.py`
- go to `https://github.com/settings/apps`
- click on `OAuth Apps` then `New OAuth app`
- Application name: `Awesome Django App` 
- Homepage IRL: `https://awesomesjango.com`
- Authorization callback userl URL:
`http://127.0.0.1:8000/accounts/github/login/callback/`
- **NB:** replace `http://127.0.0.1:8000` with `https://warriors-chat-ca1113b90a31.herokuapp.com/`
- Click `Register Application`
- Copy `Client ID` and `Client Secret`
- Click 'Generate a new client secret' and copy the secrect code
- Add logo (if required)
- click `Update application`
- in `a_users/template/social_logins.html`, add the url link to href attr for the `GitHub` link element:
`href="{% provider_login_url 'github' %}"`


## (X) Twitter login/signup
- add `'allauth.socialaccount.providers.twitter',` to `INSTALLED_APPS`, added below `'allauth.socialaccount'`
- Add config object inthe `SOCIALACCOUNT_PROVIDERS`:
'twitter': {
    'APP': {
        'client_id': os.environ.get("OAUTH_TWITTER_CLIENT_ID"),
        'secret': os.environ.get("OAUTH_TWITTER_SECRET"),
    },
}, 
- Define `OAUTH_TWITTER_CLIENT_ID` and `OAUTH_TWITTER_SECRET` in the `env.py`
- go to `https://developer.x.com/` then click `Developer Portal`
- sign-up for free account to get to `https://developer.x.com/en/portal/dashboard`
- edit default app, add app name e.g.`Awesome Django Chat App`
- Click on `Keys and tokens` tab
- in the `Consumer Keys` section and besides `API Key and Secret` click `Generate`, Copy `token ID` and `token Secret`into env.py
- Back to  `Settings` tab, under `User Authentication settings` click `setup`
- `App permissions:` Read, click the `Request email from users`
- `Type of App:` Web App, for OAuth 2.0 
- `App info`, for Callback URI: `http://127.0.0.1:8000/accounts/twitter/login/callback/`
- **NB:** replace `http://127.0.0.1:8000` with `https://warriors-chat-ca1113b90a31.herokuapp.com/`
- Add `website URL` e.g. `https://awesomedjangoapp.com`
- Add `Terms of Service URL` e.g. `https://awesomedjangoapp.com`
- Add `website URL` e.g. `https://awesomedjangoapp.com`
- Save all changes
- Add 
- in `a_users/template/social_logins.html`, add the url link to href attr for the `Twitter` link element:
`href="{% provider_login_url 'twitter' %}"`
- Refresh and test
- for error : `Third-Party Login Failure`
- Add `SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")` to the `setting.py`

## Facebook login/signup
- add `'allauth.socialaccount.providers.facebook',` to `INSTALLED_APPS`, added below `'allauth.socialaccount'`
- Add config object inthe `SOCIALACCOUNT_PROVIDERS`:
'facebook': {
    'APP': {
        'client_id': os.environ.get("OAUTH_FACEBOOK_CLIENT_ID"),
        'secret': os.environ.get("OAUTH_FACEBOOK_SECRET"),
    },
    'AUTH_PARAMS': {
        'auth_type': 'reauthenticate',
    }
}, 
- Define `OAUTH_FACEBOOK_CLIENT_ID` and `OAUTH_FACEBOOK_SECRET` in the `env.py`
- go to `https://developer.facebook.com/`, login,  then click `Get Started`
- go through registration and do all verifications
- Click `My Apps` then `Create App`
- Application name: `Awesome Django App`
- Under `Use cases` click `Other`
- NB: if there's an existing business you'd click `Authenticate and request data from users with Facebook login`
- Under `Business`, select `consumers`
- next screen click `Create App`, app created
- Navigate to `App Settings` on the left panel
- Select `Basic`
- Copy `App ID` and `App secret` values to env.py
- Under `App domains` add: `https://warriors-chat-ca1113b90a31.herokuapp.com/`
- Under `Privacy Policy URL` add: `https://awesomedjangoapp.com`
- Under `Terms of Service URL` add: `https://awesomedjangoapp.com`
- Under `Data deletion URL` add: `https://example.com` must be a valid url path (GB will test it)
- Select `Category` and upload app image
- In a real life app, you would add business info and verify (The General Data Protection Regulation (GDPR) )
- At the bottom click `+ Add Platform` and select `Website` then `next`
- Under `Website` add the site URL `https://awesomedjangoapp.com` the `Save changes`
- In `Development` no need to set callback URI
- in `a_users/template/social_logins.html`, add the url link to href attr for the `Facebook` link element:
`href="{% provider_login_url 'facebook' %}"`
- **Error:** `Fix Facebook Login Error Can't load URL`
- In app `Awesome Django App` portal on `https://developer.facebook.com/`
- On the left panel, click `Add Product` then `Facebook Login` > `Set up`
- Select `Web` then add URL for your app `https://warriors-chat-ca1113b90a31.herokuapp.com/` then `save`
- Under `Facebook Login` , click `settings`
- in the `Client OAuth settings` section, add callback URI in the `Valid OAuth Redirect URIs` add:
`https://warriors-chat-ca1113b90a31.herokuapp.com/accounts/facebook/login/callback/`
- cannot be run on `http//127.0.0.1:8000`, only `https` allowed

- **Error:** for live apps, the redirect return `http` instead of `https` add this line for fix
`ACCOUNT_HTTP_PROTOCOL = 'https'`

