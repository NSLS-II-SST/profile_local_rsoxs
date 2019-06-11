run_report(__file__)

import numpy as np
import bluesky.plans as bp
import bluesky.plan_stubs as bps
from cycler import cycler


def full_carbon_scan(multiple=1,sigs=[IzeroMesh],dets=[sw_det],energy=en):
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
    beamline_status()
    if len(read_input("Starting a Carbon energy scan hit any key in the next 3 seconds to abort", "abort", "", 3)) > 0:
        return

    # create a list of energies
    energies = np.arange(270,282,.5)
    energies = np.append(energies,np.arange(282,286,.1))
    energies = np.append(energies,np.arange(286,292,.2))
    energies = np.append(energies,np.arange(292,305,1))
    energies = np.append(energies,np.arange(305,320,1))
    energies = np.append(energies,np.arange(320,350,5))
    times = energies.copy()

    # Define exposures times for different energy ranges
    times[energies<282] = 1
    times[(energies < 286) & (energies >= 282)] = 5
    times[energies >= 286] = 2
    times *= multiple

    # use these energies and exposure times to scan energy and record detectors and signals
    yield from en_scan_core(sigs, dets,energy,energies,times)


def en_scan_core(I400sigs, dets, energy, energies, times):
    sw_det.saxs.cam.acquire_time.kind = 'hinted'
    sw_det.waxs.cam.acquire_time.kind = 'hinted'
    sigcycler = cycler(energy, energies)
    for i400channel in I400sigs:
        i400channel.parent.exposure_time.kind = 'hinted'
        try:
            sigcycler += cycler(i400channel.parent.exposure_time,times.copy())
        except ValueError:
            print('same i400 detected')
            i400channel.kind = 'hinted'
    sigcycler += cycler(sw_det.saxs.cam.acquire_time, times.copy())
    sigcycler += cycler(sw_det.waxs.cam.acquire_time, times.copy())
    light_was_on = False
    if light.value is 1:
        light.off()
        light_was_on = True
        boxed_text('Warning', 'light was on, taking a quick snapshot to clear CCDs', 'yellow', shrink=True)
        yield from quicksnap()

    yield from bp.scan_nd(I400sigs+ dets+ [en],sigcycler)

    if light_was_on:
        light.on()

