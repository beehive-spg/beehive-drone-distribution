from distribution.domain import Hive, Status
from schematics.models import Model
from schematics.types import IntType, StringType
from schematics.types.compound import ModelType

class Drone(Model):
	id = IntType(required=True)
	hive = ModelType(Hive, serialize_when_none=False)
	name = StringType(serialize_when_none=False)
	type = ModelType(Type, serialize_when_none=False)
	status = StringType(choices = [
							Status.idle.value,
							Status.flying.value,
							Status.charging.value ], serialize_when_none=False)