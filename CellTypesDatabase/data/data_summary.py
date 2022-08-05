import os
import sys
import os.path
import json

import matplotlib.pyplot as plt

from pyneuroml import pynml
import airspeed

nogui = "-nogui" in sys.argv

HTML_TEMPLATE_FILE = "CellInfo_TEMPLATE.html"


def make_html_file(info, template=HTML_TEMPLATE_FILE, target="CellInfo.html"):
    merged = merge_with_template(info, template)
    html_dir = "summary"
    new_html_file = os.path.join(html_dir, target)
    lf = open(new_html_file, "w")
    lf.write(merged)
    lf.close()
    print("Written HTML info to: %s" % new_html_file)


def make_md_file():

    html_dir = "summary"
    new_html_file = os.path.join(html_dir, "CellInfo.html")
    new_md_file = os.path.join(html_dir, "README.md")

    hf = open(new_html_file, "r")
    mf = open(new_md_file, "w")
    started = False
    for line in hf:
        l = line.strip()
        if l == "</body>":
            started = False
        if started:
            mf.write(l + "\n")
        if l == "<body>":
            started = True

    mf.close()
    hf.close()
    print("Written Markdown info to: %s" % new_md_file)


def merge_with_template(model, templfile):
    if not os.path.isfile(templfile):
        templfile = os.path.join(os.path.dirname(sys.argv[0]), templfile)
    with open(templfile) as f:
        templ = airspeed.Template(f.read())
    return templ.merge(model)


def get_if_iv_for_dataset(dataset_analysis_file):

    with open(dataset_analysis_file, "r") as json_file:
        data = json.load(json_file)

    id = data["data_set_id"]
    sweeps = data["sweeps"]

    print("Looking at data analysis in %s (dataset: %s)" % (dataset_analysis_file, id))

    currents_v_sub = {}
    currents_rate_spike = {}

    for s in sweeps.keys():
        current = float(sweeps[s]["sweep_metadata"]["aibs_stimulus_amplitude_pa"])
        print("Sweep %s (%s pA)" % (s, current))

        freq_key = "%s:mean_spike_frequency" % (s)
        steady_state_key = "%s:average_1000_1200" % (s)

        if (
            freq_key in sweeps[s]["pyelectro_iclamp_analysis"]
            and sweeps[s]["pyelectro_iclamp_analysis"][freq_key] > 0
        ):
            currents_rate_spike[current] = sweeps[s]["pyelectro_iclamp_analysis"][
                freq_key
            ]
        else:
            currents_rate_spike[current] = 0
            currents_v_sub[current] = sweeps[s]["pyelectro_iclamp_analysis"][
                steady_state_key
            ]

    curents_sub = list(currents_v_sub.keys())
    curents_sub.sort()
    v_sub = [currents_v_sub[c] for c in curents_sub]

    curents_spike = list(currents_rate_spike.keys())
    curents_spike.sort()
    v = [currents_rate_spike[c] for c in curents_spike]

    return data, v_sub, curents_sub, v, curents_spike


