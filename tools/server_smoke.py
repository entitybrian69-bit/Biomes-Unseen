#!/usr/bin/env python3
"""Use RCON to check worldgen and the Hollow Deep in a running test server."""
import os
import socket
import struct
import sys
import time


def read_exact(sock, length):
    data = bytearray()
    while len(data) < length:
        chunk = sock.recv(length - len(data))
        if not chunk:
            raise ConnectionError("RCON closed the connection")
        data.extend(chunk)
    return bytes(data)


def send_packet(sock, packet_id, packet_type, text):
    body = struct.pack("<ii", packet_id, packet_type) + text.encode("utf-8") + b"\x00\x00"
    sock.sendall(struct.pack("<i", len(body)) + body)


def read_packet(sock):
    size = struct.unpack("<i", read_exact(sock, 4))[0]
    body = read_exact(sock, size)
    packet_id, packet_type = struct.unpack("<ii", body[:8])
    return packet_id, packet_type, body[8:-2].decode("utf-8", errors="replace")


def command(sock, packet_id, text):
    send_packet(sock, packet_id, 2, text)
    while True:
        response_id, _packet_type, response = read_packet(sock)
        if response_id == packet_id:
            print("RCON %s -> %s" % (text, response), flush=True)
            return response
        if response_id == -1:
            raise RuntimeError("RCON command rejected: " + response)


def connect(port, password):
    last_error = None
    for _ in range(30):
        try:
            sock = socket.create_connection(("127.0.0.1", port), timeout=5)
            sock.settimeout(120)
            send_packet(sock, 1, 3, password)
            packet_id, _packet_type, response = read_packet(sock)
            if packet_id == -1:
                raise PermissionError("RCON authentication failed")
            return sock
        except (OSError, ConnectionError) as error:
            last_error = error
            time.sleep(1)
    raise ConnectionError("Could not connect to RCON: %s" % last_error)


def main():
    port = int(os.environ.get("RCON_PORT", "25575"))
    password = os.environ.get("RCON_PASSWORD", "arena-smoke")
    with connect(port, password) as sock:
        biome = command(sock, 2, "locate biome biomesunseen:amber_meadow")
        if "Could not find" in biome or "Unknown" in biome:
            raise RuntimeError("The custom Overworld biome is not locatable")
        structure = command(sock, 3, "locate structure biomesunseen:windmill_ruin")
        if "Unknown structure" in structure:
            raise RuntimeError("The custom structure is not registered")
        dimension = command(sock, 4, "execute in biomesunseen:hollow_deep run time query daytime")
        if "Unknown dimension" in dimension or "Unparseable" in dimension:
            raise RuntimeError("Hollow Deep is not available to the server")
        send_packet(sock, 5, 2, "stop")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print("Worldgen smoke test failed: %s" % exc, file=sys.stderr)
        sys.exit(1)
