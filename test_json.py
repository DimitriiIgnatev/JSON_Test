#/usr/bin/env python
# coding: utf-8

"""
Test API.
"""

from __future__ import print_function
import os
import sys
import socket as s
import json as j
from collections import namedtuple
import pytest
from hamcrest import * # pylint: disable=wildcard-import
from hamcrest.core.base_matcher import BaseMatcher
from hamcrest.core.helpers.wrap_matcher import wrap_matcher
import requests
import allure

SOCKET_ERROR = s.error
ERROR_CONDITION = None

try:
    os.environ["PASS"]
except KeyError:
    print("Please set the environment variable PASS")
    sys.exit(1)

try:
    os.environ["TEST_URL"]
except KeyError:
    print("Please set the environment variable TEST_URL")
    sys.exit(1)

try:
    os.environ["APIUSERTEST"]
except KeyError:
    print("Please set the environment variable APIUSERTEST")
    sys.exit(1)


DEMO_TOKEN_KEY = 'token'
Srv = namedtuple('Server', 'host port link')
Case = namedtuple('Case', 'token data')
TEST_URL = os.environ["TEST_URL"]
APIUSERTEST = os.environ["APIUSERTEST"]

class BaseModifyMatcher(BaseMatcher):
    """A matcher that modify check value and pass it following the specified matcher."""
    def __init__(self, item_matcher):
#        BaseMatcher.__init__(self, item_matcher)
        self.item_matcher = item_matcher

    def _matches(self, item):
        if isinstance(item, self.instance) and item:
            self.new_item = self.modify(item)
            return self.item_matcher.matches(self.new_item)
        return False

    def describe_mismatch(self, item, mismatch_description):
        if isinstance(item, self.instance) and item:
            self.item_matcher.describe_mismatch(self.new_item, mismatch_description)
        else:
            mismatch_description.append_text('not %s, was: ' % self.instance) \
                                .append_text(repr(item))

    def describe_to(self, description):
        description.append_text(self.description) \
                   .append_text(' ') \
                   .append_description_of(self.item_matcher)



@pytest.yield_fixture
def socket():
    _socket = s.socket(s.AF_INET, s.SOCK_STREAM)
    yield _socket
    _socket.close()

@pytest.yield_fixture
def Server(request):
    class Dummy:
        def  __init__(self, srv):
            self.srv = srv
            self.conn = None

        @property
        def uri(self):
            return 'https://{host}/{link}'.format(**self.srv._asdict())

        def connect(self):
            self.conn = s.create_connection((self.srv.host, self.srv.port))
            self.conn.sendall('HEAD /404 HTTP/1.0\r\n\r\n')
            self.conn.recv(1024)

        def close(self):
            if self.conn:
                self.conn.close()



    res = Dummy(request.param)
    yield res
    res.close()


@pytest.yield_fixture(scope='function', autouse=True)
def collect_logs(request):
    if 'Server' in request.fixturenames:
#        with some_logfile_collector(SERVER_LOCATION):
        yield
    else:
        yield


# In that lib payload content in param text, when we get it, we start parsing
def has_content(item):
    return has_property('text', item if isinstance(item, BaseMatcher) else contains_string(item))


def has_status(status):
    return has_property('status_code', equal_to(status))


def contains_reversed_words(item_match):
    """
    Example:
        >>> from hamcrest import *
        >>> contains_reversed_words(contains_inanyorder('oof', 'rab')).matches("foo bar")
        True
    """
    class IsStringOfReversedWords(BaseModifyMatcher):
        description = 'string of reversed words'
        modify = lambda _, item: reverse_words(item.split())
        instance = basestring

    return IsStringOfReversedWords(wrap_matcher(item_match))

def is_json(item_match):
    """
    Example:
        >>> from hamcrest import *
        >>> is_json(has_entries('foo', contains('bar'))).matches('{"foo": ["bar"]}')
        True
    """
    class AsJson(BaseModifyMatcher):
        description = 'json with'
        modify = lambda _, item: j.loads(item)
        instance = basestring
    return AsJson(wrap_matcher(item_match))

def idparametrize(name, values, fixture=False):
    return pytest.mark.parametrize(name, values, ids=list(map(repr, values)), indirect=fixture)

@pytest.fixture
def error_if_wat(request):
    assert request.getfuncargvalue('Server').srv != ERROR_CONDITION


