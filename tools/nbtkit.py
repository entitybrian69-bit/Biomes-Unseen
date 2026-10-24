"""Minimal NBT writer for structure templates (standard library only)."""
import gzip
import re
import struct

T_BYTE, T_INT, T_DOUBLE, T_STRING, T_LIST, T_COMPOUND = 1, 3, 6, 8, 9, 10
DATA_VERSION = 3465  # Minecraft 1.20.1


def w_str(s):
    raw = s.encode("utf-8")
    return struct.pack(">H", len(raw)) + raw


def p_list(tag_id, payloads):
    return bytes([tag_id]) + struct.pack(">i", len(payloads)) + b"".join(payloads)


def p_compound(fields):
    """fields: list of (tag_id, name, payload)."""
    return b"".join(bytes([t]) + w_str(n) + p for t, n, p in fields) + b"\x00"


def p_int_list(values):
    return p_list(T_INT, [struct.pack(">i", v) for v in values])


def p_double_list(values):
    return p_list(T_DOUBLE, [struct.pack(">d", v) for v in values])


def state_compound(spec):
    """'minecraft:ladder[facing=south]' -> palette compound with Name and Properties."""
    match = re.match(r"^([a-z0-9_:]+)(?:\[(.*)\])?$", spec)
    fields = [(T_STRING, "Name", w_str(match.group(1)))]
    if match.group(2):
        props = [tuple(kv.split("=")) for kv in match.group(2).split(",")]
        fields.append((T_COMPOUND, "Properties", p_compound([(T_STRING, k, w_str(v)) for k, v in props])))
    return p_compound(fields)


def template(size, blocks, entities):
    """blocks: [(x, y, z, state, nbt_fields|None)]; entities: [(x, y, z, entity_id)]. Returns gzip bytes."""
    palette, index, block_payloads = [], {}, []
    for x, y, z, state, nbt in blocks:
        if state not in index:
            index[state] = len(palette)
            palette.append(state)
        fields = [(T_LIST, "pos", p_int_list([x, y, z])), (T_INT, "state", struct.pack(">i", index[state]))]
        if nbt:
            fields.append((T_COMPOUND, "nbt", p_compound(nbt)))
        block_payloads.append(p_compound(fields))
    entity_payloads = []
    for x, y, z, eid in entities:
        nbt = p_compound([(T_STRING, "id", w_str(eid)), (T_BYTE, "PersistenceRequired", b"\x01")])
        entity_payloads.append(p_compound([(T_LIST, "pos", p_double_list([x + 0.5, float(y), z + 0.5])),
                                           (T_LIST, "blockPos", p_int_list([x, int(y), z])),
                                           (T_COMPOUND, "nbt", nbt)]))
    root = p_compound([
        (T_INT, "DataVersion", struct.pack(">i", DATA_VERSION)),
        (T_LIST, "size", p_int_list(list(size))),
        (T_LIST, "palette", p_list(T_COMPOUND, [state_compound(s) for s in palette])),
        (T_LIST, "blocks", p_list(T_COMPOUND, block_payloads)),
        (T_LIST, "entities", p_list(T_COMPOUND, entity_payloads)),
    ])
    return gzip.compress(bytes([T_COMPOUND]) + w_str("") + root, 9)


def chest_nbt(loot_table):
    return [(T_STRING, "id", w_str("minecraft:chest")), (T_STRING, "LootTable", w_str(loot_table))]
