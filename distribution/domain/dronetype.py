from schematics.models import Model
from schematics.types import IntType, StringType, BooleanType

class Dronetype(Model):
	id = IntType(required=True, serialized_name='db/id')
	name = StringType(serialize_when_none=False, serialized_name='dronetype/name')
	range = IntType(serialize_when_none=False, serialized_name='dronetype/range')
	speed = IntType(serialize_when_none=False, serialized_name='dronetype/speed')
	chargetime = IntType(serialize_when_none=False, serialized_name='dronetype/chargetime')
	default = BooleanType(serialize_when_none=False, serialized_name='dronetype/default')