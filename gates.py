import pennylane as qml
gates = {}
def setup_gates():
	global gates
	gates = {
		"H": qml.Hadamard,
		"PX": qml.PauliX,
		"PY": qml.PauliY,
		"PZ": qml.PauliZ, 
		"S": qml.S,
		"T": qml.T,
		"SX": qml.SX,
		"CNOT": qml.CNOT,
		"CZ": qml.CZ,
		"CY": qml.CY,
		"CH": qml.CH,
		"SWAP": qml.SWAP,
		"CSWAP": qml.CSWAP,
		"ISWAP": qml.ISWAP,
		"RX": qml.RX,
		"RY": qml.RY,
		"RZ": qml.RZ,
		"Toffoli": qml.Toffoli,
		"CSWAP": qml.CSWAP,
		"CRZ": qml.CRZ,
		"CRY": qml.CRY,
		"CRX": qml.CRX,
	}
setup_gates()
