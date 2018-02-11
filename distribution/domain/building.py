from distribution.domain import Hive
from schematics.models import Model
from schematics.types import IntType, StringType
from schematics.types.compound import ModelType

class Building(Model):
	_id = IntType(required=True)
	address = StringType()
	xcoord = IntType()
	ycoord = IntType()
	hive = ModelType(Hive)