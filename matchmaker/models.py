from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    profile_photo = models.ImageField(upload_to='profiles/')

    def image_tag(self):
        return u'<img src="%s" />' % self.profile_photo.url
    image_tag.short_description = 'Image'
    image_tag.allow_tags = True

    def __str__(self):
        return "%s's profile" % self.user
