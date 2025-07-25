from datetime import datetime, date
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field, validator


class Category(str, Enum):
    ORGANOID = "Organoid(类器官)"
    CONSUMABLE = "Consumable(耗材)"
    EQUIPMENT = "Equipment(设备)"
    REAGENT = "Reagent(试剂)"


class SubCategory(str, Enum):
    HUMAN_ORGANOID = "Human Organoid(人源类器官)"
    MOUSE_ORGANOID = "Mouse Organoid(小鼠类器官)"
    OTHER_AUXILIARY_REAGENTS = "Other Auxiliary Reagents(其他辅助试剂)"
    CRYOTUBES = "Cryotubes(冷冻管)"
    MATRIGEL = "Matrigel(基质胶)"
    LARGE_EQUIPMENT = "Large Equipment(大型设备)"
    PRIMERS = "Primers(引物)"
    CENTRIFUGE_TUBE = "Centrifuge Tube(离心管)"
    PIPETTE_TIPS = "Pipette Tips(移液枪吸头)"
    PIPETTE = "Pipette(移液枪)"
    ORGANOID_DIFFERENTIATION_MEDIUM = "Organoid Differentiation Medium(类器官分化培养基)"
    ORGANOID_CULTURE_KIT = "Organoid Culture Kit(类器官培养套件)"
    ORGANOID_BASAL_MEDIUM = "Organoid Basal Medium(类器官基础培养基)"
    COMPLETE_ORGANOID_CULTURE_MEDIUM = "Complete Organoid Culture Medium(类器官完全培养基)"
    ORGANOID_CONDITIONED_MEDIUM = "Organoid Conditioned Medium(类器官条件培养基)"
    CELL_CULTURE_PLATE = "Cell Culture Plate(细胞培养板)"
    CELL_CULTURE_FLASK = "Cell Culture Flask(细胞培养瓶)"
    CELL_CULTURE_DISH = "Cell Culture Dish(细胞培养皿)"
    CELL_CULTURE_REAGENTS = "Cell Culture Reagents(细胞培养试剂)"
    CELL_SHAKE_FLASK = "Cell Shake Flask(细胞摇瓶)"
    CELL_COUNTING_PLATE = "Cell Counting Plate(细胞计数板)"
    CHIP = "Chip(芯片)"
    SERUM = "Serum(血清)"


class Source(str, Enum):
    HUMAN = "Human(人源)"
    MOUSE = "Mouse(鼠源)"
    HESC = "hESC(人胚胎干细胞)"
    HPSC = "hPSC(人诱导多能干细胞)"


class Unit(str, Enum):
    BOX = "Box(盒)"
    PACKET = "Packet(包)"
    BOTTLE = "Bottle(瓶)"
    UNIT = "Unit(台)"
    TUBE = "Tube(支)"
    BIGBOX = "Big Box(箱)"


class InventoryStatus(str, Enum):
    AVAILABLE = "AVAILABLE(可用)"
    RESERVED = "RESERVED(预留)"
    IN_USE = "IN_USE(使用中)"
    EXPIRED = "EXPIRED(过期)"
    DAMAGED = "DAMAGED(损坏)"
    QUARANTINE = "QUARANTINE(隔离)"
    OUT_OF_STOCK = "OUT_OF_STOCK(缺货)"


