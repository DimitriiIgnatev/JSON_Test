# JSON Test
Templates for API Tests

## For running tests use next lines:

touch token.txt

export PASS='*'

export TEST_URL='demo.*.com'

export APIUSERTEST='apiusertest@*.com'

pytest -s 15.py

pytest -s --junitxml=pytests.xml --cov-report xml --cov-report term --cov-branch --cov=15 15.py

pytest -s --collect-only 15.py

pytest -s --fulltrace 15.py

pytest -v --alluredir=/var/tmp/allure/ 16.py

/home/linuxbrew/.linuxbrew/bin/allure generate -o /var/tmp/allure/output/ -- /var/tmp/allure/


```python
'{"status":"error","reason":8,"errorDetails":"market_direction: Market Direction is required / currency: Currency is required / amount: Amount is required / counter_currency: Counter Currency is required / value_date: Value Date is required"}'
```

## Description

For these tests, pytest was used with all the necessary options.

FrameWorks: 

[Pytest](http://pytest.org/latest/apiref.html)

[PyHamcrest](https://github.com/hamcrest/PyHamcrest) 

[Requests](http://docs.python-requests.org/en/master/user/quickstart/#json-response-content)

[Allure2](https://github.com/allure-framework/allure2)

Have been used:

[Test fixture](http://en.wikipedia.org/wiki/Test_fixture#Software)
 
### Fixtures come to the rescue when needed:
 
 * generate test data;
 * prepare test bench;
 * to change the behavior of the stand;
 * to write setUp/tearDown;
 * to collect logs of the services or crashdump;
 * use system emulators or stubs;
 * and much more.
 
[Matcher](http://docs.oracle.com/javase/7/docs/api/java/util/regex/Matcher.html)
 
[Parameterization](https://blogs.msdn.microsoft.com/jledgard/2003/11/03/software-testing-6-good-tests-for-bad-parameters/)

[Marks](https://docs.pytest.org/en/latest/reference.html#marks)
