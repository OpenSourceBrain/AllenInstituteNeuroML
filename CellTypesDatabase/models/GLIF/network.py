usage = """
This file can be used to generate networks of the GLIF LEMS models
Usage:

    python network.py -flag(s)
    
    Flag options:
    
    -small      builds and simulates a small network with only L2/3
    -large      builds and simulates a large network with 4 layers
    -noinputs   no input to the network
"""


from tkinter.tix import DirSelectDialog
from neuromllite import Network, Cell, Population, Simulation, Synapse
from neuromllite import RectangularRegion, RandomLayout
from neuromllite import Projection, RandomConnectivity, OneToOneConnector

import sys


def generate(ref="GLIF net test", add_inputs=True, type="large"):

    ################################################################################
    ###   Build new network

    net = Network(id=ref, notes="Network with GLIF cells")

    net.parameters = {
        "N_scaling": 0.005,
        "layer_height": 400,
        "width": 100,
        "depth": 100,
        "input_weight": 1,
        "global_e_scaling": 1,
        "global_i_scaling": 1,
    }
    net.temperature = 32.0
    net.seed = 1234

    # cell_list = {<layer>: [<spiny cell id>, <aspiny cell id>], ...}
    if type == "large":
        cell_list = {
            "L23": ["566320096", "489931668"],
            "L4": ["486558431", "566382734"],
            "L5": ["486052403", "485904755"],
            "L6": ["566303332", "566357260"],  # layer 6a
        }
    elif type == "small":
        cell_list = {"L23": ["566320096", "489931668"]}

    for key, value in cell_list.items():
        for i in value:
            cell = Cell(id=f"GLIF_{i}", lems_source_file=f"{i}/GLIF_{i}__lems.xml")
            net.cells.append(cell)

    if add_inputs:
        input_cell = Cell(id="InputCell", pynn_cell="SpikeSourcePoisson")
        input_cell.parameters = {"start": 0, "duration": 10000000000, "rate": 150}
        net.cells.append(input_cell)

    e_syn = Synapse(
        id="ampa",
        pynn_receptor_type="excitatory",
        pynn_synapse_type="curr_exp",
        parameters={"tau_syn": 0.5},
    )
    net.synapses.append(e_syn)
    i_syn = Synapse(
        id="gaba",
        pynn_receptor_type="inhibitory",
        pynn_synapse_type="curr_exp",
        parameters={"tau_syn": 0.5},
    )
    net.synapses.append(i_syn)

    if type == "large":
        N_full = {
            "L23": {"E": 20683, "I": 5834},
            "L4": {"E": 21915, "I": 5479},
            "L5": {"E": 4850, "I": 1065},
            "L6": {"E": 14395, "I": 2948},
        }
    elif type == "small":
        N_full = {"L23": {"E": 20683, "I": 5834}}

    scale = 0.1

    pops = []
    input_pops = []
    pop_dict = {}

    layers = ["L23", "L4", "L5", "L6"] if type == "large" else ["L23"]

    for l in layers:

        i = 3 - layers.index(l)
        r = RectangularRegion(
            id=l,
            x=0,
            y=i * net.parameters["layer_height"],
            z=0,
            width=net.parameters["width"],
            height=net.parameters["layer_height"],
            depth=net.parameters["depth"],
        )
        net.regions.append(r)

        for t in ["E", "I"]:

            try:
                import opencortex.utils.color as occ

                if l == "L23":
                    if t == "E":
                        color = occ.L23_PRINCIPAL_CELL
                    if t == "I":
                        color = occ.L23_INTERNEURON
                if l == "L4":
                    if t == "E":
                        color = occ.L4_PRINCIPAL_CELL
                    if t == "I":
                        color = occ.L4_INTERNEURON
                if l == "L5":
                    if t == "E":
                        color = occ.L5_PRINCIPAL_CELL
                    if t == "I":
                        color = occ.L5_INTERNEURON
                if l == "L6":
                    if t == "E":
                        color = occ.L6_PRINCIPAL_CELL
                    if t == "I":
                        color = occ.L6_INTERNEURON

            except:
                color = ".8 0 0" if t == "E" else "0 0 1"

            pop_id = "%s_%s" % (l, t)
            if t == "E":
                cell_id = "GLIF_%s" % (cell_list[l][0])
            elif t == "I":
                cell_id = "GLIF_%s" % (cell_list[l][1])
            pops.append(pop_id)
            ref = "l%s%s" % (l[1:], t.lower())

            exec(
                ref
                + " = Population(id=pop_id, size='int(%s*N_scaling)'%N_full[l][t], component=cell_id, properties={'color':color, 'type':t})"
            )
            exec("%s.random_layout = RandomLayout(region = r.id)" % ref)
            exec("net.populations.append(%s)" % ref)
            exec("pop_dict['%s'] = %s" % (pop_id, ref))

            if add_inputs:
                color = ".8 .8 .8"
                input_id = "%s_%s_input" % (l, t)
                input_pops.append(input_id)
                input_ref = "l%s%s_i" % (l[1:], t.lower())
                exec(
                    input_ref
                    + " = Population(id=input_id, size='int(%s*N_scaling)'%N_full[l][t], component=input_cell.id, properties={'color':color})"
                )
                exec("%s.random_layout = RandomLayout(region = r.id)" % input_ref)
                exec("net.populations.append(%s)" % input_ref)

    conn_probs = [
        [0.1009, 0.1689, 0.0437, 0.0818, 0.0323, 0.0, 0.0076, 0.0],
        [0.1346, 0.1371, 0.0316, 0.0515, 0.0755, 0.0, 0.0042, 0.0],
        [0.0077, 0.0059, 0.0497, 0.135, 0.0067, 0.0003, 0.0453, 0.0],
        [0.0691, 0.0029, 0.0794, 0.1597, 0.0033, 0.0, 0.1057, 0.0],
        [0.1004, 0.0622, 0.0505, 0.0057, 0.0831, 0.3726, 0.0204, 0.0],
        [0.0548, 0.0269, 0.0257, 0.0022, 0.06, 0.3158, 0.0086, 0.0],
        [0.0156, 0.0066, 0.0211, 0.0166, 0.0572, 0.0197, 0.0396, 0.2252],
        [0.0364, 0.001, 0.0034, 0.0005, 0.0277, 0.008, 0.0658, 0.1443],
    ]

    if add_inputs:
        for p in pops:
            proj = Projection(
                id="proj_input_%s" % p,
                presynaptic="%s_input" % p,
                postsynaptic=p,
                synapse=e_syn.id,
                delay=2,
                weight="input_weight",
            )
            proj.one_to_one_connector = OneToOneConnector()
            net.projections.append(proj)

    for pre_i in range(len(pops)):
        for post_i in range(len(pops)):
            pre = pops[pre_i]
            post = pops[post_i]
            prob = conn_probs[post_i][pre_i]  #######   TODO: check!!!!
            weight = 1
            syn = e_syn
            if prob > 0:
                if "I" in pre:
                    weight = -1
                    syn = i_syn
                proj = Projection(
                    id="proj_%s_%s" % (pre, post),
                    presynaptic=pre,
                    postsynaptic=post,
                    synapse=syn.id,
                    delay=1,
                    weight=weight,
                )
                proj.random_connectivity = RandomConnectivity(probability=prob)
                net.projections.append(proj)

    new_file = net.to_json_file("%s.json" % (net.id))
    ################################################################################
    ###   Build Simulation object & save as JSON

    record_traces = {}
    record_spikes = {}

    from neuromllite.utils import evaluate

    for p in pops:
        forecast_size = evaluate(pop_dict[p].size, net.parameters)
        record_traces[p] = list(range(min(2, forecast_size)))
        record_spikes[p] = "*"
    for ip in input_pops:
        record_spikes[ip] = "*"

    sim = Simulation(
        id="Sim%s" % (net.id),
        network=new_file,
        duration="100",
        dt="0.025",
        seed=1234,
        record_traces=record_traces,
        record_spikes=record_spikes,
    )

    sim.to_json_file("%s.nmllite.json" % (sim.id))

    return sim, net


if __name__ == "__main__":

    if len(sys.argv) == 1:
        print(usage)
        exit()
    if "-small" in sys.argv:
        type = "small"
    else:
        type = "large"

    if "-noinputs" in sys.argv:
        sim, net = generate(f"GLIF_net_noinputs_{type}", False, type)
    else:
        sim, net = generate(f"GLIF_net_{type}", True, type)

    ################################################################################
    ###   Run in some simulators

    from neuromllite.NetworkGenerator import check_to_generate_or_run

    check_to_generate_or_run(["-jnml", "-graph"], sim)
