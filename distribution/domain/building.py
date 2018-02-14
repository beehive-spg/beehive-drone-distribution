from distribution.domain.hive import Hive
from schematics.models import Model
from schematics.types import IntType, StringType
from schematics.types.compound import ModelType

class Building(Model):
	id = IntType(required=True, serialized_name='db/id')
	address = StringType(serialize_when_none=False, serialized_name='building/address')
	xcoord = IntType(serialize_when_none=False, serialized_name='building/xcoord')
	ycoord = IntType(serialize_when_none=False, serialized_name='building/ycoord')
	hive = ModelType(Hive, serialize_when_none=False, serialized_name='building/hive')