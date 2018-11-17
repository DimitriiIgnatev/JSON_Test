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


def test_server_connect(socket, Server):
    socket.connect(Server.host_port)
    assert socket
