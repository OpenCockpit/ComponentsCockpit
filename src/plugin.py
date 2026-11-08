# Copyright (C) 2018-2026 by xcentaurix
# License: GNU General Public License v3.0


from .Debug import logger
from .Version import VERSION


def Plugins(**__):
    logger.info("  +++ Version: %s starts...", VERSION)
    return []
