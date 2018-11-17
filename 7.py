import pytest
import socket as s
from hamcrest import *
from hamcrest.core.base_matcher import BaseMatcher
import json as j

SOCKET_ERROR = s.error

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
        host_port = 'demo.*.com', 80
        uri = 'http://%s:%s/' % host_port
    return Dummy

@pytest.yield_fixture(scope='function', autouse=True)
def collect_logs(request):
    if 'Server' in request.fixturenames:
#        with some_logfile_collector(SERVER_LOCATION):
            yield
    else:
        yield


def test_server_connect(socket, Server):
    assert_that(calling(socket.connect).with_args(Server.host_port), is_not(raises(SOCKET_ERROR)))

def has_content(item):
    return has_property('text', item if isinstance(item, BaseMatcher) else contains_string(item))

def has_status(status):
    return has_property('status_code', equal_to(status))

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
