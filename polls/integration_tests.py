from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Choice, Poll, Vote


class PollIntegrationTests(TestCase):
    def setUp(self):
        self.owner = User.objects.create_user(
            username="owner", password="testpass123"
        )

        self.voter = User.objects.create_user(
            username="voter", password="testpass123"
        )

        self.poll = Poll.objects.create(
            owner=self.owner, text="What is your favorite framework?"
        )

        self.choice_django = Choice.objects.create(
            poll=self.poll, choice_text="Django"
        )

        self.choice_flask = Choice.objects.create(
            poll=self.poll, choice_text="Flask"
        )

    def test_authenticated_user_can_vote_and_vote_is_saved(self):
        self.client.login(username="voter", password="testpass123")

        response = self.client.post(
            reverse("polls:vote", args=[self.poll.id]),
            {"choice": self.choice_django.id},
        )

        self.assertEqual(response.status_code, 200)

        vote = Vote.objects.get(user=self.voter, poll=self.poll)

        self.assertEqual(vote.choice, self.choice_django)
        self.assertEqual(Vote.objects.count(), 1)
        self.assertEqual(self.choice_django.get_vote_count, 1)

    def test_poll_list_view_renders_poll_title_in_template(self):
        self.client.login(username="voter", password="testpass123")

        response = self.client.get(reverse("polls:list"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "polls/polls_list.html")
        self.assertContains(response, "What is your favorite framework?")
