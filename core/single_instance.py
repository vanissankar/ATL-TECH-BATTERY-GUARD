import socket

PORT = 56565

_socket = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
)

try:

    _socket.bind(
        ("127.0.0.1", PORT)
    )

    IS_PRIMARY = True

except OSError:

    IS_PRIMARY = False