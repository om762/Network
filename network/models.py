from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext as _


class User(AbstractUser):
    pass

class Post(models.Model):
    poster = models.ForeignKey("network.User", verbose_name=_("Post by"), on_delete=models.CASCADE, related_name='posts')
    content = models.TextField(_("Content"))
    liked_by = models.ManyToManyField("network.User", verbose_name=_("Liked by"))
    post_at = models.DateField(_("Post Date"), auto_now=True)
    update_at = models.DateField(_("Last Update"), auto_now_add=True)

