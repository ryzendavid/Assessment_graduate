"""
PRACTICE TASK: Transactional key-value store (Lloyds OA style)
Target time: 35 minutes. No AI, no looking things up.

Implement KVStore so that all the tests at the bottom pass.

Spec
----
set(key, value)   -> store value under key
get(key)          -> return value, or None if key doesn't exist
delete(key)       -> remove key; return True if it existed, else False
begin()           -> start a new transaction (transactions can be NESTED)
commit()          -> commit the innermost transaction into its parent
                     (or into the main store if it's the outermost one).
                     Return False if there is no active transaction, else True.
rollback()        -> discard every change made in the innermost transaction.
                     Return False if there is no active transaction, else True.

Rules
-----
- get() must see uncommitted changes from ALL open transactions.
- A delete inside a transaction must hide the key, and rollback must bring it back.
- Rolling back an inner transaction must NOT undo the outer transaction's changes.

Hint (read only if stuck after 10 mins):
  Keep a stack (list) of dicts, one per open transaction. Use a sentinel
  object to mark "deleted in this layer". get() walks the stack from top to bottom.

Run:  python3 kv_store_practice.py
"""

deleted = object()

class KVStore:
    def __init__(self):
       self.data = {}
       self.stack = []

    def set(self, key, value):
        if self.stack:
            self.stack[-1][key] = value
        else:
            self.data[key] = value

    def get(self, key):
        #check transaction from new to old
        for layer in reversed(self.stack):
            if key in layer:
                value = layer[key]
                return None if value is deleted else value
        return self.data.get(key)

    def delete(self, key):
        #first checks if key exists
        if self.get(key) is None:
            return False

        #check if transaction is open then mark deleted else remove from main store
        if self.stack:
            self.stack[-1][key] = deleted
        else:
            del self.data[key]

        return True

    def begin(self):
        pass  # TODO

    def commit(self):
        pass  # TODO

    def rollback(self):
        pass  # TODO


# ---------------- TESTS (don't edit below) ----------------

def run_tests():
    tests = []

    def test(fn):
        tests.append(fn)
        return fn

    @test
    def basic_set_get():
        s = KVStore()
        s.set("a", 1)
        assert s.get("a") == 1
        assert s.get("missing") is None

    @test
    def overwrite():
        s = KVStore()
        s.set("a", 1); s.set("a", 2)
        assert s.get("a") == 2

    @test
    def delete_basic():
        s = KVStore()
        s.set("a", 1)
        assert s.delete("a") is True
        assert s.get("a") is None
        assert s.delete("a") is False

    @test
    def no_transaction_commit_rollback():
        s = KVStore()
        assert s.commit() is False
        assert s.rollback() is False

    @test
    def rollback_undoes_set():
        s = KVStore()
        s.set("a", 1)
        s.begin(); s.set("a", 2)
        assert s.get("a") == 2
        assert s.rollback() is True
        assert s.get("a") == 1

    @test
    def commit_keeps_set():
        s = KVStore()
        s.begin(); s.set("a", 5)
        assert s.commit() is True
        assert s.get("a") == 5
        assert s.rollback() is False  # nothing left open

    @test
    def rollback_restores_deleted():
        s = KVStore()
        s.set("a", 1)
        s.begin()
        assert s.delete("a") is True
        assert s.get("a") is None
        s.rollback()
        assert s.get("a") == 1

    @test
    def nested_inner_rollback_keeps_outer():
        s = KVStore()
        s.begin(); s.set("a", 1)
        s.begin(); s.set("a", 2); s.set("b", 3)
        s.rollback()
        assert s.get("a") == 1
        assert s.get("b") is None
        s.commit()
        assert s.get("a") == 1

    @test
    def nested_inner_commit_then_outer_rollback():
        s = KVStore()
        s.set("a", 0)
        s.begin(); s.set("a", 1)
        s.begin(); s.set("a", 2)
        s.commit()                 # inner merges into outer
        assert s.get("a") == 2
        s.rollback()               # outer rollback discards everything
        assert s.get("a") == 0

    @test
    def delete_then_set_in_nested():
        s = KVStore()
        s.set("x", "base")
        s.begin(); s.delete("x")
        s.begin(); s.set("x", "new")
        assert s.get("x") == "new"
        s.rollback()
        assert s.get("x") is None
        s.commit()
        assert s.get("x") is None
        assert s.delete("x") is False

    @test
    def delete_missing_inside_transaction():
        s = KVStore()
        s.begin()
        assert s.delete("ghost") is False
        s.commit()
        assert s.get("ghost") is None

    @test
    def falsy_values_are_real_values():
        s = KVStore()
        s.set("zero", 0); s.set("empty", "")
        s.begin(); s.set("zero", None if False else 0)
        s.commit()
        assert s.get("zero") == 0
        assert s.get("empty") == ""

    passed = 0
    for fn in tests:
        try:
            fn()
            print(f"PASS  {fn.__name__}")
            passed += 1
        except Exception as e:
            print(f"FAIL  {fn.__name__}  ({type(e).__name__}: {e})")
    print(f"\n{passed}/{len(tests)} passed")


if __name__ == "__main__":
    run_tests()