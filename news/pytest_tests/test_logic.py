import pytest
from pytest_django.asserts import assertRedirects, assertFormError

from django.urls import reverse

from news.forms import BAD_WORDS, WARNING
from news.models import Comment, News

from http import HTTPStatus

def test_user_can_create_comment(author_client, author, news, form_data, news_id_for_args):
    url = reverse('news:detail', args=news_id_for_args)
    response = author_client.post(url, data=form_data)
    assertRedirects(response, f'{url}#comments')
    assert Comment.objects.count() == 1
    comment = Comment.objects.get()
    assert comment.text == form_data['text']
    assert comment.news == news
    assert comment.author == author


@pytest.mark.django_db
def test_anonymous_user_cant_create_comment(client, form_data, news_id_for_args):
    url = reverse('news:detail', args=news_id_for_args)
    response = client.post(url, data=form_data)
    assert Comment.objects.count() == 0


@pytest.mark.django_db
def test_user_cant_use_bad_words(author_client, bad_words_data, news_id_for_args):
    url = reverse('news:detail', args=news_id_for_args)
    response = author_client.post(url, data=bad_words_data)
    assertFormError(
        response,
        form='form',
        field='text',
        errors=WARNING
    )
    assert Comment.objects.count() == 0







