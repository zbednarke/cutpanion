import pytest
from django.test import Client, RequestFactory, TransactionTestCase, override_settings
from django.urls import reverse, set_urlconf
from django.contrib.auth import get_user_model
import datetime

from accounts.tests.factories import UserFactory

User = get_user_model


@pytest.fixture
def logged_in_client(basic_user):
    """A django client with logged in basic user
    user = basic_user
    """
    client = Client()
    
    client.force_login(basic_user)
    client.user = basic_user
    return client


@pytest.fixture
def basic_user():
    """A basic user"""
    user = UserFactory(username='basic_user', password='test', last_login=datetime.datetime.now())
    yield user
    try:
        user.delete()
    except:
        pass