from schematics.models import Model
from schematics.types import IntType

class Hopstart(Model):
    id = IntType(required=True, serialized_name='db/id')