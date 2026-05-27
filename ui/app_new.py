"""Compatibility shim — delegates to the new UI tree under `ui_new/`.

The `--new` flag in `main.py` imports this module, which keeps the call site
unchanged while the rewritten UI lives in its own clean package.
"""

from ui_new.app import launch  # noqa: F401