class ProductDetailsSchema(BaseModel):
    productid: str = Field(
        ..., min_length=1, max_length=20, description="产品号，唯一标识", example="P12345"
    )
    category: Category = Field(..., description="产品类别", example=Category.ORGANOID)
    setsubcategory: SubCategory = Field(
        ..., description="产品子类别", example=SubCategory.HUMAN_ORGANOID
    )
    source: Source = Field(..., description="产品来源", example=Source.HUMAN)
    productnameen: str = Field(..., example="Product Name EN")
    productnamezh: str = Field(..., example="产品名称")
    specification: str = Field(..., example="Specification")
    unit: Unit = Field(..., description="单位", example=Unit.BOX)
    components: List[str] = Field(
        default_factory=list, description="包含组分", example=["P12345", "P12346"]
    )
    is_sold_independently: bool = Field(True, description="是否独立销售", example=True)
    remarks_temperature: Optional[str] = Field(
        None, description="标签温度标注", example="Store at -20°C"
    )
    storage_temperature_duration: Optional[str] = Field(
        None, description="储存温度&质保期", example="Store at -20°C for 6 months"
    )
    reorderlevel: int = Field(..., example=10, description="补货水平")
    targetstocklevel: int = Field(..., example=100, description="目标库存水平")
    leadtime: int = Field(..., example=5, description="交货时间（天）")


class ProductInventoryCreateSchema(BaseModel):
    """Schema for creating ProductInventory - excludes auto-generated fields"""
    productid: str = Field(..., max_length=20, description="产品号，必须存在于产品详情中")
    basicmediumid: str = Field(..., max_length=7)
    addictiveid: str = Field(..., max_length=7)
    quantityinstock: int = Field(...)
    productiondate: date = Field(...)
    imageurl: Optional[str] = Field(None, description="图片URL")
    status: InventoryStatus = Field(..., description="库存状态", example=InventoryStatus.AVAILABLE)
    productiondatetime: datetime = Field(..., description="生产时间")
    producedby: str = Field(..., max_length=50, description="生产人员")
    coa_appearance: Optional[str] = Field(None, max_length=100, description="外观描述")
    coa_clarity: Optional[bool] = Field(None, description="透明度")
    coa_osmoticpressure: Optional[float] = Field(None, description="渗透压")
    coa_ph: Optional[float] = Field(None, description="pH值")
    coa__mycoplasma: Optional[bool] = Field(None, description="支原体检测")
    coa_sterility: Optional[bool] = Field(None, description="无菌检测")
    coa_fillingvolumedifference: Optional[bool] = Field(None, description="装量差异限度")
    to_show: bool = Field(default=True, description="是否展示")
    lastupdatedby: str = Field(..., max_length=50)

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "productid": "P12345",
                "basicmediumid": "BM001",
                "addictiveid": "AD001",
                "quantityinstock": 50,
                "productiondate": "2025-01-01",
                "status": "AVAILABLE(可用)",
                "productiondatetime": "2025-01-01T12:00:00",
                "producedby": "John Doe",
                "to_show": True,
                "lastupdatedby": "Jane Doe",
                # Optional fields
                "imageurl": "http://example.com/image.jpg",
                "coa_appearance": "Clear and colorless",
                "coa_clarity": True,
                "coa_osmoticpressure": 300.5,
                "coa_ph": 7.4,
                "coa__mycoplasma": False,
                "coa_sterility": True,
                "coa_fillingvolumedifference": True,
            }
        }


