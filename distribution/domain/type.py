from schematics.models import Model
from schematics.types import IntType, StringType, BooleanType

class Type(Model):
	id = IntType(required=True)
	name = StringType(serialize_when_none=False)
	range = IntType(serialize_when_none=False)
	speed = IntType(serialize_when_none=False)
	chargetime = IntType(serialize_when_none=False)
	default = BooleanType(serialize_when_none=False)