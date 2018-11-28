from django.test import TestCase
from django.contrib.auth import get_user_model

from users.models import Tenant


UserModel = get_user_model()


class UserProfileTest(TestCase):

    def test_user_profile(self):
        tenant = Tenant(
            name="租户_001", code="tenant_001", type="租户类型_001")
        tenant.save()

        _user = UserModel.objects.create_user(
            "test_user", "test@user.com", "123456")
        _user.tenant = tenant
        _user.owner = _user
        _user.save()

        self.assertEqual(_user.tenant.name, "租户_001")
        self.assertEqual(_user.tenant.code, "tenant_001")
        self.assertEqual(_user.owner.username, "test_user")
        self.assertEqual(_user.owner.email, "test@user.com")
