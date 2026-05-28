## Code changes & Setup
The only code changes made to the existing application code were adding the following ones:
- Two new dependecies to the `requirements.txt` file
- Existing unit tests from `polls/tests.py` were renamed to `polls/tests_legacy.py` (to avoid name collision with my new unit tests)
- `.coverage` was added to `.gitignore`

These changes do not modify the application logic in any way. All of them can be verified by looking at the commit history if needed.

To install dependencies and enable running the later tests locally, follow these steps:
1. Create a fresh virtual environment with `python3 -m venv .venv`
2. Activate it by running `source .venv/bin/activate`
3. Install all requirements by running `pip3 install -r requirements.txt`

## Running Q3 unit tests
- Navigate to the root repo directory
- To simply run the test suite (without coverage), run `python3 manage.py test polls.tests`
- To run the test suite and then generate a coverage report in the terminal, run `coverage run manage.py test polls.tests` followed by `coverage report`. Coverage report will be printed in the terminal.
- To generate html version of this report, run `coverage html`. This report will be automatically saved under `htmlcov/index.html` and can be opened with your browser.

## Running Q4 performance tests
- Navigate to the root repo directory
- Run `python3 manage.py runserver` to start the server
> Note: this assumes that you followed the steps for Q2 testing outlined in my writeup and have already completed migration and created an admin account. If you haven't, please run those commands from the writeup first.

- Run `python3 create_test_users.py` to create 200 test users.
- Run the load test: `k6 run --summary-trend-stats="avg,p(95),p(99)" --out json=load_results.json load_test.js`
- Test output summary will be printed to the terminal, detailed test output will be saved to `load_results.json`
- To plot these results, run `python3 plot_performance_test.py`
    - Make sure to replace `spike_results.json` with `load_tests.json` and `spike_test_response_time_graph.png` with `load_test_response_time_graph.png`. Both tests use the same plotting code but you'll need to adjust file names manually.

- Repeat the same steps for the spike test
- Run `k6 run --summary-trend-stats="avg,p(95),p(99)" --out json=spike_results.json spike_test.js` and plot the results using the same command as above

## Running Q5 tests
> Note: no separate framework configuration is needed with my test setup.
- Run `python3 -m playwright install` to make sure that playwright downloads all the data in needs
- Start your server by running `python3 manage.py runserver`
> Note: similar to Q4, these instructions assume that you already ran setup commands (needed only once). If you haven't, refer to the Q4 instructions for how to do setup.

- Run `ADMIN_USERNAME=your_username ADMIN_PASSWORD=your_password python3 -m pytest playwright_tests.py --headed`,
where `ADMIN_USERNAME` and `ADMIN_PASSWORD` are the username and password you setup when running Q2/Q4 tests.

## Running Q7 tests
- Test file:`polls/integration_tests.py`
- To run the first test: `python manage.py test polls.integration_tests.PollIntegrationTests.test_authenticated_user_can_vote_and_vote_is_saved`
- To run the second test: `python manage.py test polls.integration_tests.PollIntegrationTests.test_poll_list_view_renders_poll_title_in_template`
- To run both tests: `python manage.py test polls.integration_tests.PollIntegrationTests`

## References
> Note: I tried to sort by question where possible, but some references apply across multiple questions

Intro resource (I used it to better understand setup commands to run the server etc, used in multiple questions):
- [Django polling/voting app architecture examples] https://docs.djangoproject.com/en/stable/intro/tutorial01/
- Q1
    - [ruff linting rules] https://docs.astral.sh/ruff/linter/
    - [isort conventions for import ordering] https://isort.readthedocs.io/en/latest/
- Q3
    - [unittest.mock patch()] https://docs.python.org/3/library/unittest.mock.html#unittest.mock.patch
    - [unittest.mock MagicMock] https://docs.python.org/3/library/unittest.mock.html#unittest.mock.MagicMock
    - [Django testing] https://docs.djangoproject.com/en/6.0/topics/testing/tools/
    - [django RequestFactory] https://docs.djangoproject.com/en/6.0/topics/testing/advanced/#django.test.RequestFactory
    - [django TestCase] https://docs.djangoproject.com/en/6.0/topics/testing/tools/#django.test.TestCase
    - [django authentication] https://docs.djangoproject.com/en/6.0/ref/contrib/auth/
    - [Django auth User model usage] https://docs.djangoproject.com/en/stable/topics/auth/default/
- Q4
    - [JS regex] https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Regular_expressions/Groups_and_backreferences
    - [django csrfmiddlewaretoken] https://docs.djangoproject.com/en/6.0/ref/csrf/
    - [k6 spike tests] https://grafana.com/docs/k6/latest/testing-guides/test-types/spike-testing/
    - [k6 load tests] https://grafana.com/docs/k6/latest/testing-guides/test-types/load-testing/
    - [pandas resampling] https://pandas.pydata.org/docs/reference/api/pandas.api.typing.DataFrameGroupBy.resample.html#pandas.api.typing.DataFrameGroupBy.resample
    - [pandas aggregation] https://pandas.pydata.org/docs/reference/api/pandas.api.typing.DataFrameGroupBy.agg.html#pandas.api.typing.DataFrameGroupBy.agg
    - [plotting refresher] https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.plot.html#matplotlib.pyplot.plot
    - [plot layout] https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.tight_layout.html#matplotlib.pyplot.tight_layout
- Q5
    - [prepping env variables for django] https://medium.com/python-in-my-pajamas/using-os-environ-to-manage-your-django-settings-the-easy-way-d2db96e73ab9
    - [playwright interactions with html forms] https://playwright.dev/python/docs/input
    - [page API and how to access different elements with playwright] https://playwright.dev/python/docs/writing-tests
- Q7
    - References here are generally similar to Q3 + plus this one:
    - [django reverse url handling] https://docs.djangoproject.com/en/6.0/ref/urlresolvers/#reverse
- Q9
    - [workflow jobs syntax and examples] https://runs-on.com/github-actions/jobs-and-steps/
    - [using secrets in workflow envs] https://docs.github.com/en/actions/how-tos/write-workflows/choose-what-workflows-do/use-secrets