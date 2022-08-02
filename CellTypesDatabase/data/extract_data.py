# Based on https://github.com/stripathy/AIBS_cell_types/blob/master/Allen_ephys_playground.ipynb

import matplotlib.pyplot as pylab
import numpy as np

from allensdk.api.queries.cell_types_api import CellTypesApi
from allensdk import __version__ as allensdk_ver
import time
import sys
import h5py

import data_helper as DH

from pyelectro import utils
from pyelectro import __version__ as pyel_ver

import pprint

pp = pprint.PrettyPrinter(indent=4)

ct = CellTypesApi()

plot = False  # not '-nogui' in sys.argv
test = "-test" in sys.argv


def extract_info_from_nwb_file(dataset_id, raw_ephys_file_name):

    info = {}

    import numpy as np

    h5f = h5py.File(raw_ephys_file_name, "r")
    metas = [
        "aibs_cre_line",
        "aibs_dendrite_type",
        "intracellular_ephys/Electrode 1/location",
    ]
    for m in metas:
        d = h5f.get("/general/%s" % m)
        # print ('%s: %s' % (d[()], type(d)))
        val = d[()]
        if not isinstance(val, str):
            val = val.decode("ascii")
        # print("%s = \t%s"%(m,val))
        info[m.split("/")[-1]] = val
    h5f.close()

    from allensdk.core.nwb_data_set import NwbDataSet

    data_set = NwbDataSet(raw_ephys_file_name)

    sweep_numbers = data_set.get_experiment_sweep_numbers()
    """if test:
        sweep_numbers = [33,45]"""

    sweep_numbers.sort()
    print("sweep_numbers: %s" % sweep_numbers)

    info[DH.DATASET] = dataset_id
    info[DH.COMMENT] = "Data analysed on %s" % (time.ctime())

    info[DH.PYELECTRO_VERSION] = pyel_ver
    info[DH.ALLENSDK_VERSION] = allensdk_ver
    info["h5py_version"] = h5py.__version__
    info[DH.SWEEPS] = {}

    for sweep_number in sweep_numbers:

        sweep_data = data_set.get_sweep(sweep_number)
        # print(data_set.get_sweep_metadata(sweep_number))

        if (
            data_set.get_sweep_metadata(sweep_number)["aibs_stimulus_name"].decode(
                "ascii"
            )
            == "Long Square"
        ):
            sweep_info = {}
            md = data_set.get_sweep_metadata(sweep_number)
            sweep_info[DH.METADATA] = {}
            for k in md:
                sweep_info[DH.METADATA][k] = (
                    md[k] if not type(md[k]) == bytes else md[k].decode("ascii")
                )
            info[DH.SWEEPS]["%i" % sweep_number] = sweep_info
            sweep_info[DH.SWEEP] = sweep_number

            # start/stop indices that exclude the experimental test pulse (if applicable)
            index_range = sweep_data["index_range"]

            # stimulus is a numpy array in amps
            stimulus = sweep_data["stimulus"][index_range[0] : index_range[-1]]

            # response is a numpy array in volts
            response = sweep_data["response"][index_range[0] : index_range[-1]] * 1000

            # sampling rate is in Hz
            sampling_rate = sweep_data["sampling_rate"]

            # define some time points in seconds (i.e., convert to absolute time)
            time_pts = (
                np.arange(0, len(stimulus) / sampling_rate, 1.0 / sampling_rate) * 1000
            )

            comment = "Sweep: %i in %i; %sms -> %sms; %sA -> %sA; %smV -> %smV" % (
                sweep_number,
                dataset_id,
                time_pts[0],
                time_pts[-1],
                np.amin(stimulus),
                np.amax(stimulus),
                np.amin(response),
                np.amax(response),
            )
            print(comment)

            sweep_info[DH.COMMENT] = comment

            analysis = utils.simple_network_analysis(
                {sweep_number: response},
                time_pts,
                extra_targets=[
                    "%s:value_280" % sweep_number,
                    "%s:average_1000_1200" % sweep_number,
                    "%s:average_100_200" % sweep_number,
                ],
                end_analysis=1500,
                plot=plot,
                show_plot_already=False,
                verbose=True,
            )

            sweep_info[DH.ICLAMP_ANALYSIS] = analysis

    analysis_file_name = "%s_analysis.json" % (dataset_id)
    analysis_file = open(analysis_file_name, "w")
    pretty = pprint.pformat(info, width=190, indent=4)
    pretty = pretty.replace("'", '"')
    pretty = pretty.replace('u"', '"')
    analysis_file.write(pretty)
    analysis_file.close()

    print("Written info to %s" % analysis_file_name)


if __name__ == "__main__":

    dataset_ids = DH.CURRENT_DATASETS
    if test:
        dataset_ids = [464198958]

    for dataset_id in dataset_ids:

        raw_ephys_file_name = "%d_raw_data.nwb" % dataset_id

        extract_info_from_nwb_file(dataset_id, raw_ephys_file_name)

    if plot:
        pylab.show()
