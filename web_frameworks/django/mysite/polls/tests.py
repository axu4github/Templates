import json
import base64

from django.utils import timezone
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase
from oauth2_provider.models import (
    get_access_token_model, get_application_model
)

from polls.models import Question, Choice
from mysite.core.utils import Utils
from users.models import Tenant, UserProfile

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


class QuestionRestAPITest(APITestCase):

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

    def test_create_question(self):
        url = reverse("polls:question-list")
        data = {
            "question_text": "question_text_001",
            "pub_date": timezone.now()
        }
        response = self.client.post(url, data, **self.auth_headers)

        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED, response.content)

        response = self.client.get(url, **self.auth_headers)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            "question_text_001",
            json.loads(response.content)[0]["question_text"])
        self.assertEqual(
            self.tenant.id, json.loads(response.content)[0]["tenant"])
        self.assertEqual(
            self.test_user.id, json.loads(response.content)[0]["owner"])

    def test_create_none_text_question(self):
        url = reverse("polls:question-list")
        data = {
            "question_text": "              ",
            "pub_date": timezone.now()
        }
        response = self.client.post(url, data, **self.auth_headers)
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
            response.content)
        self.assertTrue(b"not be blank" in response.content)

    def test_read_question(self):
        response = self.client.get(
            reverse("polls:question-list"), **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(0, len(json.loads(response.content)))

    def test_update_question(self):
        url = reverse("polls:question-list")
        data = {
            "question_text": "question_text_002",
            "pub_date": timezone.now()
        }
        response = self.client.post(url, data, **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            json.loads(response.content)["question_text"],
            "question_text_002")

        pk = json.loads(response.content)["id"]
        url = reverse("polls:question-detail", args=(pk,))
        data = {
            "question_text": "question_text_02_modified",
            "pub_date": timezone.now()
        }
        response = self.client.put(url, data, **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            json.loads(response.content)["question_text"],
            "question_text_02_modified")

        response = self.client.get(url, **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            json.loads(response.content)["question_text"],
            "question_text_02_modified")

    def test_delete_question(self):
        url = reverse("polls:question-list")
        data = {
            "question_text": "question_text_003",
            "pub_date": timezone.now()
        }
        response = self.client.post(url, data, **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            json.loads(response.content)["question_text"],
            "question_text_003")

        pk = json.loads(response.content)["id"]

        response = self.client.get(url, **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(1, len(json.loads(response.content)))

        url = reverse("polls:question-detail", args=(pk,))
        response = self.client.delete(url, **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.get(
            reverse("polls:question-list"), **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(0, len(json.loads(response.content)))

    def test_list_question(self):
        url = reverse("polls:question-list")
        data = {
            "question_text": "question_text_004",
            "pub_date": timezone.now()
        }
        response = self.client.post(url, data, **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            json.loads(response.content)["question_text"],
            "question_text_004")

        response = self.client.get(url, **self.auth_headers)
        self.assertEqual(
            json.loads(response.content)[0]["question_text"],
            "question_text_004")

    def test_query_question(self):
        q = Question(question_text="question_text_005_001")
        q.save()
        q = Question(question_text="question_text_005_002")
        q.save()

        query = "question_text=question_text_005_001"
        url = reverse("polls:question-list")
        url = "{0}?{1}".format(url, query)
        response = self.client.get(url, **self.auth_headers)
        _j = json.loads(response.content)

        self.assertEqual(1, len(_j))
        self.assertEqual("question_text_005_001", _j[0]["question_text"])

    def test_query_none_question(self):
        q = Question(question_text="question_text_008_001")
        q.save()
        q = Question(
            question_text="question_text_008_002",
            pub_date=Utils.parse_datetime("2018-11-14 10:00:00"))
        q.save()

        query = "pub_date= to 2018-11-13 00:00:00"
        url = reverse("polls:question-list")
        url = "{0}?{1}".format(url, query)
        response = self.client.get(url, **self.auth_headers)
        _j = json.loads(response.content)

        self.assertEqual(0, len(_j), response.content)

    def test_list_question_relation(self):
        q = Question(
            question_text="question_text_006", pub_date=timezone.now())
        q.save()
        c = Choice(question=q, choice_text="006_001")
        c.save()

        response = self.client.get(
            reverse("polls:choice-list"), **self.auth_headers)

        self.assertEqual(q.id, json.loads(response.content)[0]["question"])


class ChoiceRestAPITest(QuestionRestAPITest):

    def test_create_choice(self):
        q = Question(question_text="question_text_007")
        q.save()

        q2 = Question(question_text="question_text_008")
        q2.save()

        url = reverse("polls:choice-list")
        data = {"choice_text": "choice_text_001", "question": q2.id}
        response = self.client.post(url, data, **self.auth_headers)

        self.assertEqual(response.status_code,
                         status.HTTP_201_CREATED, response.content)
        self.assertEqual(q2.id, json.loads(response.content)["question"])
