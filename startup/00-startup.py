import sys
from pathlib import Path

paths = [
    path
    for path in Path(
        "/nsls2/data/sst/rsoxs/shared/config/bluesky/collection_packages"
    ).glob("*")
    if path.is_dir()
]
for path in paths:
    sys.path.append(str(path))


from sst_funcs.printing import run_report

run_report(__file__)

# sst devices  These all reference the Base classes and instantiate the objects themselves into the current namespace
#from sst_hw.gatevalves import *
#from sst_hw.shutters import *
#from sst_hw.vacuum import *
#from sst_hw.motors import *
#from sst_hw.mirrors import *
#from sst_hw.diode import *
#from sst_hw.energy import *

# sst code  # Common code
from sst_base.archiver import *

# RSoXS startup - bluesky RE / db / md definitions
from rsoxs.startup import *

# RSoXS specific devices
from rsoxs.HW.motors import sam_viewer
from rsoxs.HW.cameras import *
from rsoxs.HW.signals import *
#from rsoxs.HW.detectors import *
#from rsoxs.HW.slits import *
#from rsoxs.HW.syringepump import *
#from rsoxs.HW.energy import *
#from rsoxs.HW.lakeshore import *

# RSoXS specific code
#from rsoxs.Functions.alignment import image_bar,list_samples,locate_samples_from_image,clear_bar,resolve_spirals
from rsoxs.Functions.alignment_local import *
#from rsoxs.Functions.common_procedures import *
#from rsoxs.Functions.configurations import *
from rsoxs.Functions.schemas import *
#from rsoxs.Functions.PVdictionary import *
#from rsoxs.Functions.energyscancore import *
from rsoxs.Functions.spreadsheets import load_sheet, save_sheet
#from rsoxs.Functions.fly_alignment import *
from rsoxs.HW.slackbot import rsoxs_bot
from rsoxs_scans.spreadsheets import *
from rsoxs_scans.acquisition import *


try:
    from bluesky_queueserver import is_re_worker_active
except ImportError:
    # TODO: delete this when 'bluesky_queueserver' is distributed as part of collection environment
    def is_re_worker_active():
        return False


#if not is_re_worker_active():
#    from rsoxs.Functions.magics import *
#
#    beamline_status()  # print out the current sample metadata, motor position and detector status


# from .Functions.startup import sd
