from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    profile_photo = models.ImageField(upload_to='profiles/')
    phone = models.CharField(max_length=13)

    def image_tag(self):
        return u'<img src="/%s" />' % (self.profile_photo.url if self.profile_photo else 'media/profiles/placeholder.jpg')
    image_tag.short_description = 'Image'
    image_tag.allow_tags = True

    def __str__(self):
        return "%s's profile" % self.user

class MatchUp(models.Model):
    match_maker = models.ForeignKey(User, related_name="match_maker_matchup")

    address = models.CharField(max_length=100)

    date_date = models.DateTimeField()

    him = models.ForeignKey(User, related_name="him_matchup", null=True, blank=True)
    her = models.ForeignKey(User, related_name="her_matchup", null=True, blank=True)

    his_phone = models.CharField(max_length=13)
    her_phone = models.CharField(max_length=13)

    him_confirmed = models.BooleanField(default=False)
    her_confirmed = models.BooleanField(default=False)

    latitude = models.FloatField()
    longitude = models.FloatField()

    creation_date = models.DateTimeField(auto_now_add=True)

    in_progress = models.BooleanField(default=True)