class ProductInventorySchema(BaseModel):
    """Schema for ProductInventory - includes all fields for read operations"""
    batchid_internal: Optional[str] = Field(None, max_length=70, description="内部批次号（自动生成）")
    batchid_external: Optional[str] = Field(None, max_length=70, description="外部批次号（自动生成）")
    productid: str = Field(..., max_length=20, description="产品号")
    basicmediumid: str = Field(..., max_length=7)
    addictiveid: str = Field(..., max_length=7)
    quantityinstock: int = Field(...)
    productiondate: date = Field(...)
    imageurl: Optional[str] = Field(None, description="图片URL")
    status: InventoryStatus = Field(..., description="库存状态")
    productiondatetime: datetime = Field(..., description="生产时间")
    producedby: str = Field(..., max_length=50, description="生产人员")
    coa_appearance: Optional[str] = Field(None, max_length=100, description="外观描述")
    coa_clarity: Optional[bool] = Field(None, description="透明度")
    coa_osmoticpressure: Optional[float] = Field(None, description="渗透压")
    coa_ph: Optional[float] = Field(None, description="pH值")
    coa__mycoplasma: Optional[bool] = Field(None, description="支原体检测")
    coa_sterility: Optional[bool] = Field(None, description="无菌检测")
    coa_fillingvolumedifference: Optional[bool] = Field(None, description="装量差异限度")
    to_show: bool = Field(default=True, description="是否展示")
    lastupdated: datetime = Field(...)
    lastupdatedby: str = Field(..., max_length=50)

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "productid": "P12345",
                "basicmediumid": "BM001",
                "addictiveid": "AD001",
                "quantityinstock": 50,
                "productiondate": "2025-01-01",
                "imageurl": "http://example.com/image.jpg",
                "status": "AVAILABLE(可用)",
                "productiondatetime": "2025-01-01T12:00:00",
                "producedby": "John Doe",
                "coa_appearance": "Clear and colorless",
                "coa_clarity": True,
                "coa_osmoticpressure": 300.5,
                "coa_ph": 7.4,
                "coa__mycoplasma": False,
                "coa_sterility": True,
                "coa_fillingvolumedifference": True,
                "to_show": True,
                "lastupdated": "2025-01-02T12:00:00",
                "lastupdatedby": "Jane Doe",
            }
        }


class ProductInventoryWithDetailsSchema(BaseModel):
    """Combined schema that includes both product details and inventory information"""
    # From ProductDetails
    productid: str = Field(..., max_length=20, description="产品号")
    category: Category = Field(..., description="产品类别")
    setsubcategory: SubCategory = Field(..., description="产品子类别")
    source: Source = Field(..., description="产品来源")
    productnameen: str = Field(..., max_length=100, description="产品名称(英文)")
    productnamezh: str = Field(..., max_length=100, description="产品名称(中文)")
    specification: str = Field(..., max_length=20, description="规格")
    unit: Unit = Field(..., description="单位")
    components: List[str] = Field(default=[], description="包含组分")
    is_sold_independently: bool = Field(default=True, description="是否独立销售")
    remarks_temperature: Optional[str] = Field(None, max_length=100, description="标签温度标注")
    storage_temperature_duration: Optional[str] = Field(None, max_length=100, description="储存温度&质保期")
    reorderlevel: int = Field(..., description="补货水平")
    targetstocklevel: int = Field(..., description="目标库存水平")
    leadtime: int = Field(..., description="交货时间（天）")
    
    # From ProductInventory
    batchid_internal: str = Field(..., max_length=70, description="内部批次号")
    batchid_external: str = Field(..., max_length=70, description="外部批次号")
    basicmediumid: str = Field(..., max_length=7, description="基础培养基ID")
    addictiveid: str = Field(..., max_length=7, description="添加剂ID")
    quantityinstock: int = Field(..., description="库存数量")
    productiondate: date = Field(..., description="生产日期")
    imageurl: Optional[str] = Field(None, description="图片URL")
    status: InventoryStatus = Field(..., description="库存状态")
    productiondatetime: datetime = Field(..., description="生产时间")
    producedby: str = Field(..., max_length=50, description="生产人员")
    coa_appearance: Optional[str] = Field(None, max_length=100, description="外观描述")
    coa_clarity: Optional[bool] = Field(None, description="透明度")
    coa_osmoticpressure: Optional[float] = Field(None, description="渗透压")
    coa_ph: Optional[float] = Field(None, description="pH值")
    coa__mycoplasma: Optional[bool] = Field(None, description="支原体检测")
    coa_sterility: Optional[bool] = Field(None, description="无菌检测")
    coa_fillingvolumedifference: Optional[bool] = Field(None, description="装量差异限度")
    to_show: bool = Field(default=True, description="是否展示")
    lastupdated: datetime = Field(..., description="最后更新时间")
    lastupdatedby: str = Field(..., max_length=50, description="最后更新人")

    class Config:
        orm_mode = True
