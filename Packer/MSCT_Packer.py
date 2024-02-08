import Musicreater
import Musicreater.experiment
import Musicreater.previous

import Musicreater.plugin

from Musicreater.plugin.addonpack import (
    to_addon_pack_in_delay,
    to_addon_pack_in_repeater,
    to_addon_pack_in_score,
)
from Musicreater.plugin.mcstructfile import (
    to_mcstructure_file_in_delay,
    to_mcstructure_file_in_repeater,
    to_mcstructure_file_in_score,
)

from Musicreater.plugin.bdxfile import to_BDX_file_in_delay, to_BDX_file_in_score

MSCT_MAIN = (
    Musicreater,
    Musicreater.experiment,
    Musicreater.previous,
)

MSCT_PLUGIN = (Musicreater.plugin,)

MSCT_PLUGIN_FUNCTION = (
    to_addon_pack_in_delay,
    to_addon_pack_in_repeater,
    to_addon_pack_in_score,
    to_mcstructure_file_in_delay,
    to_mcstructure_file_in_repeater,
    to_mcstructure_file_in_score,
    to_BDX_file_in_delay,
    to_BDX_file_in_score,
)

import hashlib

import dill
import brotli


def enpack_msct_pack(sth, to_dist: str):
    packing_bytes = brotli.compress(
        dill.dumps(
            sth,
        )
    )
    with open(
        to_dist,
        "wb",
    ) as f:
        f.write(packing_bytes)

    return hashlib.sha256(packing_bytes)


with open("./Packer/checksum.txt", "w", encoding="utf-8") as f:
    f.write("MSCT_MAIN:\n")
    f.write(enpack_msct_pack(MSCT_MAIN, "./Packer/MSCT_MAIN.MPK").hexdigest())
    f.write("\nMSCT_PLUGIN:\n")
    f.write(enpack_msct_pack(MSCT_PLUGIN, "./Packer/MSCT_PLUGIN.MPK").hexdigest())
    f.write("\nMSCT_PLUGIN_FUNCTION:\n")
    f.write(
        enpack_msct_pack(
            MSCT_PLUGIN_FUNCTION, "./Packer/MSCT_PLUGIN_FUNCTION.MPK"
        ).hexdigest()
    )
