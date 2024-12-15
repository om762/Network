from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext as _
import random

def generate_random_color():
    return random.choice([
        "#2C3E50", "#34495E", "#1ABC9C", "#16A085", "#E74C3C", 
        "#C0392B", "#8E44AD", "#9B59B6", "#2980B9", "#3498DB", 
        "#2ECC71", "#27AE60", "#F39C12", "#F1C40F", "#D35400", 
        "#E67E22", "#BDC3C7", "#95A5A6", "#7F8C8D"
    ])
class User(AbstractUser):
    color = models.CharField(max_length=7, default=generate_random_color)


class Post(models.Model):
    poster = models.ForeignKey("network.User", verbose_name=_("Post by"), on_delete=models.CASCADE, related_name='posts')
    content = models.TextField(_("Content"))
    liked_by = models.ManyToManyField("network.User", verbose_name=_("Liked by"))
    post_at = models.DateTimeField(_("Post Date"), auto_now=True)
    update_at = models.DateField(_("Last Update"), auto_now_add=True)

    def toggle_like(self, user):
        if self.liked_by.filter(id=user.id).exists():
            self.liked_by.remove(user)
        else:
            self.liked_by.add(user)
    
    def likes(self):
        return self.liked_by.count()
    
    def is_liked_by(self, user):
        return self.liked_by.filter(id=user.id).exists()
    
    def comment_count(self):
        return self.comments.count()

class Comment(models.Model):
    comment_on = models.ForeignKey("network.Post", verbose_name=_("Post"), on_delete=models.CASCADE, related_name='comments')
    commenter = models.ForeignKey("network.User", verbose_name=_("Commenter"), on_delete=models.CASCADE, related_name='comments')
    comment = models.TextField(_("Comment"))
    commented_at = models.DateTimeField(_("Comment Date"), auto_now=True)
    
    def __str__(self):
        return f'"{self.comment}" by {self.commenter}'