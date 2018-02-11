from enum import Enum

class Status(Enum):
	"""
	GET methods use Status.status.name
	POST methods use Status.status.value
	"""
	idle = "drone.status/idle"
	flying = "drone.status/flying"
	charging = "drone.status/charging"