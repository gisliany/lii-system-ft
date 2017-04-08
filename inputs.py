from classes.truth_table import TruthTable
from classes.qmccluskey import QuineMcCluskey
from classes.dfs import DFS
from classes.converter import Converter

# inputs

# the loads'll be sorted by their priorities
potencias = {
    'source': [
        {'id': 'S1', 'power': 35000},
        {'id': 'S2', 'power': 25000},
        {'id': 'S3', 'power': 4000},
        {'id': 'S4', 'power': 3000},
        {'id': 'S5', 'power': 5500}
    ],
    'load': [
        {'id': 'L1', 'power': 19200},
        {'id': 'L2', 'power': 19200},
        {'id': 'L3', 'power': 8800},
        {'id': 'L4', 'power': 5700},
        {'id': 'L5', 'power': 2700}
    ]
}

topology = {
    'S': ['T1'],
    'T1': ['S', 'N1'],
    'T2': ['N1', 'J1'],
    'N1': ['T1', 'T2'],
    'J1': ['T2', 'J2', 'L4'],
    'J2': ['J1', 'J3', 'S5', 'L1'],
    'J3': ['J2', 'J4', 'S1', 'S3', 'L2'],
    'J4': ['J3', 'J5', 'L5'],
    'J5': ['J4', 'S2', 'S4', 'L3'],
    'S1': ['J3'],
    'S2': ['J5'],
    'S3': ['J3'],
    'S4': ['J5'],
    'S5': ['J2'],
    'L1': ['J2'],
    'L2': ['J3'],
    'L3': ['J5'],
    'L4': ['J1'],
    'L5': ['J4']
}

rates = [
    {'id': 'T1', 'rate': [0.00000114]},
    {'id': 'T2', 'rate': [0.00000171]},
    {'id': 'N1', 'rate': [0.000104]},
    {'id': 'J1', 'rate': [0.0000114]},
    {'id': 'J2', 'rate': [0.0000114]},
    {'id': 'J3', 'rate': [0.0000114]},
    {'id': 'J4', 'rate': [0.0000114]},
    {'id': 'J5', 'rate': [0.0000114]},
    {'id': 'S1', 'rate': [0.0000114]},
    {'id': 'S2', 'rate': [0.0000114]},
    {'id': 'S3', 'rate': [0.00000761]},
    {'id': 'S4', 'rate': [0.00000761]},
    {'id': 'S5', 'rate': [0.0000143]}
]

distribution = "Failure Rate"

# The first and maybe second and third parameters are associated with time
evaluation_metrics = {
    'Reliability': [0, 100000, 10000],
    'MTTF': [],
    'Birnbaum Importance S1': [10000, 'S1'],
    'Birnbaum Importance S2': [10000, 'S2'],
    'Birnbaum Importance S3': [10000, 'S3'],
    'Birnbaum Importance S4': [10000, 'S4'],
    'Birnbaum Importance S5': [10000, 'S5'],
    'Birnbaum Importance T1': [10000, 'T1'],
    'Birnbaum Importance T2': [10000, 'T2']
}

failure_condition = [
    {'gate': 'kofn', 'name': 'gate1', 'k': 1, 'n': 5, 'inputs': ['L1', 'L2', 'L3', 'L4', 'L5']}
]

# main

# Truth Table
truth_table = TruthTable(potencias['source'], potencias['load'])
truth_table.analyze()
expressions = truth_table.getOutputExpressions()

# Quine MCcluskey
for load, exp in expressions.iteritems():
    qm = QuineMcCluskey(exp)
    qm.resolve()
    expressions[load] = qm.getPrimeImplicants()

# DFS
final_expressions = {}
for load, exp in expressions.iteritems():
    final_expressions[load] = []
    for term in exp:
        # lembrar de tratar para muitas subestacoes
        dfs = DFS('S', load, topology)
        dfs.execute()
        # lembrar de tratar para muitos caminhos
        term_and = [dfs.getPaths()[0][1:]]
        for key, boolean in enumerate(term):
            if boolean == '1':
                dfs = DFS(potencias['source'][key]['id'], load, topology)
                dfs.execute()
                term_and += dfs.getPaths()
        final_expressions[load].append(term_and)

#print final_expressions

# Converter
converter = Converter(final_expressions, distribution, rates, evaluation_metrics, failure_condition)
converter.prepareCommand()
converter.initSharpe()
