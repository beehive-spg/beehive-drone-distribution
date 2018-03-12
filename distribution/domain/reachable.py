#!/usr/bin/env python3
from distribution.domain.building import Building
from schematics.models import Model
from schematics.types import IntType, StringType, FloatType
from schematics.types.compound import ModelType

class Reachable(Model):
	id = IntType(required=True, serialized_name='db/id')
	start = ModelType(Building, serialize_when_none=False, serialized_name='connection/start')
	end = ModelType(Building, serialize_when_none=False, serialized_name='connection/end')
	distance = FloatType(serialize_when_none=False, serialized_name='connection/distance')