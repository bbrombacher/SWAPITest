Install & Download dependencies (mainly pytest and requests)
1. Clone git project with https://github.com/bbrombacher/SWAPITest.git
2. Open terminal, navigate to project root directory
3. Type pip install -r requirements.txt

Run tests
1. Open terminal, navigate to project tests folder.
2. Run all Tests: pytest
3. Run a specific test file: pytest test_swapi.py (or other test_name.py file)
4. Run a specific test within a file: pytest test.swapi.py::TestSwapi::test_TESTNAME
5. More run details can be found at https://docs.pytest.org/en/latest/
