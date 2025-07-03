from models.productrequests.tortoise import RequestDetails
import re

# Test __str__ for RequestDetails
def test_requestdetails_str():
    obj = RequestDetails()
    # The __str__ returns self.id, which is not set by default
    obj.id = "REQID123"
    assert str(obj) == "REQID123"


# Test generate_requestid static method
def test_generate_requestid_format(monkeypatch):
    # Patch datetime and uuid to fixed values
    class DummyDatetime:
        @staticmethod
        def utcnow():
            class Dummy:
                def strftime(self, fmt):
                    return "20250703123456"
            return Dummy()
    monkeypatch.setattr("models.productrequests.tortoise.datetime", DummyDatetime)
    monkeypatch.setattr("models.productrequests.tortoise.uuid", type("DummyUUID", (), {"uuid4": staticmethod(lambda: type('U', (), {"hex": "abcdef1234567890"})())}))
    rid = RequestDetails.generate_requestid()
    # Should match the format: 14 digits + 6 hex chars
    assert re.match(r"^20250703123456abcdef$", rid)

# Test pydantic RequestDetailsSchema fields (from pydantic.py)
from models.productrequests.pydantic import RequestDetailsSchema
def test_requestdetails_schema_fields():
    schema = RequestDetailsSchema.__fields__
    for field in [
        "requestid", "requestorname", "requestdate", "requestproductid", "requestunit",
        "is_urgent", "remarks", "status", "fullfillername", "fullfilldate"
    ]:
        assert field in schema
