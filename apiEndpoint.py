"""
PRACTICE TASK 2: API endpoint with JSON validation (Lloyds OA style)
Target time: 35 minutes. No AI, no looking things up.

CONCEPT
-------
An API endpoint receives a request body as a raw STRING of JSON. Your job:
  1. Turn the string into Python data (json.loads)  -> may fail!
  2. Check every field is present and the right type/format
  3. Return an HTTP status code + a JSON-style dict response

Status codes you need:
  201 = Created (success)      400 = Bad Request (client sent bad data)

In the real test you may get a framework (Flask etc.) or just a function like
this one. Either way, the validation logic is the part being marked.

TASK: POST /payments
--------------------
Implement handle_create_payment(raw_body) -> (status_code, response_dict)

Checks, IN THIS ORDER (return on the first failure):

  1. raw_body isn't valid JSON          -> 400, {"error": "invalid_json"}
  2. parsed JSON isn't an object (dict) -> 400, {"error": "invalid_body"}
  3. For each required field, in this order:
        from_account, to_account, amount, currency
     - missing -> 400, {"error": "missing_field", "field": <name>}
     - invalid -> 400, {"error": "invalid_field", "field": <name>}

     Valid means:
       from_account / to_account : a string of exactly 8 digits, e.g. "12345678"
       amount   : a number (int or float, NOT a bool), finite, > 0,
                  at most 2 decimal places (10.5 ok, 10.555 not ok)
       currency : exactly the string "GBP"
  4. Optional field "reference": if present must be a string of max 18 chars
     - invalid -> 400, {"error": "invalid_field", "field": "reference"}
  5. from_account == to_account         -> 400, {"error": "same_account"}
  6. Otherwise -> 201 and:
       {"status": "accepted", "from_account": ..., "to_account": ...,
        "amount": ..., "currency": "GBP", "reference": <reference or "">}
  
  Extra unknown fields are ignored.

HINTS (read only if stuck)
--------------------------
- json.loads raises json.JSONDecodeError on bad input -> use try/except.
- isinstance(x, dict), isinstance(x, str), isinstance(x, (int, float))
- TRAP: True/False count as ints in Python! isinstance(True, int) is True.
- TRAP: Python's json accepts NaN and Infinity -> use math.isfinite().
- 2 decimal places: round(amount, 2) == amount
- "12345678".isdigit() and len(...) == 8
- Write a small helper for the two account fields so you don't repeat code.

Run:  python3 api_validation_practice.py
"""
import json
import math


    # return (status_code, response_dict)

    #func checks if acc number is valid, value must be provided and is 8 + digits
def is_valid_account(value):

        #first checks if value is a string, if yes, carries on. any other type returns false. also checks that len is 8 characters in the string
        return isinstance(value, str) and len(value) == 8 and value.isdigit()  #is digit checks that characters in the str are 0-9 only accepts these characters.. 
         #it will either returnb true/false

def is_valid_amount(value):

        #if val is bool, false... reason for this is that booleans are also ints (suprising??) it is 0/1.. if we were to ever put amount as true, this will return 1 or false 0
    if isinstance(value, bool):
        return False

        #if val is not int or float, false
    if not isinstance(value, (int,float)):
        return False

    if not math.isfinite(value):
        return False
        
    if value <= 0:
        return False

    return round(value, 2) == value

def handle_create_payment(raw_body):
    #parsing json (from json to py, usese .loads)

    try:
        data = json.loads(raw_body)
    except json.JSONDecodError:
        return 400, {"Error" : "invalid_body"}

    #should be an object
    if not isinstance(data, dict):
        return 400, {"Error" : "Invalid body"}

    #req fields.. in order

    required = [
        ("from_account", is_valid_account),
        ("to_account", is_valid_account),
        ("amount", is_valid_amount),
        ("currency", lambda v: v == "GBP"),
                ]

    for field, validator in required:
        if field not in data:
            return 400, {"Error" : "missing_field", "field" : field }

        if not validator (data[field]):
            return 400, {"Error" : "invalid_field", "field" : field}

    reference = data.get("reference", "")
    if not isinstance(reference, str) or len(reference) > 18:
        return 400, {"Error" : "invalid_field", "field" : field}

    if data["from_account"] == data["to_account"]:
        return 400, {"error" : "same_account"}

    #success

    return 201, {
        "status" : "accepted",
        "from_account" : data["from_account"],
        "to_account" : data["to_account"],
        "amount" : data["amount"],
        "currency" : "GBP",
        "reference" : reference
    }


    




