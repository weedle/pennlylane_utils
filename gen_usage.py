#!/Users/kevinjayamanna/miniconda3/bin/python
import pennylane as qml
import numpy as np
import pandas as pd
import sys

from gates import setup_gates, gates

import numbers

#dev = qml.device("default.qubit")
dev = qml.device("default.mixed")
starting_state = np.sqrt(np.array([1, 0]))
starting_wires = []

def get_trace_dist(rho, delta):
    return 0.5 * np.trace(np.sqrt(np.conj(rho - delta).T * (rho - delta)))

def get_fidelity(rho, delta):
    return (np.trace(np.sqrt(np.sqrt(rho)*delta*np.sqrt(rho))))**2
    return np.conj(state).T * state

def get_exp_val(state, op, is_matrix=True):
    if not is_matrix:
        op = qml.matrix(op)(wires=0)
    return np.trace(qml.math.dot(state, op))

@qml.qnode(dev)
def pure_state_to_dens_mat(state, wires):
    qml.MottonenStatePreparation(state, wires)
    return qml.density_matrix(wires)

@qml.qnode(dev)
def main_q_fn(args):
	global starting_wires
	global starting_state
	if not isinstance(starting_wires, numbers.Number) and len(starting_wires) == 0:
		starting_wires = 0
	else:
		qml.MottonenStatePreparation(starting_state, wires=starting_wires)
	for arg in args:
		if len(arg[2]) > 0:
			gates[arg[0]](*arg[1], wires=arg[2])
		else:
			gates[arg[0]](*arg[1], wires=starting_wires)
	
	return qml.probs(), qml.state()


def get_state(given_args):
    qnode = qml.QNode(main_q_fn, dev)
    to_call = []
    wires = []
    args = []
    last_call = ""

    is_wires = False
    preamble = []
    for arg in given_args:
        if arg == "w":
            is_wires = True
        else:
            if arg in gates.keys():
                is_wires = False
                if last_call != "":
                    to_call.append([last_call, args, wires])
                    args = []
                    wires = []
                last_call = arg
            else:
                if not isinstance(arg, numbers.Number):
                    arg = eval(arg)
                if last_call == "":
                    preamble.append(arg)
                else:
                    if is_wires:
                        wires.append(arg)
                    else:
                        args.append(arg)
    allowed_preambles = [2**n + n for n in range(10)]
    if len(preamble) > 0:
        if len(preamble) not in allowed_preambles:
            print("Error: should have 2**n values in starting state and n specified wires.")
            return
        point_of_wires = allowed_preambles.index(len(preamble))
        starting_state = preamble[:len(preamble)-point_of_wires]
        starting_wires = preamble[-point_of_wires:]
    to_call.append([last_call, args, wires])

    return qnode(to_call)

if len(sys.argv) > 1:
    print(get_state(sys.argv[1:])[0]) 
