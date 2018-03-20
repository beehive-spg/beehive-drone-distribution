#!/usr/bin/env python3
from unittest.mock import patch
from distribution.domain.point import Point

def test_shift_and_repr():
	point = Point(10, 10)
	point.shift(10, 10)
	rep = point.__repr__()
	assert point.x == 20
	assert point.y == 20
	assert rep == "Point("+ str(point.x) +","+ str(point.y) +")"
