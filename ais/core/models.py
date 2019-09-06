from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _


class Question(models.Model):
    query = models.CharField(max_length=400)
    user = models.ForeignKey(get_user_model(),
                             related_name='questions',
                             on_delete=models.CASCADE,)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Question')
        verbose_name_plural = _('Questions')

    def __str__(self):
        return self.query
