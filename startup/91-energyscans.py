run_report(__file__)

import numpy as np
import bluesky.plans as bp
import bluesky.plan_stubs as bps
from cycler import cycler


def full_carbon_scan(multiple=1,mesh=IzeroMesh,det=sw_det,energy=en):
    '''
    Full Carbon Scan runs an RSoXS sample set through the carbon edge, with particular emphasis in he pre edge region

    this results in 128 exposures


    :param multiple: adjustment for exposure times
    :param mesh: which Izero channel to use
    :param det: which detector to use
    :param energy: what energy motor to scan
    :return: perform scan

    normal scan takes ~ 12 minutes to complete
    '''
    sample()
    if(len(read_input("Starting a Carbon energy scan hit any key in the next 3 seconds to abort", "abort", "", 3))>0):
        return

    energies = np.arange(270,282,.5)
    energies = np.append(energies,np.arange(282,286,.1))
    energies = np.append(energies,np.arange(286,292,.2))
    energies = np.append(energies,np.arange(292,305,1))
    energies = np.append(energies,np.arange(305,320,1))
    energies = np.append(energies,np.arange(320,350,5))
    times = energies.copy()
    times[energies<282] = 1
    times[(energies < 286) & (energies >= 282)] = 5
    times[energies >= 286] = 2
    times *= multiple
    times2 = times.copy()
    times3 = times.copy()
    sw_det.saxs.cam.acquire_time.kind = 'hinted'
    sw_det.waxs.cam.acquire_time.kind = 'hinted'
    mesh.parent.exposure_time.kind = 'hinted'

    yield from bp.scan_nd(
        [mesh,det,en],
        (cycler(sw_det.saxs.cam.acquire_time, times) +
        cycler(sw_det.waxs.cam.acquire_time, times2) +
        cycler(mesh.parent.exposure_time, times3) +
        cycler(energy, energies)))
