# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.urls import reverse
from django.utils import timezone
from django.utils.html import format_html

from .models import Category, Article, ArticleComment


# Artcile admin actions

def publish_articles(modeladmin, request, queryset):
    for article in queryset:
        article.status = Article.PUBLISHED
        article.published_date = timezone.now()
        article.save()


publish_articles.short_description = 'Publish selected Articles'


def unpublish_articles(modeladmin, request, queryset):
    queryset.update(status=Article.DRAFT, published_date=None)


unpublish_articles.short_description = 'Unpublish selected Articles'


# Register your models here.

class ArticleAdmin(admin.ModelAdmin):
    fields = (('headline', 'category',), 'status', 'content', 'notice')
    list_select_related = ('reporter',)
    list_display = (
        'headline', 'reporter', 'category', 'status', 'added_date', 'published_date',)

    search_fields = ('headline', 'reporter', 'content',)
    actions = [publish_articles, unpublish_articles, ]
    list_filter = ['status', 'published_date']

    def get_form(self, request, obj=None, **kwargs):
        """ When displaying change textarea height"""
        form = super(ArticleAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['content'].widget.attrs['style'] = 'height: 300px;'
        form.base_fields['notice'].widget.attrs['style'] = 'height: 50px;'
        return form

    def save_model(self, request, obj, form, change):
        """When creating a new object, set the reporter field.
        """
        if obj.status == obj.PUBLISHED:
            obj.published_date = timezone.now()
        elif obj.status == obj.DRAFT:
            obj.published_date = None

        if not change:
            obj.reporter = request.user

        obj.save()


class CategoryAdmin(admin.ModelAdmin):
    fields = ('name',)
    list_display = ('name', 'reporter', 'added_date', 'total_articles')
    list_select_related = ('reporter',)

    def save_model(self, request, obj, form, change):
        """When creating a new object, set the reporter field.
        """
        if not change:
            obj.reporter = request.user
        obj.save()


class ArticleCommentAdmin(admin.ModelAdmin):
    fields = ('content', 'article')
    list_display = ('id', 'user', 'link_to_article', 'content', 'added_date')
    list_select_related = ('user', 'article')

    def link_to_article(self, obj):
        link = reverse("article-detail", args=[obj.article.slug])
        return format_html('<a href="{}"> Edit {}</a>', link, obj.article)

    link_to_article.short_description = 'Show Article'

    def save_model(self, request, obj, form, change):
        """When creating a new object, set the reporter field.
        """
        if not change:
            obj.user = request.user
        obj.save()


admin.site.register(ArticleComment, ArticleCommentAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.site_title = "Blog admin panel"
admin.site.index_title = 'SP-Test'
