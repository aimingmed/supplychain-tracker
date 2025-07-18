"""
Tests for Pydantic schemas in productlog module.
"""
import pytest
from datetime import date, datetime
from pydantic import ValidationError

from models.productlog.pydantic import (
    ProductDetailsSchema,
    ProductInventoryCreateSchema,
    ProductInventorySchema,
    Category,
    SubCategory,
    Source,
    Unit,
    InventoryStatus
)


class TestProductDetailsSchema:
    """Test ProductDetailsSchema validation."""

    def test_valid_product_details_schema(self):
        """Test valid ProductDetailsSchema creation."""
        data = {
            "productid": "P12345",
            "category": "Organoid(类器官)",
            "setsubcategory": "Human Organoid(人源类器官)",
            "source": "Human(人源)",
            "productnameen": "Test Product EN",
            "productnamezh": "测试产品",
            "specification": "100ml",
            "unit": "Box(盒)",
            "components": ["P12345", "P12346"],
            "is_sold_independently": True,
            "remarks_temperature": "Store at -20°C",
            "storage_temperature_duration": "Store at -20°C for 6 months",
            "reorderlevel": 10,
            "targetstocklevel": 100,
            "leadtime": 5
        }
        
        schema = ProductDetailsSchema(**data)
        assert schema.productid == "P12345"
        assert schema.category == Category.ORGANOID
        assert schema.setsubcategory == SubCategory.HUMAN_ORGANOID
        assert schema.source == Source.HUMAN
        assert schema.unit == Unit.BOX

    def test_invalid_category(self):
        """Test ProductDetailsSchema with invalid category."""
        data = {
            "productid": "P12345",
            "category": "INVALID_CATEGORY",
            "setsubcategory": "Human Organoid(人源类器官)",
            "source": "Human(人源)",
            "productnameen": "Test Product EN",
            "productnamezh": "测试产品",
            "specification": "100ml",
            "unit": "Box(盒)",
            "reorderlevel": 10,
            "targetstocklevel": 100,
            "leadtime": 5
        }
        
        with pytest.raises(ValidationError) as exc_info:
            ProductDetailsSchema(**data)
        assert "category" in str(exc_info.value)

    def test_productid_too_long(self):
        """Test ProductDetailsSchema with productid too long."""
        data = {
            "productid": "P" * 25,  # Too long
            "category": "Organoid(类器官)",
            "setsubcategory": "Human Organoid(人源类器官)",
            "source": "Human(人源)",
            "productnameen": "Test Product EN",
            "productnamezh": "测试产品",
            "specification": "100ml",
            "unit": "Box(盒)",
            "reorderlevel": 10,
            "targetstocklevel": 100,
            "leadtime": 5
        }
        
        with pytest.raises(ValidationError) as exc_info:
            ProductDetailsSchema(**data)
        assert "productid" in str(exc_info.value)


class TestProductInventoryCreateSchema:
    """Test ProductInventoryCreateSchema validation."""

    def test_valid_product_inventory_create_schema(self):
        """Test valid ProductInventoryCreateSchema creation."""
        data = {
            "productid": "P12345",
            "basicmediumid": "BM001",
            "addictiveid": "AD001",
            "quantityinstock": 50,
            "productiondate": date.today(),
            "imageurl": "http://example.com/image.jpg",
            "status": "AVAILABLE(可用)",
            "productiondatetime": datetime.now(),
            "producedby": "John Doe",
            "coa_appearance": "Clear and colorless",
            "coa_clarity": True,
            "coa_osmoticpressure": 300.5,
            "coa_ph": 7.4,
            "coa__mycoplasma": False,
            "coa_sterility": True,
            "coa_fillingvolumedifference": True,
            "to_show": True,
            "lastupdatedby": "Jane Doe",
        }
        
        schema = ProductInventoryCreateSchema(**data)
        assert schema.productid == "P12345"
        assert schema.status == InventoryStatus.AVAILABLE
        assert schema.quantityinstock == 50

    def test_invalid_status(self):
        """Test ProductInventoryCreateSchema with invalid status."""
        data = {
            "productid": "P12345",
            "basicmediumid": "BM001",
            "addictiveid": "AD001",
            "quantityinstock": 50,
            "productiondate": date.today(),
            "imageurl": "http://example.com/image.jpg",
            "status": "INVALID_STATUS",
            "productiondatetime": datetime.now(),
            "producedby": "John Doe",
            "lastupdatedby": "Jane Doe",
        }
        
        with pytest.raises(ValidationError) as exc_info:
            ProductInventoryCreateSchema(**data)
        assert "status" in str(exc_info.value)

    def test_missing_required_field(self):
        """Test ProductInventoryCreateSchema with missing required field."""
        data = {
            "basicmediumid": "BM001",
            "addictiveid": "AD001",
            "quantityinstock": 50,
            "productiondate": date.today(),
            "imageurl": "http://example.com/image.jpg",
            "status": "AVAILABLE(可用)",
            "productiondatetime": datetime.now(),
            "producedby": "John Doe",
            "lastupdatedby": "Jane Doe",
        }
        
        with pytest.raises(ValidationError) as exc_info:
            ProductInventoryCreateSchema(**data)
        assert "productid" in str(exc_info.value)


class TestInventoryStatusEnum:
    """Test InventoryStatus enum values."""

    def test_all_status_values(self):
        """Test all InventoryStatus enum values."""
        assert InventoryStatus.AVAILABLE == "AVAILABLE(可用)"
        assert InventoryStatus.RESERVED == "RESERVED(预留)"
        assert InventoryStatus.IN_USE == "IN_USE(使用中)"
        assert InventoryStatus.EXPIRED == "EXPIRED(过期)"
        assert InventoryStatus.DAMAGED == "DAMAGED(损坏)"
        assert InventoryStatus.QUARANTINE == "QUARANTINE(隔离)"
        assert InventoryStatus.OUT_OF_STOCK == "OUT_OF_STOCK(缺货)"

    def test_status_enum_validation(self):
        """Test InventoryStatus enum validation in schema."""
        for status in InventoryStatus:
            data = {
                "productid": "P12345",
                "basicmediumid": "BM001",
                "addictiveid": "AD001",
                "quantityinstock": 50,
                "productiondate": date.today(),
                "imageurl": "http://example.com/image.jpg",
                "status": status.value,
                "productiondatetime": datetime.now(),
                "producedby": "John Doe",
                "lastupdatedby": "Jane Doe",
            }
            
            schema = ProductInventoryCreateSchema(**data)
            assert schema.status == status
