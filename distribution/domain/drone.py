from distribution.domain.hive import Hive
from distribution.domain.type import Type
from distribution.domain.status import Status
from schematics.models import Model
from schematics.types import IntType, StringType
from schematics.types.compound import ModelType

class Drone(Model):
	id = IntType()
	hive = ModelType(Hive, serialize_when_none=False)
	name = StringType(serialize_when_none=False)
	type = ModelType(Type, serialize_when_none=False)
	status = ModelType(Status, serialize_when_none=False)