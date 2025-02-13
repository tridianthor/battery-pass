from labeling.models import Labeling

labeling = Labeling.objects.all()
print(labeling)

from labeling.models import Labeling
import uuid
from psycopg.types.composite import CompositeInfo, register_composite
import psycopg
import json

conn = psycopg.connect("dbname=battery_pass user=battery_admin password=battery_admin")
info = CompositeInfo.fetch(conn, "label_type")
register_composite(info, conn)
label = info.python_type("test", "test", "test")

labels = [info.python_type('Symbol 1', 'Meaning 1', 'Subject'),
    info.python_type('Symbol 2', 'Meaning 2', 'Subject 2')]


labeling = Labeling(uuid.uuid4(), "declaration", "result", labels)
labeling.save()