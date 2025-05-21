from tortoise import Model
from tortoise import fields

def create_dict_from_list(
    field_list: list, 
    default_value: str = fields.FloatField()
) -> dict:
    """
    Create a dictionary from a list of field names.
    
    Args:
        field_list (list): List of field names.
        default_value (str): Default value for each field in the dictionary.
        
    Returns:
        dict: Dictionary with field names as keys and default values as values.
    """
    return {field: default_value for field in field_list}



