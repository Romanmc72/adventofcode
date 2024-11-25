#!/usr/bin/env python3
"""
Description
-----------
A module for custom exceptions.
"""


class TimeIsUpException(Exception):
    """Thrown when an action is attempted but the timer is at zero."""

    pass


class AlreadyOpen(Exception):
    """Thrown if a valve is attempted to be opened but it is already open"""

    pass
