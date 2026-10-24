"""Readable JSON writer: objects that fit in `width` columns stay on one line."""
import json
import os


def fmt(o, ind=0, width=100):
    s = json.dumps(o, separators=(", ", ": "), ensure_ascii=False)
    if not isinstance(o, (dict, list)) or len(s) + 2 * ind <= width:
        return s
    pad = "  " * (ind + 1)
    if isinstance(o, dict):
        items = ["%s%s: %s" % (pad, json.dumps(k), fmt(v, ind + 1, width)) for k, v in o.items()]
        return "{\n" + ",\n".join(items) + "\n" + "  " * ind + "}"
    return "[\n" + ",\n".join(pad + fmt(v, ind + 1, width) for v in o) + "\n" + "  " * ind + "]"


def write(path, obj, width=100):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(fmt(obj, 0, width) + "\n")
