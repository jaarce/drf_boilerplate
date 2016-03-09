from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):

    user = models.OneToOneField(User)
    avatar = models.CharField(max_length=500, null=True, blank=True)
    social_account = models.OneToOneField("SocialAccount",
                                          null=True,
                                          blank=True,
                                          help_text="(Facebook ID, Twitter ID, Google+ ID)")

    def __unicode__(self):
        return self.user.username


class SocialAccount(models.Model):
    network_id = models.CharField(max_length=500, default=None)
    network_name = models.CharField(max_length=100,
                                    default=None,
                                    choices=(("Facebook", "Facebook"),
                                             ("Google+", "Google+"),
                                             ("Twitter", "Twitter")))

    def __unicode__(self):
        return self.network_id
