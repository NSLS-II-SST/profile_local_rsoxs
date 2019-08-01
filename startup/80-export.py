run_report(__file__)
from pathlib import Path

"""
Example:
--------

In [20]: tiff_series.export(db[-3].documents(fill=True), file_prefix='{start[institution]}-Eph={event[data][energy]}-{s
    ...: tart[scan_id]}-', directory=f'Z:/images/users/{hdr.start["user"]}')
Out[20]:
{'stream_data': [WindowsPath('//XF07ID1-WS17/RSoXS Documents/images/users/Eliot/NIST-Eph=459.987181-40-primary-sw_det_saxs_image-0.tiff'),
  WindowsPath('//XF07ID1-WS17/RSoXS Documents/images/users/Eliot/NIST-Eph=459.987181-40-primary-sw_det_waxs_image-0.tiff'),
  WindowsPath('//XF07ID1-WS17/RSoXS Documents/images/users/Eliot/NIST-Eph=459.9903474-40-primary-sw_det_saxs_image-1.tiff'),
  WindowsPath('//XF07ID1-WS17/RSoXS Documents/images/users/Eliot/NIST-Eph=459.9903474-40-primary-sw_det_waxs_image-1.tiff'),
  WindowsPath('//XF07ID1-WS17/RSoXS Documents/images/users/Eliot/NIST-Eph=460.0084854-40-primary-sw_det_saxs_image-2.tiff'),
  WindowsPath('//XF07ID1-WS17/RSoXS Documents/images/users/Eliot/NIST-Eph=460.0084854-40-primary-sw_det_waxs_image-2.tiff')]}
"""
from event_model import Filler, RunRouter
from suitcase import tiff_series,csv
import suitcase.jsonl
from datetime import datetime
from bluesky_darkframes import DarkSubtraction

USERDIR = 'Z:/images/users/'


def factory(name, start_doc):
    filler = Filler(db.reg.handler_reg)

    # filler(name, start_doc)  # modifies doc in place

    def subfactory(name, descriptor_doc):

        if descriptor_doc['name'] in ['primary', 'dark']:
            dt = datetime.now()
            formatted_date = dt.strftime('%Y-%m-%d')
            # #energy = hdr.table(stream_name='baseline')['Beamline Energy_energy'][1]
            # serializer = tiff_series.Serializer(file_prefix=('{start[institution]}/'
            #                                                  '{start[user_name]}/'
            #                                                  '{start[project_name]}/'
            #                                                  f'{formatted_date}/'
            #                                                  '{start[scan_id]}-'
            #                                                  '{start[sample_name]}-'
            #                                                  #'{event[data][en_energy]:.2f}eV-'
            #                                                  ),
            #                                     directory=USERDIR)
            # serializer('start', start_doc)
            # serializer('descriptor', descriptor_doc)
            SAXSsubtractor = DarkSubtraction('Synced_saxs_image')
            WAXSsubtractor = DarkSubtraction('Synced_waxs_image')
            SAXSserializer = tiff_series.Serializer(file_prefix=('{start[institution]}/'
                                                                 '{start[user_name]}/'
                                                                 '{start[project_name]}/'
                                                                 f'{formatted_date}/sd'
                                                                 '{start[scan_id]}-'
                                                                 '{start[sample_name]}-'
                                                                 ),
                                                    directory=USERDIR)
            WAXSserializer = tiff_series.Serializer(file_prefix=('{start[institution]}/'
                                                                 '{start[user_name]}/'
                                                                 '{start[project_name]}/'
                                                                 f'{formatted_date}/wd'
                                                                 '{start[scan_id]}-'
                                                                 '{start[sample_name]}-'),
                                                    directory=USERDIR)

            # Here we push the run 'start' doc through.
            SAXSsubtractor('start', start_doc)
            SAXSsubtractor('descriptor', descriptor_doc)
            SAXSserializer('start', start_doc)
            SAXSserializer('descriptor', descriptor_doc)
            WAXSsubtractor('start', start_doc)
            WAXSsubtractor('descriptor', descriptor_doc)
            WAXSserializer('start', start_doc)
            WAXSserializer('descriptor', descriptor_doc)

            # And by returning this function below, we are routing all other
            # documents *for this run* through here.
            def fill_subtract_and_serialize(name, doc):
                name, doc = filler(name, doc)
                sname, sdoc = SAXSsubtractor(name, doc)
                SAXSserializer(sname, sdoc)
                wname, wdoc = WAXSsubtractor(name, doc)
                WAXSserializer(wname, wdoc)
            if descriptor_doc['name'] == 'primary':
                serializercsv = csv.Serializer(file_prefix=('{start[institution]}/'
                                                            '{start[user_name]}/'
                                                             '{start[project_name]}/'
                                                            f'{formatted_date}/'
                                                            '{start[scan_id]}-'
                                                            '{start[sample_name]}-'
                                                            #'{event[data][Beamline Energy_energy]:.2f}eV-'
                                                            ),
                                               directory=USERDIR,
                                               flush=True,
                                               line_terminator='\n')
                serializercsv('start', start_doc)
                serializercsv('descriptor', descriptor_doc)
                return [fill_subtract_and_serialize,serializercsv]  # fill_subtract_and_serialize
            return [fill_subtract_and_serialize]
        elif descriptor_doc['name'] == 'baseline':
            dt = datetime.now()
            formatted_date = dt.strftime('%Y-%m-%d')
            # energy = hdr.table(stream_name='baseline')['Beamline Energy_energy'][1]
            serializer = csv.Serializer(file_prefix=('{start[institution]}/'
                                                     '{start[user_name]}/'
                                                     '{start[project_name]}/'
                                                     f'{formatted_date}/'
                                                     '{start[scan_id]}-'
                                                     '{start[sample_name]}-'
                                                     #'{event[data][Beamline Energy_energy]:.2f}eV-'
                                                     ),
                                        directory=USERDIR,
                                        flush=True,
                                        line_terminator='\n')
            serializer('start', start_doc)
            serializer('descriptor', descriptor_doc)
            return [serializer]

        else:
            return []

    def cb(name, doc):
        filler(name, doc)  # Fill in place any externally-stored data written by area detector.


    return [cb], [subfactory]


rr = RunRouter([factory])

rr_token = RE.subscribe(rr)  # This should be subscribed *after* db so filling happens after db.insert.


import event_model
import suitcase.jsonl


def factory2(name, start_doc):
    dt = datetime.now()
    formatted_date = dt.strftime('%Y-%m-%d')
    with suitcase.jsonl.Serializer(file_prefix=('{institution}/'
                                                '{user_name}/'
                                                '{project_name}/'
                                                f'{formatted_date}/'
                                                '{scan_id}-'
                                                '{sample_name}-'
                                                ),
                                   directory=USERDIR,
                                   sort_keys=True,
                                   indent=2) as serializer:
        serializer(name, start_doc)
    # We do not need any further documents from the RunRouter.
    return [], []


rr2 = event_model.RunRouter([factory2])
rr2_token = RE.subscribe(rr2)