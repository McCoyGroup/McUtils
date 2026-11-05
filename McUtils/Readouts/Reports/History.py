"""
Snapshots of a `ReportDocument` and the differences between them: what a person (or a model) changed, as a list of
added, removed, changed and moved blocks. Used by `ReportDocument.snapshot` / `diff` / `transaction`.
"""

import copy

__all__ = ["DocumentSnapshot", "diff_snapshots"]


def _clip(text, n=200):
    text = str(text)
    return text if len(text) <= n else text[:n - 1] + "…"


class DocumentSnapshot:
    """An independent copy of a document's blocks, recorded sources, id counters and locked ids."""

    def __init__(self, doc):
        self.blocks, self.sources, self.counters, self.locked = copy.deepcopy(
            (doc.blocks, doc.sources, doc._counters, list(doc.meta.get("locked", []))))

    def rows(self):
        """``({id: {kind, fields...}}, [ids in order])``"""
        rows, order = {}, []
        for b in self.blocks:
            row = {"kind": b.kind}
            row.update({k: v for k, v in vars(b).items() if k != "id"})
            rows[b.id] = row
            order.append(b.id)
        return rows, order

    def restore(self, doc):
        doc.blocks, doc.sources, doc._counters = copy.deepcopy((self.blocks, self.sources, self.counters))
        if self.locked:
            doc.meta["locked"] = list(self.locked)
        else:
            doc.meta.pop("locked", None)

    def diff(self, other):
        """The changes from this snapshot to ``other`` (see `diff_snapshots`)."""
        return diff_snapshots(self, other)


def _summary(row):
    out = {"kind": row["kind"]}
    if row["kind"] == "readout":
        out.update(handle=row.get("handle"), include=row.get("include"))
        if row.get("caption"):
            out["caption"] = _clip(row["caption"], 80)
    else:
        for k in ("level", "role", "callout_kind"):
            if k in row:
                out[k] = row[k]
        out["text"] = _clip(row.get("text", ""), 80)
    return out


def _moved(old_order, new_order):
    """Ids present in both orders that changed place (all but a longest run that kept its order)."""
    common = set(old_order) & set(new_order)
    pos = {b: i for i, b in enumerate(old_order) if b in common}
    seq = [b for b in new_order if b in common]
    if not seq:
        return []
    best, prev = [], []
    for i, b in enumerate(seq):
        k, j = 1, -1
        for m in range(i):
            if pos[seq[m]] < pos[b] and best[m] + 1 > k:
                k, j = best[m] + 1, m
        best.append(k)
        prev.append(j)
    i = max(range(len(seq)), key=best.__getitem__)
    keep = set()
    while i != -1:
        keep.add(seq[i])
        i = prev[i]
    return [b for b in seq if b not in keep]


def diff_snapshots(old, new):
    """
    ``[{op, id, ...}]`` from ``old`` to ``new``: ``added`` (with ``after``, the block it follows or ``"start"``, and a
    short ``block`` summary), ``removed`` (with ``block``), ``changed`` (``fields: {name: {from, to}}``) and ``moved``
    (with ``after``). When blocks swap places, one of the two is reported as the move.
    """
    old_rows, old_order = old.rows()
    new_rows, new_order = new.rows()
    changes = []
    for i, b in enumerate(new_order):
        if b not in old_rows:
            changes.append({"op": "added", "id": b, "after": new_order[i - 1] if i else "start",
                            "block": _summary(new_rows[b])})
    for b in old_order:
        if b not in new_rows:
            changes.append({"op": "removed", "id": b, "block": _summary(old_rows[b])})
    for b in new_order:
        if b in old_rows and old_rows[b] != new_rows[b]:
            fields = {k: {"from": _clip(old_rows[b].get(k)), "to": _clip(new_rows[b].get(k))}
                      for k in sorted(set(old_rows[b]) | set(new_rows[b])) if old_rows[b].get(k) != new_rows[b].get(k)}
            changes.append({"op": "changed", "id": b, "fields": fields})
    for b in _moved(old_order, new_order):
        i = new_order.index(b)
        changes.append({"op": "moved", "id": b, "after": new_order[i - 1] if i else "start"})
    return changes
