from django.db import models
import re

class LabelTypeField(models.TextField):
    def from_db_value(self, value, expression, connection):
        if value is None:
            return None
        """ parts = value.strip('()').split(',')
        return tuple(part.strip() for part in parts) """
        text = "".join(value)
        pattern = r'"([^"]*)"|([^",]+)|([{},()])'
        result = re.findall(pattern, text)
        result = [item for tuple_item in result for item in tuple_item if item]
        return text

    def to_python_value(self, value):
        if isinstance(value, tuple):
            return value
        if value is None:
            return None
        parts = value.strip('()').split(',')
        return tuple(part.strip() for part in parts)

    def get_prep_value(self, value):
        if value is None:
            return None
        return "(" + ",".join(str(v) for v in value) + ")"
    
    def db_type(self, connection):
        return 'label_type'