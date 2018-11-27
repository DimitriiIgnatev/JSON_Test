# JSON Test
Templates for API Tests

## For running tests use next lines:

touch token.txt

export PASS='*'

export TEST_URL='demo.*.com'

export APIUSERTEST='apiusertest@*.com'

pytest -v test_json.py

pytest -s --junitxml=pytests.xml --cov-report xml --cov-report term --cov-branch --cov=test_json test_json.py

pytest -v --collect-only test_json.py

pytest -v --fulltrace test_json.py

pytest -v --alluredir=/var/tmp/allure/ test_json.py

/home/linuxbrew/.linuxbrew/bin/allure generate -o /var/tmp/allure/output/ -- /var/tmp/allure/


```python
'{"status":"success","orderStatus":"created and executed","yourOrderRef":"147","kantoxOrderRef":"O-6G7NZM3GY","currency":"EUR","counterCurrency":"USD","amount":147.0,"valueDate":"30/11/2018","beneficiaryAccountRef":"BA-MVBDZBL3Z","marketDirection":"buy","settlementStatus":"Creating instructions","counterValue":166.71,"rate":1.1341,"ratePair":"EUR/USD","executionTimeStamp":"27/11/2018 00:19:20 UTC"}'
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
