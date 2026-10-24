#!/usr/bin/env python3
"""Use RCON to check worldgen and the Hollow Deep in a running test server."""
import json
import os
import re
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


def parse_location(response, label):
    match = re.search(r"\[(-?\d+),\s*(?:-?\d+|~),\s*(-?\d+)\]", response)
    if not match:
        raise RuntimeError("Could not parse %s location from RCON response: %s" % (label, response))
    return int(match.group(1)), int(match.group(2))


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
        biome_pos = parse_location(biome, "biome")
        structure = command(sock, 3, "locate structure biomesunseen:windmill_ruin")
        if "Unknown structure" in structure or "Could not find" in structure:
            raise RuntimeError("The custom structure is not locatable")
        structure_pos = parse_location(structure, "structure")
        dimension = command(sock, 4, "execute in biomesunseen:hollow_deep run time query daytime")
        if "Unknown dimension" in dimension or "Unparseable" in dimension:
            raise RuntimeError("Hollow Deep is not available to the server")
        portal = command(sock, 5, "setblock 128 120 128 biomesunseen:hollow_portal")
        if "Unknown block" in portal or "Failed" in portal or "Could not" in portal:
            raise RuntimeError("Hollow Portal block could not be placed")
        verify_portal = command(sock, 6,
                                "execute if block 128 120 128 biomesunseen:hollow_portal run setblock 129 120 128 biomesunseen:hollow_portal")
        if "Changed block at" not in verify_portal:
            raise RuntimeError("Hollow Portal block did not remain in the world after placement")
        command(sock, 7, "setblock 128 120 128 air")
        command(sock, 8, "setblock 129 120 128 air")
        for packet_id, (x, z) in ((9, biome_pos), (10, structure_pos)):
            command(sock, packet_id, "forceload add %d %d" % (x, z))
        time.sleep(5)
        for packet_id, (x, z) in ((11, biome_pos), (12, structure_pos)):
            command(sock, packet_id, "forceload remove %d %d" % (x, z))
        command(sock, 13, "save-all flush")
        with open("worldgen-smoke.json", "w", encoding="utf-8") as report:
            json.dump({"biome": {"id": "biomesunseen:amber_meadow", "x": biome_pos[0], "z": biome_pos[1]},
                       "structure": {"id": "biomesunseen:windmill_ruin", "x": structure_pos[0], "z": structure_pos[1]}},
                      report, indent=2)
        send_packet(sock, 14, 2, "stop")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print("Worldgen smoke test failed: %s" % exc, file=sys.stderr)
        sys.exit(1)
