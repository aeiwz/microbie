import pandas as pd
import numpy as np
from scipy.stats import entropy
from scipy.optimize import minimize_scalar

def calculate_diversity_indices(file_path, metadata_columns=9):
    """
    Calculate diversity indices for each sample in the taxonomy CSV file.
    
    Parameters:
    - file_path (str): Path to the taxonomy CSV file.
    - metadata_columns (int): Number of metadata columns in the file to exclude from sample columns. Default is 9.
    
    Returns:
    - pd.DataFrame: DataFrame with calculated diversity indices for each sample.
    """
    # Load the taxonomy CSV file
    taxonomy_df = pd.read_csv(file_path)

    # Extract only the sample columns
    sample_columns = taxonomy_df.columns[:-metadata_columns]

    def berger_parker_index(counts):
        return np.max(counts) / np.sum(counts)

    def effective_number_of_species(shannon_index):
        return np.exp(shannon_index)

    def fishers_alpha(counts):
        a = sum(counts)
        s = len(counts)
        
        def equation(alpha):
            return (s / alpha) - sum([((alpha / (alpha + k)) ** k) for k in counts])
        
        res = minimize_scalar(equation, bounds=(0.01, 100), method='bounded')
        return res.x

    def inverse_simpson_index(counts):
        total = np.sum(counts)
        return 1 / np.sum((counts / total) ** 2)

    def pielou_evenness(shannon_index, richness):
        return shannon_index / np.log(richness)

    def richness(counts):
        return np.sum(counts > 0)

    def shannon_diversity_index(counts):
        return entropy(counts, base=np.e)

    def simpson_index(counts):
        total = np.sum(counts)
        return np.sum((counts / total) ** 2)

    # Initialize a dictionary to store results
    results = {}

    # Calculate indices for each sample
    for sample in sample_columns:
        counts = taxonomy_df[sample].values
        shannon_index = shannon_diversity_index(counts)
        
        results[sample] = {
            'Berger Parker index': berger_parker_index(counts),
            'Effective number of species': effective_number_of_species(shannon_index),
            'Fisher\'s alpha': fishers_alpha(counts),
            'Inverse Simpson\'s index': inverse_simpson_index(counts),
            'Pielou\'s evenness': pielou_evenness(shannon_index, richness(counts)),
            'Richness': richness(counts),
            'Shannon diversity index': shannon_index,
            'Simpson\'s index': simpson_index(counts),
            'Total count': np.sum(counts)
        }

    # Convert results to a DataFrame for better visualization
    results_df = pd.DataFrame(results).T
    results_df.sort_index(inplace=True)
    
    return results_df

