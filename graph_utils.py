from data_utils import *
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt

def plot_actes(df : pd.DataFrame):
    """Plot the total number of actes for each acte type."""

    # Taking necessairy data
    total_actes = get_total_actes(df)

    # Create the bar plot
    bars = plt.bar(total_actes['acte'], 
                   total_actes['nb_actes'], 
                   color='skyblue', 
                   edgecolor='black', 
                   linewidth=0.8)

    # Adding value labels on top of each bar
    for bar in bars:

        # Get height of the bar
        height = bar.get_height()

        # Position the text label
        plt.text(bar.get_x() + bar.get_width() / 2, 
                 height, 
                 f'{int(height)}', # Transform 1,000 to 1000
                 ha='center', 
                 va='bottom', 
                 fontsize=8)
    
    # Title and labels
    plt.title("Nombre total d'actes par type", fontsize=14, fontweight='bold', pad=15)
    plt.xlabel("Type d'acte (CCAM)", fontsize=12)
    plt.ylabel("Nombre total d'actes", fontsize=12)
    plt.xticks(fontsize=10)
    plt.yticks(fontsize=10)
    plt.grid(axis='y', linestyle='--', alpha=0.6)

    #plt.tight_layout()
    plt.show()

def plot_global_acte_per_year(df: pd.DataFrame):
    """Plot the total number of actes per year."""
    total_per_year = df.groupby('year')['nb_actes'].sum().reset_index()

    plt.figure(figsize=(10, 6))
    bars = plt.bar(total_per_year['year'], total_per_year['nb_actes'], color='skyblue', edgecolor='black', linewidth=0.8)
    # Adding value labels on top of each bar
    for bar in bars:

        # Get height of the bar
        height = bar.get_height()

        # Position the text label
        plt.text(bar.get_x() + bar.get_width() / 2, 
                 height, 
                 f'{int(height)}', # Transform 1,000 to 1000
                 ha='center', 
                 va='bottom', 
                 fontsize=8)
        
    plt.title("Nombre total d'actes par année", fontsize=14, fontweight='bold', pad=15)
    
    plt.xlabel("Année", fontsize=12)
    plt.ylabel("Nombre total d'actes", fontsize=12)
    
    plt.xticks(fontsize=10)
    plt.yticks(fontsize=10)
    
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.show()

def plot_stacked_acte_per_year(df: pd.DataFrame):
    """Plot stacked bar chart of number of actes per year per acte type."""

    # Group by year and acte
    summary = df.groupby(['year', 'acte'])['nb_actes'].sum().reset_index()

    # Pivot for stacked bars
    pivot_df = summary.pivot(index='year', columns='acte', values='nb_actes').fillna(0)

    # Colors (one per acte)
    colors = plt.cm.tab20.colors  # up to 20 actes, adjust if needed

    # Plot stacked bars
    ax = pivot_df.plot(kind='bar', stacked=True, figsize=(12, 6), color=colors, edgecolor='black', linewidth=0.8)
    year_totals = pivot_df.sum(axis=1)

    # Add value labels on each segment
    for p in ax.patches:
        height = p.get_height()
        if height > 0:  # only label non-zero segments
             # Find the year index based on bar position
            year_idx = int(p.get_x() + p.get_width() / 2)
            # Get corresponding year total
            year_label = pivot_df.index[year_idx]
            total = year_totals.loc[year_label]
            # Compute percentage
            percentage = (height / total) * 100 if total > 0 else 0

            ax.text(p.get_x() + p.get_width()/2, 
                    p.get_y() + height/2,
                    f'{percentage:.1f}%',
                    ha='center',
                    va='center',
                    fontsize=8,
                    color='white')
    
    plt.title("Nombre d'actes par année et par type d'acte", fontsize=14, fontweight='bold', pad=15)
    plt.xlabel("Année", fontsize=12)
    plt.ylabel("Nombre d'actes", fontsize=12)
    plt.xticks(fontsize=10)
    plt.yticks(fontsize=10)
    plt.grid(True, linestyle='--', alpha=0.4)
    plt.legend(title='Acte', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.show()


def plot_actes_per_year(df : pd.DataFrame):
    """Plot the total number of actes for each acte type per year."""
    
    data = get_total_actes_per_year(df)

    # Group actes into high and low categories
    high_actes = ['JPHB0020', 'JPHJ0020']  
    low_actes = ['JPHB0010', 'JPHJ0010']

     # -- Palette de couleurs --
    actes = data['acte'].unique()
    cmap = plt.cm.get_cmap('tab10', len(actes))
    color_dict = {acte: cmap(i) for i, acte in enumerate(actes)}

    # two subplots
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    plt.style.use('ggplot')

    # Graph1: High volume actes
    for acte in high_actes:
        acte_data = data[data['acte'] == acte]
        axes[0].plot(
            acte_data['year'],
            acte_data['nb_actes'],
            marker='o',
            linewidth=2,
            color=color_dict.get(acte, 'gray'),
            label=acte
        )

    axes[0].set_title("Actes à volume élevé", fontsize=13, fontweight='bold')
    axes[0].set_xlabel("Année")
    axes[0].set_ylabel("Nombre d'actes")
    axes[0].grid(True, linestyle='--', alpha=0.7)
    axes[0].legend(title="Acte")

    # Graph2: low volume actes
    for acte in low_actes:
        acte_data = data[data['acte'] == acte]
        axes[1].plot(
            acte_data['year'],
            acte_data['nb_actes'],
            marker='o',
            linewidth=2,
            color=color_dict.get(acte, 'gray'),
            label=acte
        )

    axes[1].set_title("Actes à volume faible", fontsize=13, fontweight='bold')
    axes[1].set_xlabel("Année")
    axes[1].grid(True, linestyle='--', alpha=0.7)
    axes[1].legend(title="Acte")

    plt.suptitle("Évolution du nombre d'actes par année", fontsize=15, fontweight='bold')
    plt.show()