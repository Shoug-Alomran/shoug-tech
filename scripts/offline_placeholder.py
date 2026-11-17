"""Detect cloud-sync placeholders (files whose bytes are not on this machine).

Shared by the site build and validators so they skip online-only files the same
way on every OS: POSIX reports them with zero allocated blocks; Windows has no
st_blocks, so OneDrive's online-only file attributes are checked instead.
"""
from __future__ import annotations

import os

# FILE_ATTRIBUTE_RECALL_ON_DATA_ACCESS | FILE_ATTRIBUTE_OFFLINE
_WINDOWS_ONLINE_ONLY = 0x400000 | 0x1000


def is_offline_placeholder(stat: os.stat_result) -> bool:
    blocks = getattr(stat, "st_blocks", None)
    if blocks is not None:
        return blocks == 0
    return bool(getattr(stat, "st_file_attributes", 0) & _WINDOWS_ONLINE_ONLY)
