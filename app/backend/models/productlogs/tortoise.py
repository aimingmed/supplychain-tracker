from enum import Enum

from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator
import random
import string


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


class ProductDetails(models.Model):    
    productid = fields.CharField(max_length=20, pk=True, description="产品号")
    category = fields.CharEnumField(Category)
    setsubcategory = fields.CharEnumField(SubCategory)
    productnameen = fields.CharField(max_length=100)
    productnamezh = fields.CharField(max_length=100)
    specification = fields.CharField(max_length=20, description="规格")
    unit = fields.CharEnumField(Unit, description="单位")
    components = fields.JSONField(default=list, description="包含组分")
    is_sold_independently = fields.BooleanField(default=True, description="是否独立销售")
    remarks_temperature = fields.CharField(max_length=100, description="标签温度标注")
    storage_temperature_duration = fields.CharField(max_length=100, description="储存温度&质保期")
    reorderlevel = fields.IntField()
    targetstocklevel = fields.IntField()
    leadtime = fields.IntField()

    def __str__(self):
        return self.productname

class ProductInventory(models.Model):
    batchid_internal = fields.CharField(max_length=70, unique=True, pk=True)
    batchid_external = fields.CharField(max_length=70)
    basicmediumid = fields.CharField(max_length=7)
    addictiveid = fields.CharField(max_length=7)
    quantityinstock = fields.IntField()
    productiondate = fields.DateField()
    imageurl = fields.TextField()
    status = fields.CharField(max_length=20)
    productiondatetime = fields.DatetimeField(description="生产时间")
    producedby = fields.CharField(max_length=50, description="生产人员")
    to_show = fields.BooleanField(default=True, description="是否展示")
    lastupdated = fields.DatetimeField(auto_now=True)
    lastupdatedby = fields.CharField(max_length=50)

    async def save(self, *args, **kwargs):
        # Set batchid_external as basicmediumid-addictiveid
        if not self.batchid_external:
            self.batchid_external = f"{self.basicmediumid}-{self.addictiveid}"
        if not self.batchid_internal:
            rand_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
            self.batchid_internal = f"{self.basicmediumid}-{self.addictiveid}-{rand_str}"
        await super().save(*args, **kwargs)

    def __str__(self):
        return f"BatchID: {self.batchid_external}, Product: {self.productname}"

    class Meta:
        table = "product_inventory"
        ordering = ["-lastupdated"]

ProductDetailsSchema = pydantic_model_creator(ProductDetails)
ProductInventorySchema = pydantic_model_creator(ProductInventory)