# ---------------- TESTS (don't edit below) ----------------

def run_tests():
    def body(**kw):
        base = {"from_account": "11111111", "to_account": "22222222",
                "amount": 25.5, "currency": "GBP"}
        base.update(kw)
        return json.dumps({k: v for k, v in base.items() if v is not REMOVE})

    REMOVE = object()
    cases = [
        ("valid payment",
         body(), (201, {"status": "accepted", "from_account": "11111111",
                        "to_account": "22222222", "amount": 25.5,
                        "currency": "GBP", "reference": ""})),
        ("valid with reference + extra field",
         body(reference="Rent Nov", note="ignored"),
         (201, {"status": "accepted", "from_account": "11111111",
                "to_account": "22222222", "amount": 25.5,
                "currency": "GBP", "reference": "Rent Nov"})),
        ("integer amount ok",
         body(amount=100), (201, {"status": "accepted", "from_account": "11111111",
                                  "to_account": "22222222", "amount": 100,
                                  "currency": "GBP", "reference": ""})),
        ("broken JSON", '{"amount": 5,', (400, {"error": "invalid_json"})),
        ("empty string", "", (400, {"error": "invalid_json"})),
        ("JSON list not object", "[1, 2, 3]", (400, {"error": "invalid_body"})),
        ("JSON null", "null", (400, {"error": "invalid_body"})),
        ("missing from_account", body(from_account=REMOVE),
         (400, {"error": "missing_field", "field": "from_account"})),
        ("missing amount AND currency -> first one reported",
         body(amount=REMOVE, currency=REMOVE),
         (400, {"error": "missing_field", "field": "amount"})),
        ("account too short", body(to_account="1234"),
         (400, {"error": "invalid_field", "field": "to_account"})),
        ("account as number not string", body(from_account=11111111),
         (400, {"error": "invalid_field", "field": "from_account"})),
        ("account with letters", body(from_account="1111abcd"),
         (400, {"error": "invalid_field", "field": "from_account"})),
        ("amount as string", body(amount="25.50"),
         (400, {"error": "invalid_field", "field": "amount"})),
        ("amount zero", body(amount=0),
         (400, {"error": "invalid_field", "field": "amount"})),
        ("amount negative", body(amount=-5),
         (400, {"error": "invalid_field", "field": "amount"})),
        ("amount 3 decimal places", body(amount=10.555),
         (400, {"error": "invalid_field", "field": "amount"})),
        ("amount is a bool (trap)", body(amount=True),
         (400, {"error": "invalid_field", "field": "amount"})),
        ("amount is Infinity (trap)",
         '{"from_account":"11111111","to_account":"22222222",'
         '"amount":Infinity,"currency":"GBP"}',
         (400, {"error": "invalid_field", "field": "amount"})),
        ("wrong currency", body(currency="USD"),
         (400, {"error": "invalid_field", "field": "currency"})),
        ("reference too long", body(reference="x" * 19),
         (400, {"error": "invalid_field", "field": "reference"})),
        ("reference not a string", body(reference=123),
         (400, {"error": "invalid_field", "field": "reference"})),
        ("same account", body(to_account="11111111"),
         (400, {"error": "same_account"})),
    ]

    passed = 0
    for name, raw, expected in cases:
        try:
            got = handle_create_payment(raw)
            assert got == expected, f"expected {expected}, got {got}"
            print(f"PASS  {name}")
            passed += 1
        except Exception as e:
            print(f"FAIL  {name}  ({type(e).__name__}: {e})")
    print(f"\n{passed}/{len(cases)} passed")


if __name__ == "__main__":
    run_tests()