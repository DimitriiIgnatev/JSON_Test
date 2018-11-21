import pytest
import os
import sys
import socket as s
from hamcrest import *
from hamcrest.core.base_matcher import BaseMatcher
from hamcrest.core.helpers.wrap_matcher import wrap_matcher
import requests
import json as j

SOCKET_ERROR = s.error

try:
    os.environ["PASS"]
except KeyError: 
    print "Please set the environment variable PASS"
    sys.exit(1)

try:
    os.environ["TEST_URL"]
except KeyError: 
    print "Please set the environment variable TEST_URL"
    sys.exit(1)

apiusertest = 'apiusertest@kantox.com'

demo_token_key = 'token'
demo_token = ''

reverse_words = lambda words: [word[::-1] for word in words]

class BaseModifyMatcher(BaseMatcher):
    def __init__(self, item_matcher):
        self.item_matcher = item_matcher

    def _matches(self, item):
        if isinstance(item, self.instance) and item:
            self.new_item = self.modify(item)
            return self.item_matcher.matches(self.new_item)
        else:
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


@pytest.fixture(scope='module')
def Server():
    class Dummy:
        test_url=os.environ["TEST_URL"]
        host_port = test_url, 443
        uri = 'https://%s:%s/api/login' % host_port
    return Dummy

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

#def test_server_connect(socket, Server):
#    assert_that(calling(socket.connect).with_args(Server.host_port), is_not(raises(SOCKET_ERROR)))

#def test_server_response(Server):
#    assert_that(requests.get(Server.uri), all_of(has_content('text not found'), has_status(501)))

def idparametrize(name, values, fixture=False):
    return pytest.mark.parametrize(name, values, ids=map(repr, values), indirect=fixture)

class DefaultCase:
    def __init__(self, text):
        self.password=os.environ["PASS"]
        self.text = text
        self.req = dict(
#            params={'text': self.text},
            data={'login': text, 'password': self.password},
            headers={'content-type': 'multipart/form-data'},
        )
#        self.req['headers'].update({'content-type': 'multipart/form-data'})

        self.match_string_of_reversed_words = all_of(
#            has_content(contains_reversed_words(text.split())),
            has_content('success'),
            has_status(200),
        )

    def __repr__(self):
        return 'text="{text}", {cls}, {req}'.format(cls=self.__class__.__name__, text=self.text, req=self.req)

class JSONCase(DefaultCase):
    def __init__(self, text):
        DefaultCase.__init__(self, text)
        self.req['headers'].update({'Accept': 'application/json'})

        self.match_string_of_reversed_words = all_of(
            has_content(is_json(has_entries('status', contains('success')))),
            has_status(200),
        )


#                                  for testclazz in JSONCase, DefaultCase])

@idparametrize('case', [testclazz(login)
                                  for login in [apiusertest]
                                  for testclazz in DefaultCase, JSONCase ])
def test_server_request(case, Server):
    json_str = j.loads(requests.post(Server.uri, **case.req).text)
    print json_str
    demo_token = json_str[demo_token_key]
    print demo_token
    assert_that(requests.post(Server.uri, **case.req), case.match_string_of_reversed_words)
