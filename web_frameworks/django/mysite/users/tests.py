import json
import base64

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from oauth2_provider.models import (
    get_access_token_model, get_application_model
)

from users.models import Tenant
from .models import UserProfile


Application = get_application_model()
AccessToken = get_access_token_model()
UserModel = get_user_model()


def get_basic_auth_header(user, password):
    user_pass = '{0}:{1}'.format(user, password)
    auth_string = base64.b64encode(user_pass.encode('utf-8'))
    auth_headers = {
        'HTTP_AUTHORIZATION': 'Basic ' + auth_string.decode("utf-8"),
    }

    return auth_headers


class UserProfileTest(TestCase):

    def setUp(self):
        self.tenant = Tenant(name="租户_001", code="tanant_001")
        self.tenant.save()

        self.test_user = UserModel.objects.create_user(
            "test_user", "test@user.com", "123456")

        up = UserProfile(user=self.test_user, tenant=self.tenant)
        up.save()

        self.application = Application(
            name="Test Application",
            user=self.test_user,
            client_type=Application.CLIENT_CONFIDENTIAL,
            authorization_grant_type=Application.GRANT_PASSWORD,
        )
        self.application.save()

        response = self.client.post(
            reverse('oauth2_provider:token'),
            data={
                'grant_type': 'password',
                'username': 'test_user',
                'password': '123456',
            },
            **get_basic_auth_header(
                self.application.client_id,
                self.application.client_secret))

        self.auth_headers = {
            'HTTP_AUTHORIZATION': 'Bearer ' + json.loads(
                response.content.decode("utf-8"))["access_token"],
        }

    def test_create_user(self):
        data = {
            "username": "test_user_001",
            "email": "test_user_001@user.com",
            "tenant": self.tenant.id
        }
        response = self.client.post(
            reverse("users:user-list"), data, **self.auth_headers)
        response_data = json.loads(response.content)

        self.assertEqual(data["username"], response_data["username"])
        self.assertEqual(data["email"], response_data["email"])
        self.assertEqual(data["tenant"], response_data["tenant"])

    # def test_read_user(self):
    #     response = self.client.get(
    #         reverse("users:user-list"), **self.auth_headers)
    #     response_data = response.content

    #     print(response_data)
