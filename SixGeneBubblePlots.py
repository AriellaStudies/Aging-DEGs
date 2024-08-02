import pandas as pd
import matplotlib.pyplot as plt

# Data dictionary for each gene
genes_data = {
    'SPARC': {
        'Up': [('Liver', 'Mus musculus')],
        'Down': [('Muscle', 'Homo sapiens'), ('Immune', 'Mus musculus'), ('Muscle', 'Mus musculus'), 
                 ('Trachea', 'Mus musculus'), ('Fat', 'Mus musculus'), ('Muscle', 'Mus musculus'), 
                 ('Muscle', 'Canis lupus familiaris'), ('Heart', 'Rattus norvegicus'), ('Fat', 'Rattus norvegicus')]
    },
    'DIRC2': {
        'Up': [],
        'Down': [('Muscle', 'Homo sapiens'), ('Muscle', 'Homo sapiens'), ('Muscle', 'Mus musculus'), 
                 ('Trachea', 'Mus musculus'), ('Fat', 'Mus musculus'), ('Heart', 'Rattus norvegicus'), 
                 ('Liver', 'Rattus norvegicus')]
    },
    'CA4': {
        'Up': [],
        'Down': [('Brain', 'Homo sapiens'), ('Muscle', 'Homo sapiens'), ('Muscle', 'Homo sapiens'), 
                 ('Immune', 'Mus musculus'), ('Liver', 'Mus musculus'), ('Fat', 'Mus musculus'), 
                 ('Brain', 'Mus musculus'), ('Heart', 'Mus musculus')]
    },
    'CDC20': {
        'Up': [],
        'Down': [('Immune', 'Mus musculus'), ('Muscle', 'Mus musculus'), ('Liver', 'Mus musculus'), 
                 ('Immune', 'Mus musculus'), ('Brain', 'Mus musculus'), ('Muscle', 'Mus musculus'), 
                 ('Liver', 'Rattus norvegicus')]
    },
    'RSRC1': {
        'Up': [('Brain', 'Homo sapiens'), ('Muscle', 'Homo sapiens'), ('Fat', 'Mus musculus'), 
               ('Brain', 'Mus musculus'), ('Brain', 'Mus musculus'), ('Fat', 'Rattus norvegicus'), 
               ('Liver', 'Rattus norvegicus')],
        'Down': []
    },
    'CASP1': {
        'Up': [('Muscle', 'Homo sapiens'), ('Trachea', 'Mus musculus'), ('Cochlea', 'Mus musculus'), 
               ('Fat', 'Mus musculus'), ('Heart', 'Rattus norvegicus'), ('Fat', 'Rattus norvegicus'), 
               ('Liver', 'Rattus norvegicus')],
        'Down': []
    }
}

# Define specific order for animal species and tissues (reversed)
animal_order = ['Mus musculus', 'Homo sapiens', 'Rattus norvegicus', 'Canis lupus familiaris']
tissue_order = ['Cochlea', 'Trachea', 'Reproductive', 'Muscle', 'Liver', 'Immune', 'Heart', 'Fat', 'Brain']

# Function to plot data for each gene
def plot_gene_data(gene_name, data):
    df = pd.DataFrame([
        {'Tissue': tissue, 'Animal': animal, 'Regulation': 'Up'} for tissue, animal in data['Up']
    ] + [
        {'Tissue': tissue, 'Animal': animal, 'Regulation': 'Down'} for tissue, animal in data['Down']
    ])
    
    # Create a complete grid of Animal x Tissue to ensure all combinations are present
    grid = pd.MultiIndex.from_product([animal_order, tissue_order], names=['Animal', 'Tissue'])
    pivot_table = df.pivot_table(index=['Animal', 'Tissue'], columns='Regulation', aggfunc='size', fill_value=0)
    pivot_table = pivot_table.reindex(grid, fill_value=0)  # Reindex to include all possible combinations

    # Reset index for plotting
    pivot_table.reset_index(inplace=True)
    pivot_table.columns.name = None  # Clean up the columns name to remove 'Regulation'

    # Plotting with adjusted figure size and margins
    fig, ax = plt.subplots(figsize=(6, 10))  # Adjusted figure size

    # Bubble size factor
    size_factor = 100

    for _, row in pivot_table.iterrows():
        color = 'red' if row.get('Up', 0) > 0 else 'blue'
        size = (row.get('Up', 0) + row.get('Down', 0)) * size_factor
        ax.scatter(row['Animal'], row['Tissue'], s=size, color=color, alpha=0.7, edgecolors='black', linewidth=1.5, marker='o')

    ax.set_xlabel('Animal Species')
    ax.set_ylabel('Tissue Type')
    ax.set_title(f'Gene Expression Regulation for {gene_name}')
    plt.xticks(rotation=45)
    plt.yticks(rotation=45)
    plt.grid(True, linestyle='--', alpha=0.6)

    plt.subplots_adjust(left=0.15, bottom=0.2)  # Adjust left and bottom margins

    plt.savefig(f'tissues{gene_name}.svg', format='svg')  # Save the figure as SVG
    plt.show()

# Generate plots for each gene
for gene_name, data in genes_data.items():
    plot_gene_data(gene_name, data)
