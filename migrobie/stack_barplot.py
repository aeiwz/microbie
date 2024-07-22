import pandas as pd
import plotly.graph_objects as go
import plotly.express as px



# Function to plot alpha abundance
def plot_alpha_abundance(df: pd.DataFrame, plot_col: str, top_rank: int =10, rank: str='Species', fig_high: int=900, fig_width: int=300):
    
    '''
    Function to plot alpha abundance
    
    Parameters:
    df: pd.DataFrame
        The input dataframe containing the abundance counts
        plot_col: str
        The column to plot the abundance counts against
        top_rank: int
        The number of top genera to plot
        rank: str
        The taxonomic rank to consider
        fig_high: int
        The height of the figure
        fig_width: int
        The width of the figure
        
        Returns:
        fig: go.Figure
        The plotly figure object
        
    '''
    # Select only numeric columns for abundance calculations
    numeric_df = df.select_dtypes(include=[int, float])
    
    # Sum the abundance counts for each genus across all samples and groups
    abundance_sums = numeric_df.sum().sort_values(ascending=False)

    # Identify the top N most abundant genera
    top_genera = abundance_sums.head(top_rank).index

    # Filter the dataset to include only the top genera and the plotting column
    df_top = df[[plot_col] + list(top_genera)]

    # Sum the counts for each group/sample, considering only numeric columns
    group_sums = df_top.groupby(plot_col).sum(numeric_only=True).reset_index()

    # Normalize the counts to percentages
    group_sums.iloc[:, 1:] = group_sums.iloc[:, 1:].div(group_sums.iloc[:, 1:].sum(axis=1), axis=0) * 100

    # Define a color palette
    color_palette = px.colors.qualitative.Plotly

    # Assign colors to each genus
    genus_colors = {genus: color_palette[i % len(color_palette)] for i, genus in enumerate(top_genera)}

    # Initialize the figure
    fig = go.Figure()

    # Add a stacked bar trace for each genus
    for col in group_sums.columns[1:]:
        fig.add_trace(
            go.Bar(
                x=group_sums[plot_col],
                y=group_sums[col],
                name=col,
                marker_color=genus_colors[col]
            )
        )

    # Update layout
    fig.update_layout(
        title_text=f"Stacked Bar Plot of Top {top_rank} Alpha Abundance",
        barmode='stack',
        xaxis_title=f"{plot_col}",
        yaxis_title="Percentage",
        legend_title=f"{rank}"
    )

    # Set figure size
    fig.update_layout(
        autosize=False,
        width=fig_width,
        height=fig_high,
    )

    return fig
