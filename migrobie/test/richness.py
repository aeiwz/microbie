import pandas as pd
import numpy as np

def calculate_richness(group):
    return (group > 0).sum(axis=0)

def calculate_richness_per_sample(taxonomy_df, sample_columns, taxonomy_ranks, output_path):
    richness_by_sample_rank_dfs = {}

    for rank in taxonomy_ranks:
        grouped = taxonomy_df.groupby(rank)[sample_columns]
        richness_df = grouped.apply(calculate_richness)
        richness_by_sample_rank_dfs[rank] = richness_df
        richness_df.to_csv(f'{output_path}/richness_per_sample_{rank}.csv')

    return richness_by_sample_rank_dfs
