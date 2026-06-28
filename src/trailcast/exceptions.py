from __future__ import annotations


class TrailcastError(Exception):
    """Base exception for all trailcast errors."""


class APIError(TrailcastError):
    """Raised when an external API call fails or returns an unexpected response."""


class InsufficientDataError(TrailcastError):
    """Raised when there is not enough data to produce a forecast."""
