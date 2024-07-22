import numpy as np

def relative_abundance(counts):
    total = np.sum(counts)
    return counts / total if total > 0 else counts

def calculate_relative_abundance(taxonomy_df, sample_columns, taxonomy_ranks, output_path):
    relative_abundance_by_rank_dfs = {}

    for rank in taxonomy_ranks:
        grouped = taxonomy_df.groupby(rank)[sample_columns].sum()
        relative_abundance_df = grouped.apply(relative_abundance, axis=1)
        relative_abundance_by_rank_dfs[rank] = relative_abundance_df
        relative_abundance_df.to_csv(f'{output_path}/relative_abundance_{rank}.csv')

    return relative_abundance_by_rank_dfs
