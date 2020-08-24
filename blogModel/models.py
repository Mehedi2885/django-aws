from django.db import models
from django.utils.encoding import smart_str
from django.utils import timezone
from .validator import valid_mehedi
from django.utils.text import slugify
from django.db.models.signals import pre_save, post_save

# create your models here.

PUBLISH_CHOICES = [
    ('draft', 'Draft'),
    ('publish', 'Publish'),
    ('private', 'Private'),
]


class PostModelQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(active=True)

    def post_item_by_title(self, value):
        return self.filter(title__icontains=value)


class PostModelManager(models.Manager):
    def get_queryset(self):
        return PostModelQuerySet(self.model, using=self._db)

    def all(self, *args, **kwargs):
        # qs = super(PostModelManager, self).all(*args, **kwargs).active()  # .filter(active=True)
        qs = self.get_queryset().active()
        print(qs)
        return qs


class PostModel(models.Model):
    title = models.CharField(max_length=150,
                             verbose_name='Post Title',
                             unique=True,
                             error_messages={
                                 'unique': 'This title is not unique, please try again',
                                 'blank': 'This title is not full, please try again'
                             },
                             help_text='Must be an unique title'
                             )
    slug = models.SlugField(null=True, blank=True)
    active = models.BooleanField(default=True)
    content = models.TextField(null=True, blank=True)
    publish = models.CharField(max_length=129, choices=PUBLISH_CHOICES, default='publish')
    view_count = models.IntegerField(default=0)
    publish_date = models.DateField(auto_now=False, auto_now_add=False, default=timezone.now)
    author_email = models.EmailField(max_length=240, validators=[valid_mehedi], null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    """ Overriding existing objects attribute with other, so objects will not work anymore"""
    # objects = PostModelManager()
    other = PostModelManager()

    # def save(self, *args, **kwargs):
    #     pass
    #     # if not self.slug and self.title:
    #     #     self.slug = slugify(self.title)
    #     super(PostModel, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'

    def __str__(self):
        return smart_str(self.title)


def blog_post_pre_save_receiver(sender, instance, *args, **kwargs):
    print('Before save')
    if not instance.slug and instance.title:
        instance.slug = slugify(instance.title)


pre_save.connect(blog_post_pre_save_receiver, sender=PostModel)


def blog_post_post_save_receiver(sender, instance, created, *args, **kwargs):
    print('After save')
    print(created)
    if created:
        if not instance.slug and instance.title:
            instance.slug = slugify(instance.title)
            instance.save()


post_save.connect(blog_post_post_save_receiver, sender=PostModel)
