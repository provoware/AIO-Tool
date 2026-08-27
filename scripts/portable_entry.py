#!/usr/bin/env python3
"""PyInstaller entry point for the self-contained Linux runtime.

The portable bootstrap deliberately repairs *copied permission bits* only inside
its newly created user mirror. This matters when the source package itself was
chmod'ed read-only: shutil.copytree would otherwise preserve those permissions
and the mirror could become read-only again.
"""
from __future__ import annotations

import stat
from pathlib import Path

import app.autostart as autostart

_ORIGINAL_COPYTREE = autostart.shutil.copytree


def _make_user_copy_writable(root: Path) -> None:
    paths = [root, *root.rglob("*")]
    for path in paths:
        try:
            mode = stat.S_IMODE(path.stat().st_mode)
            if path.is_dir():
                path.chmod(mode | stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR)
            else:
                path.chmod(mode | stat.S_IRUSR | stat.S_IWUSR)
        except OSError:
            # The following real write probe in app.autostart remains the
            # authoritative gate; a permission that cannot be changed must not
            # be hidden here.
            pass


def _copytree_into_writable_user_mirror(src, dst, *args, **kwargs):
    result = _ORIGINAL_COPYTREE(src, dst, *args, **kwargs)
    _make_user_copy_writable(Path(dst))
    return result


autostart.shutil.copytree = _copytree_into_writable_user_mirror
main = autostart.main

if __name__ == "__main__":
    raise SystemExit(main())
