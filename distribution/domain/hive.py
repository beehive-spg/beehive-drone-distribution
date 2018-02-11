from schematics.models import Model
from schematics.types import IntType, StringType

class Hive(Model):
	id = IntType(required=True)
	name = StringType()
	demand = IntType()
	free = IntType()