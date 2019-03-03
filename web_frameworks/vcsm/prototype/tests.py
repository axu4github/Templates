import json

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from prototype.serializers import TenantSerializer


class TestSerializerUse(APITestCase):
    """ 测试 Serializer 使用方法 """

    def test_insert(self):
        """ 测试创建方法 """
        data = {
            "name": "租户_002",
            "code": "tenant_002",
            "type": "类型_002",
            "details": "详情_002"
        }
        response_data = TenantSerializer().insert(data)

        for k, v in data.items():
            self.assertEqual(v, response_data[k])


class TestTenantRestAPI(APITestCase):
    """ 测试租户接口 """

    def get_version_uri(self, raw_uri):
        # return "/{0}/{1}".format("v1", raw_uri)
        return raw_uri

    def create_tenant(self, data):
        """ 创建租户 """
        response = self.client.post(
            self.get_version_uri(reverse("prototype:tenant-list")), data)
        response_data = json.loads(response.content)
        return response, response_data

    def test_create_tenant(self):
        """ 测试创建租户 """
        data = {
            "name": "租户_001",
            "code": "tenant_001",
            "type": "类型_001",
            "details": "详情_001"
        }
        response, response_data = self.create_tenant(data)

        self.assertEqual(response.status_code,
                         status.HTTP_201_CREATED,
                         response.content)

        for field, _ in data.items():
            self.assertEqual(data[field], response_data[field])

    def test_create_tenant_field_name_not_have(self):
        """ 测试创建租户时，名称（必输项）字段不给 """
        response, response_data = self.create_tenant({})

        self.assertEqual(response.status_code,
                         status.HTTP_400_BAD_REQUEST,
                         response.content)
        self.assertTrue("name" in response_data.keys())
        self.assertTrue("is required" in " ".join(response_data["name"]))

    def test_create_tenant_field_name_is_have_but_is_null(self):
        """ 测试创建租户时，名称字段有，但是是空值 """
        response, response_data = self.create_tenant({"name": ""})

        self.assertEqual(response.status_code,
                         status.HTTP_400_BAD_REQUEST,
                         response.content)
        self.assertTrue("name" in response_data.keys())
        self.assertTrue("not be blank" in " ".join(response_data["name"]))

    def test_create_tenant_field_code_has_chinese(self):
        """ 测试创建租户时，代码值有中文 """
        response, response_data = self.create_tenant({
            "name": "租户_002",
            "code": "租户代码_002"
        })

        self.assertEqual(response.status_code,
                         status.HTTP_400_BAD_REQUEST,
                         response.content)
        self.assertTrue("code" in response_data.keys())
        self.assertTrue(
            "can not contain chinese" in " ".join(response_data["code"]))
