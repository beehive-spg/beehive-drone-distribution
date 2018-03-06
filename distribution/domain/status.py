from distribution.domain.stati import Stati
from schematics.models import Model
from schematics.types import IntType, StringType

class Status(Model):
    id = IntType(serialize_when_none=False, serialized_name='db/id')
    ident = StringType(choices = [
                            Stati.idle.value,
                            Stati.flying.value,
                            Stati.charging.value,
                            Stati.order.value ], serialize_when_none=False, serialized_name='db/ident')