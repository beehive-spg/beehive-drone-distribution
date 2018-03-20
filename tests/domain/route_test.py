#!/usr/bin/env python3
import json
from pytest import fixture
from unittest.mock import patch
from distribution.domain.route import Route

@fixture
def json_route():
    return [{
        "db/id": 17592186045922,
        "route/origin": {
            "db/ident": "route.origin/order"
        },
        "hop/_route": [
            {
                "db/id": 17592186045924,
                "hop/start": {
                    "db/id": 17592186045498
                },
                "hop/end": {
                    "db/id": 17592186045779
                },
                "hop/starttime": 1520369612000,
                "hop/endtime": 1520369764588,
                "hop/distance": 2288.83
            },
            {
                "db/id": 17592186045925,
                "hop/start": {
                    "db/id": 17592186045779
                },
                "hop/end": {
                    "db/id": 17592186045486
                },
                "hop/starttime": 1520369767588,
                "hop/endtime": 1520369931546,
                "hop/distance": 2459.3813
            },
            {
                "db/id": 17592186045926,
                "hop/start": {
                    "db/id": 17592186045486
                },
                "hop/end": {
                    "db/id": 17592186045919
                },
                "hop/starttime": 1520369934546,
                "hop/endtime": 1520370114007,
                "hop/distance": 2691.916
            },
            {
                "db/id": 17592186045927,
                "hop/start": {
                    "db/id": 17592186045919
                },
                "hop/end": {
                    "db/id": 17592186045430
                },
                "hop/starttime": 1520370117007,
                "hop/endtime": 1520370136998,
                "hop/distance": 299.87103
            }
        ]
    }]

def test_route():
    route = Route(json_route()[0])
    assert route.to_primitive()['db/id'] == json_route()[0]['db/id']
    assert route.to_primitive()['route/origin'] == json_route()[0]['route/origin']
    assert route.to_primitive()['hop/_route'][0]['db/id'] == json_route()[0]['hop/_route'][0]['db/id']