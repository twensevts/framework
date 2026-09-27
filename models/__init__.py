"""Объектная модель системы коллекционирования комиксов."""

from .users import User
from .series import Series
from .issues import Issue
from .collections import Collection

__all__ = ["Collection", "Issue", "Series", "User"]
