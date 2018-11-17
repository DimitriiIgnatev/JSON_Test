import pytest
import socket as s


@pytest.yield_fixture
def socket():
    _socket = s.socket(s.AF_INET, s.SOCK_STREAM)
    yield _socket
    _socket.close()

def test_server_connect(socket):
    socket.connect(('demo.*.com', 80))
    assert socket
