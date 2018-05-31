# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views import generic

from .forms import CommentForm
from .models import Article, ArticleComment


# Create your views here.

class IndexView(LoginRequiredMixin, generic.ListView):
    template_name = 'blog/index.html'
    context_object_name = 'latest_article_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Article.objects.filter(status=Article.PUBLISHED).order_by('-published_date')[:5]


class ArticleDetailView(LoginRequiredMixin, generic.DetailView):
    model = Article
    template_name = 'blog/article_detail.html'

    def get_context_data(self, **kwargs):
        context = super(ArticleDetailView, self).get_context_data(**kwargs)
        context['comments'] = ArticleComment.objects.filter(article=self.object.id).select_related('user').all()
        context['form'] = CommentForm
        return context


@login_required()
def add_comment(request, article=None):
    if not request.POST:
        return HttpResponseRedirect(reverse('index'))
    article = get_object_or_404(Article, pk=article)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.article = article
        comment.user = request.user
        comment.save()
        return HttpResponseRedirect(reverse('article-detail', kwargs={'slug': article.slug}))
