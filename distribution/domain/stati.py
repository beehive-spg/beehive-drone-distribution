from enum import Enum

class Stati(Enum):
    idle = "drone.status/idle"
    flying = "drone.status/flying"
    charging = "drone.status/charging"
    order = "route.origin/order"
    distribution = "route.origin/distribution"