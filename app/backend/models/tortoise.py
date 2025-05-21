from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator


class TextSummary(models.Model):
    url = fields.TextField()
    summary = fields.TextField()
    created_at = fields.DatetimeField(auto_now_add=True)

    def __str__(self):
        return self.url
    

class ClinicalSampleProfile(models.Model):
    AccessionID = fields.CharField(max_length=13, pk=True)
    Code = fields.CharField(max_length=255)
    InternalID = fields.CharField(max_length=255, null=True)
    tumortype = fields.CharField(max_length=255)
    datatype = fields.CharField(max_length=255)
    sampletype = fields.CharField(max_length=255)
    costcenter = fields.CharField(max_length=2)

    def __str__(self):
        return self.AccessionID
    
    def __repr__(self):
        return "Clinical Sample Profile"


class MutationProfile(models.Model):
    AccessionID = fields.ForeignKeyField(
        'models.ClinicalSampleProfile',  # Foreign key to ClinicalSampleProfile model
        db_column='AccessionID',         # Explicitly specify the database column name (optional, but good practice)
        to_field='AccessionID',          # Specify the field in ClinicalSampleProfile to link to (primary key)
        related_name='mutation_profiles' # Optional: for reverse access from ClinicalSampleProfile
    )
    Chr = fields.CharField(max_length=25)
    Start = fields.IntField()
    End = fields.IntField()
    Ref = fields.TextField()
    Alt = fields.TextField()
    Func_refGene = fields.CharField(max_length=255, null=True)
    Gene_refGene = fields.CharField(max_length=255, null=True)
    GeneDetail_refGene = fields.TextField(null=True)
    ExonicFunc_refGene = fields.CharField(max_length=255, null=True)

    def __str__(self):
        return self.AccessionID
    
    def __repr__(self):
        return "Mutation Profile"
    
class DepMapCellLineProfile(models.Model):
    depmap_id = fields.CharField(max_length=10, pk=True)
    cell_line_display_name = fields.CharField(max_length=25)
    lineage_1 = fields.CharField(max_length=25)
    lineage_2 = fields.CharField(max_length=100)
    lineage_3 = fields.CharField(max_length=100)
    lineage_4 = fields.CharField(max_length=25)
    lineage_6 = fields.CharField(max_length=50)

    def __str__(self):
        return "DepMap CellLine Profile"


class DepMapDrugAUCPrismRepurposingSecondaryScreen(models.Model):
    depmap_id = fields.ForeignKeyField(
        'models.DepMapCellLineProfile',  # Foreign key to DepMapCellLineProfile model
        db_column='depmap_id',          # Explicitly specify the database column name (optional, but good practice)
        to_field='depmap_id',           # Specify the field in DepMapCellLineProfile to link to (primary key)
        related_name='drug_auc_prism_repurpose' # Optional: for reverse access from DepMapCellLineProfile
    )
    drug_name = fields.CharField(max_length=50, null=True)
    auc = fields.FloatField(null=True)
    
    def __str__(self):
        return str(self.depmap_id_id)  # Return the FK id value as string


class DepMapBatchCorrectedExpressionPublic24Q4(models.Model):
    depmap_id = fields.ForeignKeyField(
        'models.DepMapCellLineProfile',  # Foreign key to DepMapCellLineProfile model
        db_column='depmap_id',          # Explicitly specify the database column name (optional, but good practice)
        to_field='depmap_id',           # Specify the field in DepMapCellLineProfile to link to (primary key)
        related_name='batchcorrected_Expression_Public_24Q4' # Optional: for reverse access from DepMapCellLineProfile
    )
    gene_name = fields.CharField(max_length=50, null=True)
    expression_value = fields.FloatField(null=True)
    
    def __str__(self):
        return "DepMap Batch Corrected Expression Public 24Q4"

SummarySchema = pydantic_model_creator(TextSummary)
ClinicalSampleProfileSchema = pydantic_model_creator(ClinicalSampleProfile)
MutationProfileSchema = pydantic_model_creator(MutationProfile)
DepMapCellLineProfileSchema = pydantic_model_creator(DepMapCellLineProfile)
DepMapDrugAUCPrismRepurposingSecondaryScreenSchema = pydantic_model_creator(DepMapDrugAUCPrismRepurposingSecondaryScreen)
DepMapBatchCorrectedExpressionPublic24Q4Schema = pydantic_model_creator(DepMapBatchCorrectedExpressionPublic24Q4)
