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
