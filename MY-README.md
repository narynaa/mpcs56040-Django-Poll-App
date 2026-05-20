## Code changes & Setup
The only code changes made to the existing application code were adding the following ones:
- Two new dependecies to the `requirements.txt` file
- Existing unit tests from polls/tests.py were renamed to polls/tests_legacy.py (to avoid name collision with my new unit tests)
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
