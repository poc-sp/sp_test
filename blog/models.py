# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
# Create your models here.
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)
    added_date = models.DateTimeField(auto_now_add=True, verbose_name="added")
    reporter = models.ForeignKey(User, on_delete=models.SET_NULL, default=None, null=True)

    @property
    def total_articles(self):
        return Article.objects.filter(category__pk=self.pk).count()

    class Meta:
        verbose_name_plural = 'categories'
        verbose_name = "category"

    def __unicode__(self):
        return self.name

    def __str__(self):
        return "{}".format(self.name)


class Article(models.Model):
    PUBLISHED = 1
    DRAFT = 2
    ARCHIVE = 3
    ARTICLE_STATUS = (
        (PUBLISHED, 'Published'), (DRAFT, 'Draft'), (ARCHIVE, 'Archived'))
    headline = models.CharField(max_length=255, verbose_name='title')
    content = models.TextField(verbose_name='content')
    reporter = models.ForeignKey(User, on_delete=models.CASCADE)
    notice = models.TextField(null=True, blank=True, default=None, verbose_name='notice')
    slug = models.SlugField(max_length=255, verbose_name='pretty-url', null=True, blank=True, unique=True)

    category = models.ForeignKey(Category, on_delete=models.SET_NULL, default=None, null=True, blank=True,
                                 verbose_name='category')
    status = models.IntegerField(choices=ARTICLE_STATUS, default=DRAFT, verbose_name='status')
    published_date = models.DateTimeField(default=None, null=True, verbose_name="published date")
    added_date = models.DateTimeField(auto_now_add=True, verbose_name="added date")

    class Meta:
        verbose_name_plural = 'articles'
        verbose_name = "article"

    def __unicode__(self):
        return self.headline

    def __str__(self):
        return "{}".format(self.headline)

    # TODO: Fix - update slug if headline change

    def save(self):
        if not self.id:
            self.slug = slugify(self.headline)
        super(Article, self).save()


class ArticleComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(verbose_name='content', max_length=500)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    added_date = models.DateTimeField(auto_now_add=True, verbose_name="added date")

    def get_absolute_url(self):
        return reverse('article-detail', kwargs={'slug': self.article.slug})

    class Meta:
        verbose_name_plural = 'comments'
        verbose_name = "comment"

    def __unicode__(self):
        return "{} {}".format(self.id, self.content)

    def __str__(self):
        return "{} {}".format(self.id, self.content)
