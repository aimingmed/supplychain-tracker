import random
import string

from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator


class ProductDetails(models.Model):
    productid = fields.CharField(max_length=20, pk=True)
    category = fields.CharField(max_length=20, description="产品类别")
    setsubcategory = fields.CharField(max_length=50, description="产品子类别")
    source = fields.CharField(max_length=20, description="产品来源")
    productnameen = fields.CharField(max_length=100)
    productnamezh = fields.CharField(max_length=100)
    specification = fields.CharField(max_length=20, description="规格")
    unit = fields.CharField(max_length=20, description="单位")
    components = fields.JSONField(default=list, description="包含组分")
    is_sold_independently = fields.BooleanField(default=True, description="是否独立销售")
    remarks_temperature = fields.CharField(max_length=100, description="标签温度标注")
    storage_temperature_duration = fields.CharField(
        max_length=100, description="储存温度&质保期"
    )
    reorderlevel = fields.IntField()
    targetstocklevel = fields.IntField()
    leadtime = fields.IntField()

    def __str__(self):
        return self.productnameen


class ProductInventory(models.Model):
    batchid_internal = fields.CharField(max_length=70, unique=True, pk=True)
    batchid_external = fields.CharField(max_length=70)
    productid = fields.CharField(max_length=20, description="产品号，必须存在于产品详情中")
    basicmediumid = fields.CharField(max_length=7)
    addictiveid = fields.CharField(max_length=7)
    quantityinstock = fields.IntField()
    productiondate = fields.DateField()
    imageurl = fields.TextField(null=True)
    status = fields.CharField(max_length=20)
    productiondatetime = fields.DatetimeField(description="生产时间")
    producedby = fields.CharField(max_length=50, description="生产人员")
    coa_appearance = fields.CharField(max_length=100, description="外观描述", null=True)
    coa_clarity = fields.BooleanField(description="透明度", null=True)
    coa_osmoticpressure = fields.FloatField(description="渗透压", null=True)
    coa_ph = fields.FloatField(description="pH值", null=True)
    coa__mycoplasma = fields.BooleanField(description="支原体检测", null=True)
    coa_sterility = fields.BooleanField(description="无菌检测", null=True)
    coa_fillingvolumedifference = fields.BooleanField(description="装量差异限度", null=True)
    to_show = fields.BooleanField(default=True, description="是否展示")
    lastupdated = fields.DatetimeField(auto_now=True)
    lastupdatedby = fields.CharField(max_length=50)

    async def save(self, *args, **kwargs):
        # Set batchid_external as basicmediumid-addictiveid
        if not self.batchid_external:
            self.batchid_external = f"{self.basicmediumid}-{self.addictiveid}"
        if not self.batchid_internal:
            rand_str = "".join(
                random.choices(string.ascii_uppercase + string.digits, k=6)
            )
            self.batchid_internal = (
                f"{self.basicmediumid}-{self.addictiveid}-{rand_str}"
            )
        await super().save(*args, **kwargs)

    def __str__(self):
        return f"BatchID: {self.batchid_external}, BasicMedium: {self.basicmediumid}, Additive: {self.addictiveid}"

    class Meta:
        table = "product_inventory"
        ordering = ["-lastupdated"]


ProductDetailsSchema = pydantic_model_creator(ProductDetails)
ProductInventorySchema = pydantic_model_creator(ProductInventory)
