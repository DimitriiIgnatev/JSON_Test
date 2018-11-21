# JSON Test
Templates for API Tests

## For running tests use next lines:

touch token.txt

export PASS='*'

export TEST_URL='demo.*.com'

export APIUSERTEST='apiusertest@*.com'

pytest -s 15.py

```python
'{"status":"error","reason":8,"errorDetails":"market_direction: Market Direction is required / currency: Currency is required / amount: Amount is required / counter_currency: Counter Currency is required / value_date: Value Date is required"}'
```

## Description

For these tests, pytest was used with all the necessary options.

FrameWorks:  

[PyHamcrest](https://github.com/hamcrest/PyHamcrest) 

[Requests](http://docs.python-requests.org/en/master/user/quickstart/#json-response-content)

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
  
