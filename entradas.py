from classes.truth_table import TruthTable
from classes.qmccluskey import QuineMcCluskey
from classes.dfs import DFS
from classes.converter import Converter

# inputs

# the charges'll be sorted by their priorities
potencias = {
    'supply': [
        {'id': 'F1', 'power': 35000},
        {'id': 'F2', 'power': 25000},
        {'id': 'F3', 'power': 4000},
        {'id': 'F4', 'power': 3000},
        {'id': 'F5', 'power': 5500}
    ],
    'charge': [
        {'id': 'C1', 'power': 19200},
        {'id': 'C2', 'power': 19200},
        {'id': 'C3', 'power': 8800},
        {'id': 'C4', 'power': 5700},
        {'id': 'C5', 'power': 2700}
    ]
}

topology = {
    'S': ['T1'],
    'T1': ['S', 'L'],
    'T2': ['L', 'J1'],
    'L': ['T1', 'T2'],
    'J1': ['T2', 'J2', 'C4'],
    'J2': ['J1', 'J3', 'F5', 'C1'],
    'J3': ['J2', 'J4', 'F1', 'F3', 'C2'],
    'J4': ['J3', 'J5', 'C5'],
    'J5': ['J4', 'F2', 'F4', 'C3'],
    'F1': ['J3'],
    'F2': ['J5'],
    'F3': ['J3'],
    'F4': ['J5'],
    'F5': ['J2'],
    'C1': ['J2'],
    'C2': ['J3'],
    'C3': ['J5'],
    'C4': ['J1'],
    'C5': ['J4']
}

rates = [
    {'id': 'T1', 'rate': [0.00000114]},
    {'id': 'T2', 'rate': [0.00000171]},
    {'id': 'L', 'rate': [0.000104]},
    {'id': 'J1', 'rate': [0.0000114]},
    {'id': 'J2', 'rate': [0.0000114]},
    {'id': 'J3', 'rate': [0.0000114]},
    {'id': 'J4', 'rate': [0.0000114]},
    {'id': 'J5', 'rate': [0.0000114]},
    {'id': 'F1', 'rate': [0.0000114]},
    {'id': 'F2', 'rate': [0.0000114]},
    {'id': 'F3', 'rate': [0.00000761]},
    {'id': 'F4', 'rate': [0.00000761]},
    {'id': 'F5', 'rate': [0.0000143]}
]

distribution = "Failure Rate"

evaluation_metrics = {
    'Reliability': [0, 100000, 10000],
    'MTTF': [],
    'Birnbaum Importance F1': [10000, 'F1'],
    'Birnbaum Importance F2': [10000, 'F2'],
    'Birnbaum Importance F3': [10000, 'F3'],
    'Birnbaum Importance F4': [10000, 'F4'],
    'Birnbaum Importance F5': [10000, 'F5'],
    'Birnbaum Importance T1': [10000, 'T1'],
    'Birnbaum Importance T2': [10000, 'T2']
}

failure_condition = [
    {'gate': 'kofn', 'name': 'gate1', 'k': 1, 'n': 5, 'inputs': ['C1', 'C2', 'C3', 'C4', 'C5']}
]

# main

# Truth Table
truth_table = TruthTable(potencias['supply'], potencias['charge'])
truth_table.analyze()
expressions = truth_table.getOutputExpressions()

# Quine MCcluskey
for charge, exp in expressions.iteritems():
    qm = QuineMcCluskey(exp)
    qm.resolve()
    expressions[charge] = qm.getPrimeImplicants()

# DFS
final_expressions = {}
for charge, exp in expressions.iteritems():
    final_expressions[charge] = []
    for term in exp:
        # lembrar de tratar para muitas subestacoes
        dfs = DFS('S', charge, topology)
        dfs.execute()
        # lembrar de tratar para muitos caminhos
        term_and = [dfs.getPaths()[0][1:]]
        for key, boolean in enumerate(term):
            if boolean == '1':
                dfs = DFS(potencias['supply'][key]['id'], charge, topology)
                dfs.execute()
                term_and += dfs.getPaths()
        final_expressions[charge].append(term_and)

#print final_expressions

# Converter
converter = Converter(final_expressions, distribution, rates, evaluation_metrics, failure_condition)
converter.prepareCommand()
converter.initSharpe()
