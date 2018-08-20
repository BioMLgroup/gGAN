from data_pipeline import reg_network, get_gene_symbols
import numpy as np
import pandas as pd

DEFAULT_ROOT_GENE = 'CRP'
DEFAULT_EVIDENCE = 'Weak'
DEFAULT_DEPTH = np.inf
GNW_DATA_DIR = '../data/gnw/'
NETWORK_FILE = GNW_DATA_DIR + 'source_networks/EColi_n{}_r{}_e{}_d{}_b{}.tsv'
RESULTS_FILE = GNW_DATA_DIR + 'results/EColi_n{}_r{}_e{}_d{}_b{}_multifactorial.tsv'  # EColi_n1076_rCRP_eWeak_dinf_bFalse_multifactorial.tsv


def dump_network(root_gene=DEFAULT_ROOT_GENE, minimum_evidence=DEFAULT_EVIDENCE, depth=DEFAULT_DEPTH, break_loops=True):
    gs = get_gene_symbols()
    nodes, edges = reg_network(gs, root_gene, minimum_evidence, depth, break_loops)
    nb_nodes = len(nodes)
    file_name = NETWORK_FILE.format(nb_nodes, root_gene, minimum_evidence, depth, break_loops)
    with open(file_name, 'w') as f:
        for tf, tg_dict in edges.items():
            for tg, reg_type in tg_dict.items():
                line = '{}\t{}\t{}\n'.format(tf, tg, reg_type)
                f.write(line)
    print('Finished preparing GNW network\nFile:{}'.format(file_name))


def gnw_results(root_gene=DEFAULT_ROOT_GENE, minimum_evidence=DEFAULT_EVIDENCE, depth=DEFAULT_DEPTH,
                break_loops=True):
    # Read results
    gs = get_gene_symbols()
    nodes, edges = reg_network(gs, root_gene, minimum_evidence, depth, break_loops)
    nb_nodes = len(nodes)
    file_name = RESULTS_FILE.format(nb_nodes, root_gene, minimum_evidence, depth, break_loops)
    df = pd.read_csv(file_name, delimiter='\t', header=0)
    df = df.reindex(columns=nodes)
    assert (df.columns == nodes).all()
    expr = df.values
    return expr, nodes


if __name__ == '__main__':
    dump_network(root_gene='CRP',
                 break_loops=False)
    gnw_results(root_gene='CRP',
                break_loops=False)
