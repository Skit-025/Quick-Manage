"""
core/decorators.py — Module 2: Core Engine
-------------------------------------------
Three decorators used everywhere from Module 2 onward:

    @validate_input(*rules)   validate arguments before a function runs
    @log_activity              log every call, its result, and how long it took
    @require_auth               block a call unless someone is logged in

A tiny in-memory "session" is included so @require_auth has something real to
check against before Module 4 wires up Flask sessions. Call login(user_id) once
you've verified credentials, logout() when done.
"""

import os
import sys
import time
import logging
from functools import wraps

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import APP_NAME
from core.exceptions import ValidationError, AuthenticationError

logger = logging.getLogger(APP_NAME)


# ── Minimal session store (placeholder until Flask sessions exist in Module 4) ──

_session = {"user_id": None}


def login(user_id: int) -> None:
    """Mark a user as logged in for the current process."""
    _session["user_id"] = user_id
    logger.info(f"User {user_id} logged in")


def logout() -> None:
    """Clear the current login state."""
    logger.info(f"User {_session.get('user_id')} logged out")
    _session["user_id"] = None


def current_user_id():
    """Return the id of the currently logged-in user, or None."""
    return _session.get("user_id")


# ── @validate_input ──────────────────────────────────────────────────────────

def validate_input(*rules):
    """
    Decorator factory. Pass any number of (predicate, message) pairs.

    Each predicate is called with the exact same *args/**kwargs the wrapped
    function receives, and must return True if the input is valid.

    Example:
        @validate_input(
            (lambda self, expense: expense.amount > 0, "Amount must be greater than 0"),
            (lambda self, expense: bool(expense.description_ or True), "Description invalid"),
        )
        def add_expense(self, expense):
            ...
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for predicate, message in rules:
                try:
                    ok = predicate(*args, **kwargs)
                except Exception as e:
                    raise ValidationError(f"Validation rule crashed: {e}")
                if not ok:
                    logger.warning(f"Validation failed for {func.__name__}: {message}")
                    raise ValidationError(message)
            return func(*args, **kwargs)
        return wrapper
    return decorator


# ── @log_activity ────────────────────────────────────────────────────────────

def log_activity(func):
    """Log function entry, exit, duration, and exceptions. Never logs passwords."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        safe_kwargs = {k: ("***" if "password" in k.lower() else v) for k, v in kwargs.items()}
        logger.info(f"CALL {func.__name__}({safe_kwargs})")
        start = time.perf_counter()
        try:
            result = func(*args, **kwargs)
        except Exception as e:
            elapsed = time.perf_counter() - start
            logger.error(f"FAIL {func.__name__} after {elapsed:.4f}s — {e}")
            raise
        elapsed = time.perf_counter() - start
        logger.info(f"DONE {func.__name__} in {elapsed:.4f}s")
        return result
    return wrapper


# ── @require_auth ────────────────────────────────────────────────────────────

def require_auth(func):
    """Block the call unless a user is currently logged in (see login() above)."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        if current_user_id() is None:
            logger.warning(f"Blocked unauthenticated call to {func.__name__}")
            raise AuthenticationError(f"{func.__name__} requires an authenticated user")
        return func(*args, **kwargs)
    return wrapper