from distribution.domain.hop import Hop
from distribution.domain.status import Status
from schematics.models import Model
from schematics.types import IntType, StringType, ListType
from schematics.types.compound import ModelType

class Route(Model):
    id = IntType(required=True, serialized_name='db/id')
    origin = ModelType(Status, serialized_name='route/origin')
    hoproute = ListType(ModelType(Hop), serialized_name='hop/_route')