def analyse_extracted_data():

    analysed = []

    analysed = [f for f in os.listdir(".") if (f.endswith("_analysis.json"))]
    # analysed = [ f for f in os.listdir('.') if (f.endswith('_analysis.json')) ]

    analysed.sort()

    info = {}
    info[
        "info"
    ] = "Cell models tuned to data extracted from Cell Types Database. Note: these are preliminary models designed to test the framework for generating NeuroML models from this data, not the final, optimised models."

    info["datasets"] = []

    to_include = None
    # to_include = ['468120757']
    # to_include = ['477127614','476686112']
    # to_include = ['477127614']

    test = "-test" in sys.argv

    if test:
        to_include = ["464198958"]

    for f in analysed:

        if to_include == None or f.split("_")[0] in to_include:

            print("*************************\n Looking at: %s" % f)

            dataset = {}
            info["datasets"].append(dataset)

            """
            with open(f, "r") as json_file:
                data = json.load(json_file)

            id = data['data_set_id']
            sweeps = data['sweeps']

            print("Looking at data analysis in %s (dataset: %s)"%(f,id))

            dataset['id'] = id

            currents_v_sub = {}
            currents_rate_spike = {}

            for s in sweeps.keys():
                current = float(sweeps[s]["sweep_metadata"]["aibs_stimulus_amplitude_pa"])
                print("Sweep %s (%s pA)"%(s, current))

                freq_key = '%s:mean_spike_frequency'%(s)
                steady_state_key = '%s:average_1000_1200'%(s)

                if sweeps[s]["pyelectro_iclamp_analysis"].has_key(freq_key):
                    currents_rate_spike[current] = sweeps[s]["pyelectro_iclamp_analysis"][freq_key]
                else:
                    currents_rate_spike[current] = 0
                    currents_v_sub[current] = sweeps[s]["pyelectro_iclamp_analysis"][steady_state_key]

            curents_sub = currents_v_sub.keys()
            curents_sub.sort()
            v = [currents_v_sub[c] for c in curents_sub]
            """
            data, v_sub, curents_sub, v, curents_spike = get_if_iv_for_dataset(f)

            id = data["data_set_id"]
            dataset["id"] = data["data_set_id"]
            metas = ["aibs_cre_line", "aibs_dendrite_type", "location"]
            for m in metas:
                dataset[m] = data[m]

            target_file = "summary/%s_%s.png"

            pynml.generate_plot(
                [curents_sub],
                [v_sub],
                "Subthreshold responses: %s" % id,
                colors=["k"],
                linestyles=["-"],
                markers=["o"],
                xaxis="Current (pA)",
                yaxis="Steady state (mV)",
                xlim=[-200, 400],
                ylim=[-120, -40],
                grid=True,
                show_plot_already=False,
                save_figure_to=target_file % ("subthreshold", id),
            )
            # plt.plot(curents_sub, , color='k', linestyle='-', marker='o')

            pynml.generate_plot(
                [curents_spike],
                [v],
                "Spiking frequencies: %s" % id,
                colors=["k"],
                linestyles=["-"],
                markers=["o"],
                xaxis="Current (pA)",
                yaxis="Firing frequency (Hz)",
                xlim=[-200, 400],
                ylim=[-10, 120],
                grid=True,
                show_plot_already=False,
                save_figure_to=target_file % ("spikes", id),
            )

            data0, indices = pynml.reload_standard_dat_file("%s.dat" % id)
            x = []
            y = []
            tt = [t * 1000 for t in data0["t"]]
            for i in indices:
                x.append(tt)
                y.append([v * 1000 for v in data0[i]])

            cols = ["b", "g", "r", "c", "m", "y", "k"]

            ax = pynml.generate_plot(
                x,
                y,
                "Example traces from: %s" % id,
                xaxis="Time (ms)",
                yaxis="Membrane potential (mV)",
                ylim=[-120, 60],
                colors=cols,
                show_plot_already=False,
                save_figure_to=target_file % ("traces", id),
            )

            ax.spines["right"].set_visible(False)
            ax.spines["top"].set_visible(False)
            ax.yaxis.set_ticks_position("left")
            ax.xaxis.set_ticks_position("bottom")

            sweeps = data["sweeps"]

            from data_helper import CURRENT_DATASETS, DATASET_TARGET_SWEEPS

            i = 0
            for s in DATASET_TARGET_SWEEPS[data["data_set_id"]]:
                current = float(
                    sweeps[str(s)]["sweep_metadata"]["aibs_stimulus_amplitude_pa"]
                )
                print("--- Sweep %s (%s pA)" % (s, current))
                plt.text(
                    1320, +8 * i, "%s pA" % (float("%.2f" % current)), color=cols[i]
                )
                i += 1

            plt.savefig(target_file % ("traces", id), bbox_inches="tight", pad_inches=0)

            ax = pynml.generate_plot(
                x,
                y,
                "Example traces from: %s" % id,
                ylim=[-120, 60],
                colors=cols,
                grid=False,
                show_plot_already=False,
            )

            scale = 1 if not "477127614" in f else 1000

            ax.plot(
                [1300 * scale, 1300 * scale, 1500 * scale],
                [40, 20, 20],
                color="k",
                linewidth=5,
                marker="",
                solid_capstyle="butt",
                solid_joinstyle="miter",
            )

            plt.axis("off")

            fig_file = target_file % ("traces_FIG", id)
            plt.savefig(fig_file, bbox_inches="tight", pad_inches=0)
            from PIL import Image

            img = Image.open(fig_file)

            img2 = img.crop((60, 40, 660, 480))
            img2.save(fig_file)

    print(info)
    make_html_file(info)
    make_md_file()

    if not nogui:
        plt.show()


if __name__ == "__main__":

    analyse_extracted_data()
