import pytest
import random
import tortoise.models
from models.productlog.tortoise import ProductDetails, ProductInventory


# Test __str__ for ProductDetails
@pytest.mark.asyncio
async def test_productdetails_str():
    obj = ProductDetails()
    obj.productname = "Test Product"
    assert str(obj) == "Test Product"


# Test __str__ for ProductInventory
@pytest.mark.asyncio
async def test_productinventory_str():
    obj = ProductInventory()
    obj.batchid_external = "BATCH123"
    obj.productname = "Test Product"
    assert str(obj) == "BatchID: BATCH123, Product: Test Product"


# Test save logic for ProductInventory
@pytest.mark.asyncio
async def test_productinventory_save_sets_batchids(monkeypatch):
    obj = ProductInventory()
    obj.basicmediumid = "BMID"
    obj.addictiveid = "AID"
    obj.batchid_external = ""
    obj.batchid_internal = ""
    # Patch parent Model.save to a dummy async function
    async def dummy_save(self, *args, **kwargs):
        return None

    monkeypatch.setattr(tortoise.models.Model, "save", dummy_save)
    # Patch random.choices to return a fixed string
    monkeypatch.setattr(random, "choices", lambda *a, **k: list("ABC123"))
    await obj.save()
    assert obj.batchid_external == "BMID-AID"
    assert obj.batchid_internal == "BMID-AID-ABC123"
