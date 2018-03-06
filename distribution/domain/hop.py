from distribution.domain.hopstart import Hopstart
from distribution.domain.hopend import Hopend
from schematics.models import Model
from schematics.types import IntType, StringType, FloatType
from schematics.types.compound import ModelType

class Hop(Model):
    id = IntType(required=True, serialized_name='db/id')
    start = ModelType(Hopstart, serialize_when_none=False, serialized_name='hop/start')
    end = ModelType(Hopend, serialize_when_none=False, serialized_name='hop/end')
    starttime = IntType(serialize_when_none=False, serialized_name='hop/starttime')
    endtime = IntType(serialize_when_none=False, serialized_name='hop/endtime')
    distance = FloatType(serialize_when_none=False, serialized_name='hop/distance')