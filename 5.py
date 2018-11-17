import pytest
import socket as s
from hamcrest import *

SOCKET_ERROR = s.error

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
