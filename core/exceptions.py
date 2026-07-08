"""
core/exceptions.py — Module 2: Core Engine
-------------------------------------------
Custom exceptions used by expense_engine.py, decorators.py and file_handler.py.

Note: these are separate from database/exception.py (Module 1), which covers
DB-level failures (UserNotFoundError, DuplicateEntryError, etc). These cover
logic-level failures that happen BEFORE data ever reaches the database —
bad input, missing auth, bad files.
"""


class CoreEngineError(Exception):
    """Base class for every exception raised inside the Core Engine (Module 2)."""
    pass


class ValidationError(CoreEngineError):
    """Raised by @validate_input when a rule fails (bad amount, missing field, etc.)."""
    pass


class AuthenticationError(CoreEngineError):
    """Raised by @require_auth when no user is currently logged in."""
    pass


class FileImportError(CoreEngineError):
    """Raised when a CSV import fails — bad path, bad format, unreadable rows."""
    pass


class FileExportError(CoreEngineError):
    """Raised when a CSV export fails — permission errors, bad path, disk issues."""
    pass


class StreamError(CoreEngineError):
    """Raised when something goes wrong mid-iteration inside a generator."""
    pass