from distribution.domain.stati import Stati
from schematics.models import Model
from schematics.types import IntType, StringType

class Status(Model):
	id = IntType()
	ident = StringType(choices = [
							Stati.idle.value,
							Stati.flying.value,
							Stati.charging.value ], serialize_when_none=False)