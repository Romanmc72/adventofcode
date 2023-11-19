#!/usr/bin/env python3
"""
Helper module for instantiating the logger
"""
import logging

logging.basicConfig()
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)
