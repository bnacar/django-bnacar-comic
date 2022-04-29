from django.db import models
from django.utils.text import slugify

# Create your models here.
class Tag(models.Model):
    name = models.CharField(max_length=255, default='WOOP', unique=True)
    slug = models.CharField(max_length=255, default='woop', unique=True)
    info = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Tag, self).save(*args, **kwargs)

class Series(models.Model):
    title = models.CharField(max_length=255, default='WOOP WOOP WOOP', unique=True)
    slug = models.CharField(max_length=255, default='woopwoopwoop', unique=True)
    blurb = models.TextField()
    tags = models.ManyToManyField(Tag)
    def __str__(self):
        return self.title

class Episode(models.Model):
    num = models.IntegerField()
    comic = models.ForeignKey(Series, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, related_name='tags')
    imgFile = models.FileField(max_length=255)
    notes = models.TextField(null=True, blank=True)
    def __str__(self):
        return self.comic.title + ' ' + str(self.num)
