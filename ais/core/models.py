from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import JSONField
from django.utils.translation import gettext as _
from django.db.models.signals import post_save
from firebase_admin import auth
from .firebase import db
import uuid


class User(AbstractUser):
    uuid = models.CharField(max_length=100,
                            blank=True,
                            unique=True,
                            default=uuid.uuid4)


# def post_save_receiver(sender, instance, created, **kwargs):
#     additional_claims = {
#         'premiumAccount': True,
#     }
#     custom_token = auth.create_custom_token(str(instance.uuid),
#                                             additional_claims)
#     doc_ref = db.collection('ais-users').document(str(instance.uuid))
#     doc_ref.set({
#         'username': instance.username,
#     })


# post_save.connect(post_save_receiver, sender=User)


class SentimentResult(models.Model):
    text = models.CharField(max_length=280)
    polarity = models.DecimalField(max_digits=6, decimal_places=5)
    subjectivity = models.DecimalField(max_digits=6, decimal_places=5)
    compound = models.DecimalField(max_digits=6, decimal_places=5)
    positive = models.DecimalField(max_digits=6, decimal_places=5)
    negative = models.DecimalField(max_digits=6, decimal_places=5)
    neutral = models.DecimalField(max_digits=6, decimal_places=5)

    question = models.ForeignKey('Question',
                                 related_name='results',
                                 on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('Result')
        verbose_name_plural = _('Results')

    def __str__(self):
        return f'\
            Polarity: {self.polarity}, \
            Subjectivity: {self.subjectivity}, \
            Compound: {self.compound}, \
            Positive: {self.positive}, \
            Negative: {self.negative}, \
            Neutral: {self.neutral}'


class Question(models.Model):
    query = models.CharField(max_length=400)
    user = models.ForeignKey(User,
                             related_name='questions',
                             on_delete=models.CASCADE,)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Question')
        verbose_name_plural = _('Questions')

    def __str__(self):
        return self.query
