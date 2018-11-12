import json

from django.utils import timezone
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


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

        # url = reverse("polls:question-list") + "query/"
        response = self.client.get(url)
        self.assertEqual(
            json.loads(response.content)[0]["question_text"],
            "question_text_004")

    def test_query_question(self):
        url = reverse("polls:question-list")
        data = {
            "question_text": "question_text_005",
            "pub_date": timezone.now()
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            json.loads(response.content)["question_text"],
            "question_text_005")

        url = "{0}?question_text=question_text_005".format(url)
        print(url)
        response = self.client.get(url)
        print(response.content)
