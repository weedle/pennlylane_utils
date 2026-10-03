import pennylane as qml
import numpy as np
import pandas as pd
import sys

from gates import setup_gates, gates

dev = qml.device("default.qubit")
starting_state = np.sqrt(np.array([1, 0]))
starting_wires = []


@qml.qnode(dev)
def main_q_fn(args):
	global starting_wires
	global starting_state
	if len(starting_wires) == 0:
		starting_wires = 0
	else:
		qml.MottonenStatePreparation(starting_state, wires=starting_wires)
	for arg in args:
		if len(arg[2]) > 0:
			gates[arg[0]](*arg[1], wires=arg[2])
		else:
			gates[arg[0]](*arg[1])
	
	return qml.probs()

qnode = qml.QNode(main_q_fn, dev)

to_call = []
args = []
wires = []
last_call = ""

is_wires = False
preamble = []

for arg in sys.argv[1:]:
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
			if last_call == "":
				preamble.append(eval(arg))
			else:
				if is_wires:
					wires.append(eval(arg))
				else:
					args.append(eval(arg))
allowed_preambles = [2**n + n for n in range(10)]
if len(preamble) > 0:
	if len(preamble) not in allowed_preambles:
		print("Error: should have 2**n values in starting state and n specified wires.")
		exit(0)
	point_of_wires = allowed_preambles.index(len(preamble))
	starting_state = preamble[:len(preamble)-point_of_wires]
	starting_wires = preamble[-point_of_wires:]
to_call.append([last_call, args, wires])

print(qnode(to_call))
