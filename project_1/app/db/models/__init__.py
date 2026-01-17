# app/db/models/__init__.py

# Import all models here so Base.metadata sees them
from .user import User
from .resource import Resource
from .reservation import Reservation
# This file makes it easier to import models elsewhere