from schematics.models import Model
from schematics.types import IntType

class Hopend(Model):
    id = IntType(required=True, serialized_name='db/id')