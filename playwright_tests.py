import os
import time
import pytest

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pollme.settings")
os.environ.setdefault("DJANGO_ALLOW_ASYNC_UNSAFE", "true")  # makes tests easier

import django

django.setup()

from django.contrib.auth.models import User
from polls.models import Poll, Choice, Vote

BASE_URL = "http://127.0.0.1:8000"
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "password123")


def unique_text(prefix):
    return f"{prefix} {int(time.time() * 1000)}"


def login(page, username=ADMIN_USERNAME, password=ADMIN_PASSWORD):
    page.goto(f"{BASE_URL}/accounts/login/")
    page.fill('input[name="username"]', username)
    page.fill('input[name="password"]', password)
    page.click('button[type="submit"], input[type="submit"]')
    page.wait_for_load_state("networkidle")


@pytest.fixture
def test_user():
    username = unique_text("e2euser").replace(" ", "")
    password = "password123"

    user = User.objects.create_user(
        username=username,
        email=f"{username}@test.local",
        password=password,
    )

    yield user, password

    User.objects.filter(id=user.id).delete()


@pytest.fixture
def poll_with_choices(test_user):
    user, _ = test_user

    poll = Poll.objects.create(
        owner=user, text=unique_text("E2E Favorite framework?")
    )

    choice1 = Choice.objects.create(poll=poll, choice_text="Django")
    choice2 = Choice.objects.create(poll=poll, choice_text="Flask")

    yield poll, choice1, choice2, user

    Poll.objects.filter(id=poll.id).delete()


def test_1_register_and_login(page):
    """Verify that a new user can register an account and successfully log in."""

    username = unique_text("registereduser").replace(" ", "")
    email = f"{username}@test.local"
    password = "password123"

    page.goto(f"{BASE_URL}/accounts/register/")
    page.fill('input[name="username"]', username)
    page.fill('input[name="email"]', email)
    page.fill('input[name="password1"]', password)
    page.fill('input[name="password2"]', password)
    page.click('button[type="submit"], input[type="submit"]')

    page.wait_for_load_state("networkidle")
    assert "login" in page.url.lower()

    page.fill('input[name="username"]', username)
    page.fill('input[name="password"]', password)
    page.click('button[type="submit"], input[type="submit"]')

    page.wait_for_load_state("networkidle")
    assert "login" not in page.url.lower()

    User.objects.filter(username=username).delete()


def test_2_create_new_poll_with_multiple_choices(page):
    """Verify that an authenticated user can create a new poll with multiple choices."""

    login(page)

    poll_text = unique_text("New poll")
    choice1 = "Option Alpha"
    choice2 = "Option Beta"

    page.goto(f"{BASE_URL}/polls/add/")
    page.fill('textarea[name="text"]', poll_text)
    page.fill('input[name="choice1"]', choice1)
    page.fill('input[name="choice2"]', choice2)
    page.click('button[type="submit"], input[type="submit"]')

    page.wait_for_load_state("networkidle")

    assert Poll.objects.filter(text=poll_text).exists()
    poll = Poll.objects.get(text=poll_text)
    assert poll.choice_set.filter(choice_text=choice1).exists()
    assert poll.choice_set.filter(choice_text=choice2).exists()

    poll.delete()


def test_3_submit_vote(page, poll_with_choices):
    """Verify that a logged-in user can submit a vote on an existing poll."""

    poll, choice1, choice2, user = poll_with_choices

    login(page, user.username, "password123")

    page.goto(f"{BASE_URL}/polls/{poll.id}/")
    page.check(f'input[value="{choice1.id}"]')
    page.click('button[type="submit"], input[type="submit"]')

    page.wait_for_load_state("networkidle")

    assert Vote.objects.filter(user=user, poll=poll, choice=choice1).exists()
    assert "Total:" in page.locator("body").inner_text()


def test_4_view_results_and_verify_count_incremented(page, poll_with_choices):
    """Verify that submitting a vote increases the total vote count displayed in poll results."""

    poll, choice1, choice2, user = poll_with_choices

    before_count = poll.get_vote_count

    login(page, user.username, "password123")

    page.goto(f"{BASE_URL}/polls/{poll.id}/")
    page.check(f'input[value="{choice2.id}"]')
    page.click('button[type="submit"], input[type="submit"]')

    page.wait_for_load_state("networkidle")

    poll.refresh_from_db()
    after_count = poll.get_vote_count

    assert after_count == before_count + 1
    assert f"Total: {after_count} votes" in page.locator("body").inner_text()


def test_5_edit_choice_on_existing_poll(page):
    """Verify that an existing poll choice can be edited and the updated value appears on the poll page."""

    admin = User.objects.get(username=ADMIN_USERNAME)

    poll = Poll.objects.create(owner=admin, text=unique_text("editable poll"))

    choice = Choice.objects.create(poll=poll, choice_text="Original Choice")

    try:
        login(page)

        page.goto(f"{BASE_URL}/polls/edit/choice/{choice.id}/")
        page.fill('input[name="choice_text"]', "Updated Choice")
        page.click('button[type="submit"], input[type="submit"]')

        page.wait_for_load_state("networkidle")

        choice.refresh_from_db()
        assert choice.choice_text == "Updated Choice"

        page.goto(f"{BASE_URL}/polls/edit/{poll.id}/")
        assert "Updated Choice" in page.locator("body").inner_text()

    finally:
        poll.delete()
