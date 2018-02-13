from distribution.domain.hive import Hive
from distribution.domain.dronetype import Dronetype
from distribution.domain.status import Status
from schematics.models import Model
from schematics.types import IntType, StringType
from schematics.types.compound import ModelType

class Drone(Model):
	id = IntType(serialized_name='db/id')
	hive = ModelType(Hive, serialize_when_none=False, serialized_name='drone/hive')
	name = StringType(serialize_when_none=False, serialized_name='drone/name')
	type = ModelType(Dronetype, serialize_when_none=False, serialized_name='drone/type')
	status = ModelType(Status, serialize_when_none=False, serialized_name='drone/status')