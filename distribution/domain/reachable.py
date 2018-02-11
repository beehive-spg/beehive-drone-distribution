#!/usr/bin/env python3
from distribution.domain.building import Building
from schematics.models import Model
from schematics.types import IntType, StringType
from schematics.types.compound import ModelType

class Reachable(Model):
	id = IntType(required=True)
	start = ModelType(Building, serialize_when_none=False)
	end = ModelType(Building, serialize_when_none=False)
	distance = IntType(serialize_when_none=False)