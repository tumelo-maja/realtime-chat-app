from django.db import models
from django.contrib.auth.models import User
from django.templatetags.static import static
from cloudinary.models import CloudinaryField

class Profile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = CloudinaryField('image', default='placeholder')
    displayname= models.CharField(max_length=20, null=True,blank=True)
    info = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.user}"
    
    @property
    def name(self):
        if self.displayname:
            name =self.displayname
        else:
            name = self.user.username
        return name

    @property
    def avatar(self):
        try:
            avatar =self.image.url
        except:
            avatar = static('images/avatar.svg')
        return avatar
