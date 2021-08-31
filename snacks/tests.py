
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from .models import Snack
# Create your tests here.
class ThingTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test", email="tester@test.com", password="pass"
        )

        self.thing = Snack.objects.create(
            title="falafel", description='falafel rap', purchaser=self.user,
        )

    def test_string_representation(self):
        self.assertEqual(str(self.thing), "falafel")

    def test_thing_content(self):
        self.assertEqual(f"{self.thing.title}", "falafel")
        self.assertEqual(f"{self.thing.purchaser}", "test")
        self.assertEqual(self.thing.description, 'falafel rap')

    def test_thing_list_view(self):
        response = self.client.get(reverse("snack_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "falafel")
        self.assertTemplateUsed(response, "snack_list.html")

    def test_thing_detail_view(self):
        response = self.client.get(reverse("snack_detail", args="1"))
        no_response = self.client.get("/100000/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, "purchaser: test")
        self.assertTemplateUsed(response, "snack_detail.html")

    def test_thing_create_view(self):
        response = self.client.post(
            reverse("snack_create"),
            {
                "title": "falafel",
                "description": "falafel rap",
                "purchaser": self.user.id,
            }, follow=True
        )

        self.assertRedirects(response, reverse("snack_detail", args="2"))
        self.assertContains(response, "Details about falafel")
    def test_thing_update_view_redirect(self):
        response = self.client.post(
            reverse("snack_update", args="1"),
            {"title": "Updated title","description":"falafel with salat","purchaser":self.user.id}
        )

        self.assertRedirects(response, reverse("snack_detail", args="1"))
    def test_thing_delete_view(self):
        response = self.client.get(reverse("snack_delete", args="1"))
        self.assertEqual(response.status_code, 200)