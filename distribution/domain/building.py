from distribution.domain import Hive
from schematics.models import Model
from schematics.types import IntType, StringType
from schematics.types.compound import ModelType

class Building(Model):
	id = IntType(required=True)
	address = StringType(serialize_when_none=False)
	xcoord = IntType(serialize_when_none=False)
	ycoord = IntType(serialize_when_none=False)
	hive = ModelType(Hive, serialize_when_none=False)