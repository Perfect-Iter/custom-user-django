from django.db import models
from user.models import CustomUser

# Create your models here.
class UserProfile(models.Model):

    user = models.ForeignKey(CustomUser, related_name="")
    

    class Meta:
        verbose_name = _("user_profile")
        verbose_name_plural = ("user_profiles")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("_detail", kwargs={"pk": self.pk})


