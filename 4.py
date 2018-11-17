import pytest
import socket as s


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
    socket.connect(Server.host_port)
    assert socket
