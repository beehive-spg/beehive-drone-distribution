from schematics.models import Model
from schematics.types import IntType, StringType

class Hive(Model):
	id = IntType(required=True, serialized_name='db/id')
	name = StringType(serialize_when_none=False, serialized_name='hive/name')
	demand = IntType(serialize_when_none=False, serialized_name='hive/demand')
	free = IntType(serialize_when_none=False, serialized_name='hive/free')
	incoming = IntType(serialize_when_none=False, serialized_name='hive/incoming')
	outgoing = IntType(serialize_when_none=False, serialized_name='hive/outgoing')