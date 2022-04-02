from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator
from django.conf import settings

# Create your models here.

class Album(models.Model):
    name = models.CharField(max_length=128, verbose_name='Name')
    description = models.TextField(max_length=1024, null=True, blank=True, verbose_name='Description')
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="albums")
    created_at = models.DateTimeField(auto_now_add=True)
    is_private = models.BooleanField(default=False, verbose_name='Private')
    favorite = models.ManyToManyField(get_user_model(), related_name="favorite_albums", verbose_name='Favorite albums', blank=True)

    class Meta:
        db_table = 'albums'
        verbose_name = 'Album'
        verbose_name_plural = 'Albums'

    def __str__(self):
        return f'{self.name}: {self.description}'

class Photo(models.Model):
    photo = models.ImageField(upload_to='pics', verbose_name="Photo")
    title = models.CharField(max_length=256, verbose_name="Title")
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="photos")
    album = models.ForeignKey('webapp.Album', on_delete=models.CASCADE,related_name="photos", null = True, blank = True)
    is_private = models.BooleanField(default=False, verbose_name='Private')
    favorite = models.ManyToManyField(get_user_model(), related_name="favorite_photos", verbose_name='Favorite photos', blank=True)

    class Meta:
        db_table = 'photos'
        verbose_name = 'Photo'
        verbose_name_plural = 'Photos'

    def __str__(self):
        return f'{self.author}:{self.title}'


class Link(models.Model):
    photo = models.OneToOneField('webapp.Photo', on_delete=models.CASCADE, related_name='link')
    link = models.CharField(max_length=200)

    class Meta:
        verbose_name='Link'
        verbose_name_plural='Links'

    def __str__(self):
        return f'{self.link}'