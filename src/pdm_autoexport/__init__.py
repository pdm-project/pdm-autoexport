from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pdm.core import Core


def main(core: Core):
    from pdm.signals import post_lock

    from pdm_autoexport.hook import run_auto_export

    post_lock.connect(run_auto_export)
