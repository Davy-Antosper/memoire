# -*- coding: utf-8 -*-
"""Encode/decode PlantUML text <-> URL (algorithme officiel), et telechargement PNG/SVG."""
import sys
import zlib
import urllib.request

B64 = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-_"
IDX = {c: i for i, c in enumerate(B64)}


def _append3bytes(b1, b2, b3, out):
    out.append(B64[(b1 >> 2) & 0x3F])
    out.append(B64[(((b1 & 0x3) << 4) | ((b2 >> 4) & 0xF)) & 0x3F])
    out.append(B64[(((b2 & 0xF) << 2) | ((b3 >> 6) & 0x3)) & 0x3F])
    out.append(B64[b3 & 0x3F])


def encode(text):
    data = zlib.compress(text.encode("utf-8"), 9)[2:-4]
    out = []
    for i in range(0, len(data), 3):
        chunk = data[i:i + 3]
        b = [c for c in chunk] + [0] * (3 - len(chunk))
        _append3bytes(b[0], b[1], b[2], out)
    return "".join(out)


def decode(encoded):
    vals = [IDX[c] for c in encoded]
    raw = bytearray()
    for i in range(0, len(vals), 4):
        chunk = vals[i:i + 4]
        while len(chunk) < 4:
            chunk.append(0)
        c1, c2, c3, c4 = chunk
        raw.append(((c1 << 2) | (c2 >> 4)) & 0xFF)
        raw.append((((c2 & 0xF) << 4) | (c3 >> 2)) & 0xFF)
        raw.append((((c3 & 0x3) << 6) | c4) & 0xFF)
    data = b"\x78\x9c" + bytes(raw)
    dec = zlib.decompressobj()
    out = dec.decompress(data)
    return out.decode("utf-8", errors="replace")


def url_for(text, fmt="png"):
    return f"https://www.plantuml.com/plantuml/{fmt}/{encode(text)}"


def fetch(text, out_path, fmt="png"):
    u = url_for(text, fmt)
    req = urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=90) as resp:
        blob = resp.read()
    with open(out_path, "wb") as fh:
        fh.write(blob)
    return len(blob), u


if __name__ == "__main__":
    mode = sys.argv[1]
    if mode == "decode":
        print(decode(sys.argv[2]))
    elif mode == "encode":
        with open(sys.argv[2], encoding="utf-8") as fh:
            print(url_for(fh.read(), sys.argv[3] if len(sys.argv) > 3 else "png"))