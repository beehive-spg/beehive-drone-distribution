from distribution.domain import Hive, Status
from schematics.models import Model
from schematics.types import IntType, StringType
from schematics.types.compound import ModelType

class Drone(Model):
	_id = IntType(required=True)
	hive = ModelType(Hive)
	name = StringType()
	_type = ModelType(Type)
	status = StringType(choices = [
							Status.idle.value,
							Status.flying.value,
							Status.charging.value ])