class DefaultCase:
    def __init__(self, text):
        self.text = text
        self.req = dict(
            headers={'content-type': 'application/x-www-form-urlencoded; charset=utf-8'},
            data={},
            params={},
        )

        self.match_string_of_reversed_words = all_of(
            has_content('success'),
            has_status(200),
        )

    def __repr__(self):
#        return 'text="{text}", {cls}, {req}'.format(cls=self.__class__.__name__, \
#            text=self.text, req=self.req)
        return 'text="{text}", {cls}'.format(cls=self.__class__.__name__, text=self.text)


class DefaultCaseLogin(DefaultCase):
    def __init__(self, text):
        DefaultCase.__init__(self, text)
        self.password = os.environ["PASS"]
        self.req['params'].update({'login': self.text, 'password': self.password})
        self.req['headers'].update({'content-type' : 'multipart/form-data'})
        self.req['headers'].update({'Accept': 'application/json'})

        self.match_login_token = all_of(
            has_status(200),
            has_content('status'),
            has_content('success'),
            has_content(DEMO_TOKEN_KEY),
        )



class JSONCase(DefaultCase):
    def __init__(self, text):
        DefaultCase.__init__(self, text)
        self.req['headers'].update({'Accept': 'application/json'})
        self.req['headers'].update({'X-ACCESS-TOKEN': self.text})

        self.match_string = all_of(
            has_content('success'),
            has_status(200),
        )


class JSONCaseData(DefaultCase):
    def __init__(self, text, data):
        DefaultCase.__init__(self, text)
        self.req['headers'].update({'Accept': 'application/json'})
        self.req['headers'].update({'X-ACCESS-TOKEN': self.text})
        self.req['data'].update(data)

        self.match_string = all_of(
            has_content('success'),
            has_content('orderStatus'),
            has_content('yourOrderRef'),
            has_content('kantoxOrderRef'),
            has_content('counterCurrency'),
            has_content('amount'),
            has_content('currency'),
            has_content('valueDate'),
            has_content('beneficiaryAccountRef'),
            has_content('marketDirection'),
            has_content('settlementStatus'),
            has_content('counterValue'),
            has_content('rate'),
            has_content('ratePair'),
            has_content('executionTimeStamp'),
            has_status(200),
        )

def my_token():
    f = open('/tmp/token.txt', 'r')
    demo_token = f.read()
    f.close()
    return demo_token

# Need run it before every tests. We keep demo_token for next requests.

@idparametrize('Server', [Srv(TEST_URL, 433, 'api/login')], fixture=True)
@idparametrize('case', [testclazz(login)
                        for login in [APIUSERTEST]
                        for testclazz in [DefaultCaseLogin]])
def test_server_login(case, Server):
    res_req = requests.post(Server.uri, **case.req)
    json_str = j.loads(res_req.text)
    demo_token = json_str[DEMO_TOKEN_KEY]
    print (demo_token)
    f = open('/tmp/token.txt', 'w')
    f.write(demo_token)
    f.close()
#    assert_that(demo_token, has_length(20))
    assert_that(demo_token)

data = {'orderRef': 147, 'marketDirection': 'buy', 'currency': 'EUR', 'amount': '147.00', 'counterCurrency': 'USD', 'beneficiaryAccountRef': 'BA-MVBDZBL3Z', 'paymentPurpose': 'services', 'valueDate': '30/11/2018'}



SERVER_CASES = [
    Srv(TEST_URL, 433, 'api/companies/6XXDG5K6C/orders/create'),
]
@idparametrize('Server', SERVER_CASES, fixture=True)
@idparametrize('case', [JSONCaseData(my_token(), data)])
def test_server(case, Server, error_if_wat):
    """
    Step 1:
        Try connect to host, port,
        and check for not raises SOCKET_ERROR.

    Step 2:
        Check for server response 'data' message.
        Response status should be equal to 501.
    """
#    with allure.step('Try connect'):
#        assert_that(calling(Server.connect), is_not(raises(SOCKET_ERROR)))

    with allure.step('Check response'):
        response = requests.post(Server.uri, **case.req)
        allure.attach('response_body', response.text)
        allure.attach('response_headers', j.dumps(dict(response.headers), indent=4))
        allure.attach('response_url', response.url)
        allure.attach('response_status', str(response.status_code))
        assert_that(response, case.match_string)
