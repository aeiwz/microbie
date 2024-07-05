# -*- coding: utf-8 -*-

import pandas as pd
import plotly.graph_objects as go

class sankey_plot():
    import pandas as pd
    import plotly.graph_objects as go
    
    
    def __init__(self, data: pd.DataFrame, n_top_rank:int = 40) -> None:
        import pandas as pd
        import plotly.graph_objects as go
        self.data = data
        self.n_top_rank = n_top_rank
        
    def plot(self, taxonomy_level: list = ['superkingdom', 'kingdom', 'phylum', 'class', 'order', 'family', 'genus', 'species'], exclude_unknown: bool = True, n_read_column: str = 'total', express_abundance: str = 'percentage'):
        
        
        import pandas as pd
        import plotly.graph_objects as go
        
        
        data = self.data
        n_top = self.n_top_rank

        # Sort the data and take the top 30
        data = data.sort_values(by=n_read_column, ascending=False).iloc[:n_top]

        # Replace underscores with spaces
        data = data.replace('_', ' ', regex=True)

        # Remove rows with 'Unknown' in specified columns
        taxonomy_columns = taxonomy_level
        
        #ch
        
        if exclude_unknown is True:
            data = data[~data[taxonomy_columns].isin(['Unknown']).any(axis=1)] # 
        else:
            pass
        


        # Initialize lists and dictionaries
        nodes = []
        links = []
        node_indices = {}
        node_sizes = {}
        node_sizes_percent = {}
        node_index = 0

        # Populate the nodes and node_indices dictionary
        for column in taxonomy_columns:
            unique_values = data[column].unique()
            for value in unique_values:
                if value not in node_indices:
                    nodes.append(value)
                    node_indices[value] = node_index
                    node_index += 1

        # Calculate node sizes and percentages
        total_sum = data[n_read_column].sum()
        for column in taxonomy_columns:
            group_sum = data.groupby(column)[n_read_column].sum()
            for value, total in group_sum.items():
                node_sizes[value] = node_sizes.get(value, 0) + total
                node_sizes_percent[value] = node_sizes_percent.get(value, 0) + (total / total_sum * 100)

        # Create the links
        for _, row in data.iterrows():
            for i in range(len(taxonomy_columns) - 1):
                source = row[taxonomy_columns[i]]
                target = row[taxonomy_columns[i + 1]]
                value = row[n_read_column]
                links.append({
                    'source': node_indices[source],
                    'target': node_indices[target],
                    'value': value
                })

        # Prepare custom hover data
        custom_hover = []
        for column in taxonomy_columns:
            group_percent = (data.groupby(column)[n_read_column].sum() / total_sum * 100).round(3)
            custom_hover.append(group_percent.to_dict())
            
            
            
        custom_hover = []
        for i in taxonomy_columns:
            total_group = data.groupby(i)[n_read_column].sum()
            total_sum = data[n_read_column].sum()
            percent = total_group/total_sum*100
            # convert series to dict {index: value}
            percent_dict = percent.to_dict()
            custom_hover.append({i: percent_dict})

        # Create nodes with size based on total read count
        nodes_with_size = [{
            'name': f'<i>{node}</i>',
            'size': node_sizes.get(node, 0),
            'percent': node_sizes_percent.get(node, 0)
        } for node in nodes]

        # Convert lists to dataframes for easier manipulation
        nodes_df = pd.DataFrame(nodes, columns=['name'])
        links_df = pd.DataFrame(links)

        # Create the Sankey diagram
        fig = go.Figure(data=[go.Sankey(
            node=dict(
                pad=15,
                thickness=20,
                line=dict(width=0.5),
                label=[node['name'] for node in nodes_with_size],
                customdata=[node['percent'] for node in nodes_with_size],
                hovertemplate='Node: %{label}<br>Total Read Count: %{customdata:.3f}%<extra></extra>'
            ),
            link=dict(
                source=links_df['source'],
                target=links_df['target'],
                value=links_df['value']
            )
        )])

        # Update layout
        fig.update_layout(
            font_size=14,
            width=4000,
            height=1000,
            title_x=0.5
        )

        fig.update_layout(
                    title={
                        'y':0.95,
                        'x':0.5,
                        'xanchor': 'center',
                        'yanchor': 'top',
                        'text': f'<b>Sankey Diagram (Top {n_top} abundance)</b>',
                        'font':dict(size=40)},
                    font=dict(size=14))



        # Show the plot
        #fig.show()
        #fig.write_html('sankey_diagram.html')
        return fig