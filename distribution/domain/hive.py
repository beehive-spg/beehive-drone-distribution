from schematics.models import Model
from schematics.types import IntType, StringType

class Hive(Model):
	id = IntType(required=True)
	name = StringType(serialize_when_none=False)
	demand = IntType(serialize_when_none=False)
	free = IntType(serialize_when_none=False)