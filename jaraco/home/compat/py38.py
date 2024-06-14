import sys


if sys.version_info < (3, 9):
    import importlib_resources as resources
else:
    from importlib import resources  # noqa: F401
