# models/__init__.py
# This file makes the models directory a Python package
# Import all models here so they can be imported easily from other modules

from .user import User
from .task import Task

__all__ = ['User', 'Task']
