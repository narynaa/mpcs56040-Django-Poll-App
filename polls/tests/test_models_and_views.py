from unittest.mock import MagicMock, Mock, patch

from django.contrib.auth.models import User
from django.test import RequestFactory, TestCase

from polls.models import Choice, Poll, Vote
from polls.views import poll_detail, poll_vote, polls_list


class PollModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="owner_test",
            password="password123",
        )
        self.poll = Poll.objects.create(
            owner=self.user,
            text="Favorite programming language?",
        )
        self.choice_python = Choice.objects.create(
            poll=self.poll,
            choice_text="Python",
        )
        self.choice_js = Choice.objects.create(
            poll=self.poll,
            choice_text="JavaScript",
        )

    def test_poll_str_returns_poll_text(self):
        self.assertEqual(str(self.poll), "Favorite programming language?")

    def test_choice_str_returns_poll_and_choice_text(self):
        self.assertEqual(
            str(self.choice_python),
            "Favorite programming lang - Python",
        )

    def test_vote_str_returns_poll_choice_and_username(self):
        vote = Vote.objects.create(
            user=self.user,
            poll=self.poll,
            choice=self.choice_python,
        )

        self.assertEqual(
            str(vote),
            # note: this truncation is part of the model's __str__ implementation
            # it looks weird, but this specific string has been tested and it
            # will work
            "Favorite progra - Python - owner_test",
        )

    def test_user_can_vote_returns_false_after_user_votes(self):
        Vote.objects.create(
            user=self.user,
            poll=self.poll,
            choice=self.choice_python,
        )

        self.assertFalse(self.poll.user_can_vote(self.user))

    def test_get_result_dict_uses_fake_random_alert_class(self):
        # Double type: Fake
        Vote.objects.create(
            user=self.user,
            poll=self.poll,
            choice=self.choice_python,
        )

        def fake_choice(_items):
            return "primary"

        with patch("polls.models.secrets.choice", side_effect=fake_choice):
            result = self.poll.get_result_dict()

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["alert_class"], "primary")
        self.assertEqual(result[0]["text"], "Python")
        self.assertEqual(result[0]["num_votes"], 1)
        self.assertEqual(result[0]["percentage"], 100)


class PollViewTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.owner = User.objects.create_user(
            username="owner_test",
            password="password123",
        )
        self.voter = User.objects.create_user(
            username="voter_test",
            password="password123",
        )
        self.poll = Poll.objects.create(
            owner=self.owner,
            text="Favorite framework?",
        )
        self.choice = Choice.objects.create(
            poll=self.poll,
            choice_text="Django",
        )

    def test_poll_detail_for_inactive_poll_renders_results_template(self):
        # Double type: Stub
        self.poll.active = False
        self.poll.save()

        request = self.factory.get(f"/polls/{self.poll.id}/")

        with patch("polls.views.render") as render_stub:
            render_stub.return_value = "stubbed response"

            response = poll_detail(request, self.poll.id)

        self.assertEqual(response, "stubbed response")
        render_stub.assert_called_once_with(
            request,
            "polls/poll_result.html",
            {"poll": self.poll},
        )

    def test_polls_list_search_filters_by_search_term(self):
        # Double type: Mock
        request = self.factory.get("/polls/list/?search=django")
        request.user = self.voter

        fake_queryset = MagicMock()
        fake_queryset.filter.return_value = fake_queryset

        fake_page = Mock(name="fake_page")

        with patch("polls.views.Poll.objects.all", return_value=fake_queryset):
            with patch("polls.views.Paginator") as paginator_mock:
                with patch("polls.views.render") as render_mock:
                    paginator_mock.return_value.get_page.return_value = (
                        fake_page
                    )
                    render_mock.return_value = "rendered response"

                    response = polls_list(request)

        self.assertEqual(response, "rendered response")
        fake_queryset.filter.assert_called_once_with(text__icontains="django")

    def test_poll_vote_without_choice_shows_error_message(self):
        # Double type: Spy
        request = self.factory.post(f"/polls/{self.poll.id}/vote/", data={})
        request.user = self.voter

        with patch("polls.views.messages.error") as message_spy:
            response = poll_vote(request, self.poll.id)

        self.assertEqual(response.status_code, 302)
        message_spy.assert_called_once()
        self.assertIn("No choice selected!", message_spy.call_args.args)

    def test_poll_vote_with_valid_choice_creates_vote(self):
        request = self.factory.post(
            f"/polls/{self.poll.id}/vote/",
            data={"choice": self.choice.id},
        )
        request.user = self.voter

        with patch("polls.views.render") as render_stub:
            render_stub.return_value.status_code = 200

            response = poll_vote(request, self.poll.id)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            Vote.objects.filter(
                user=self.voter,
                poll=self.poll,
                choice=self.choice,
            ).exists()
        )
