import json

from django.utils import timezone
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Question, Choice
from mysite.core.utils import Utils


class QuestionRestAPITest(APITestCase):

    def test_create_question(self):
        url = reverse("polls:question-list")
        data = {
            "question_text": "question_text_001",
            "pub_date": timezone.now()
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            "question_text_001",
            json.loads(response.content)[0]["question_text"])

    def test_create_none_text_question(self):
        url = reverse("polls:question-list")
        data = {
            "question_text": "              ",
            "pub_date": timezone.now()
        }
        response = self.client.post(url, data)
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
            response.content)
        self.assertTrue(b"not be blank" in response.content)

    def test_read_question(self):
        response = self.client.get(reverse("polls:question-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(0, len(json.loads(response.content)))

    def test_update_question(self):
        url = reverse("polls:question-list")
        data = {
            "question_text": "question_text_002",
            "pub_date": timezone.now()
        }
        response = self.client.post(url, data)
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
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            json.loads(response.content)["question_text"],
            "question_text_02_modified")

        response = self.client.get(url)
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
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            json.loads(response.content)["question_text"],
            "question_text_003")

        pk = json.loads(response.content)["id"]

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(1, len(json.loads(response.content)))

        url = reverse("polls:question-detail", args=(pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.get(reverse("polls:question-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(0, len(json.loads(response.content)))

    def test_list_question(self):
        url = reverse("polls:question-list")
        data = {
            "question_text": "question_text_004",
            "pub_date": timezone.now()
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            json.loads(response.content)["question_text"],
            "question_text_004")

        response = self.client.get(url)
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
        response = self.client.get(url)
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
        response = self.client.get(url)
        _j = json.loads(response.content)

        self.assertEqual(0, len(_j), response.content)

    def test_list_question_relation(self):
        q = Question(
            question_text="question_text_006", pub_date=timezone.now())
        q.save()
        c = Choice(question=q, choice_text="006_001")
        c.save()

        response = self.client.get(reverse("polls:choice-list"))
        self.assertEqual(q.id, json.loads(response.content)[0]["question"])


class ChoiceRestAPITest(APITestCase):

    def test_create_choice(self):
        q = Question(question_text="question_text_007")
        q.save()

        q2 = Question(question_text="question_text_008")
        q2.save()

        url = reverse("polls:choice-list")
        data = {"choice_text": "choice_text_001", "question": q2.id}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code,
                         status.HTTP_201_CREATED, response.content)
        self.assertEqual(q2.id, json.loads(response.content)["question"])
