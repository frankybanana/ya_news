import pytest
from datetime import datetime, timedelta

from django.test.client import Client
from django.conf import settings
from django.utils import timezone

from news.models import Comment, News

from news.forms import BAD_WORDS


@pytest.fixture
def author(django_user_model):
    return django_user_model.objects.create(username='Автор')


@pytest.fixture
def not_author(django_user_model):
    return django_user_model.objects.create(username='Не автор')


@pytest.fixture
def client(author):
    client = Client()
    return client


@pytest.fixture
def author_client(author):
    client = Client()
    client.force_login(author)
    return client


@pytest.fixture
def not_author_client(not_author):
    client = Client()
    client.force_login(not_author)
    return client


@pytest.fixture
def news(author):
    news = News.objects.create(
        title='Заголовок',
        text='Текст заметки',
    )
    return news


@pytest.fixture
def comment(news, author):
    comment = Comment.objects.create(
        news=news,
        author=author,
        text='Текст комментария'
    )
    return comment


@pytest.fixture
def form_data():
    return {
        'text': 'Текст комментария'
    }


@pytest.fixture
def comment_id_for_args(comment):
    return (comment.id,)


@pytest.fixture
def news_id_for_args(news):
    return (news.id,)


@pytest.fixture
def bad_words_data():
    return {
        'text': f'Какой-то текст, {BAD_WORDS[0]}, еще текст'
    }


@pytest.fixture
def all_news():
    today = datetime.today()
    all_news = [
        News(
            title=f'Новость {index}',
            text='Просто текст.',
            date=today - timedelta(days=index)
        )
        for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1)
    ]
    News.objects.bulk_create(all_news)


@pytest.fixture
def new_comments(news, author):
    now = timezone.now()
    for index in range(10):
        comment = Comment.objects.create(
            news=news, author=author, text=f'Tекст {index}',
        )
        comment.created = now + timedelta(days=index)
        comment.save()
