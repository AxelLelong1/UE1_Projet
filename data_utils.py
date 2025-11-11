from IPython.display import display
import pandas as pd
import numpy as np
import xlrd


hopital_path = "./data/hopital/"
hopital_prefix = 'open_ccam_'
hopital_suffix = '_reg.csv'

liberal_path = "./data/liberal/"
liberal_prefix = '20'
liberal_suffix = '_actes-techniques-ccam_serie-annuelle.xlsx'
liberal_suffix_2 = '_actes-techniques-ccam_serie-annuelle.xls'

# -- IMPORT --

def import_data_hopital(year: str):
    """Import data from a CSV file into a pandas DataFrame."""

    # Construct the file path and read the CSV file
    df = pd.read_csv(f'{hopital_path}{hopital_prefix}{year}{hopital_suffix}', sep=';')

    # Add a 'year' column to the DataFrame
    df['year'] = '20' + year
    df['origin'] = 'hopital'
    return df

def import_data_liberal(year: str):
    """Import data from a CSV file into a pandas DataFrame."""

    # Construct the file path and read the CSV file
    try:
        df = pd.read_excel(f'{liberal_path}{liberal_prefix}{year}{liberal_suffix}', sheet_name=1)
    except:
        df = pd.read_excel(f'{liberal_path}{liberal_prefix}{year}{liberal_suffix_2}', sheet_name=1)

    # Add a 'year' column to the DataFrame
    df['year'] = '20' + year
    df['origin'] = 'liberal'
    return df


# -- DATA CLEANUP --

def data_cleanup(df: pd.DataFrame):
    """Clean up the DataFrame by handling missing values and keeping necessary columns."""

    # Replace '.' with 0
    df.replace('.', 0, inplace=True)

    # Rename column if it exists
    if 'Acte CCAM + phase' in df.columns:
        df.rename(columns={'Acte CCAM + phase': 'acte'}, inplace=True)
    if 'dms_globale' in df.columns:
        df.rename(columns={'dms_globale': 'dms'}, inplace=True)

    # Keep only relevant columns
    relevant_columns = ['acte', 'nb_actes', 'year', 'origin']
    df = df.groupby(['acte', 'year', 'origin'], as_index=False)['nb_actes'].sum()
    df = df[relevant_columns]

    return df

def cleanup_liberal(df: pd.DataFrame):
    """Specific cleanup for liberal data."""
    
    df.rename(columns={'Code Acte': 'acte'}, inplace=True)
    # Add missing 0 at the ned of every acte code
    df['acte'] = df['acte'] + '0'
    
    # Get the column that has Quantité d'actes in it's name
    actes_column = [col for col in df.columns if "Quantité" in col]
    if actes_column:
        df.rename(columns={actes_column[0]: 'nb_actes'}, inplace=True)
    
    relevant_columns = ['acte', 'nb_actes', 'year', 'origin']
    df = df[relevant_columns]
    return df

def merge_dataframes(dfs: list):
    """Merge a list of DataFrames into a single DataFrame."""
    merged_df = pd.concat(dfs, ignore_index=True)
    return merged_df

def keep_actes(df: pd.DataFrame, actes_list: list):
    """Filter the DataFrame to keep only specified actes."""
    filtered_df = df[df['acte'].isin(actes_list)]
    filtered_df.reset_index(drop=True, inplace=True)
    return filtered_df

# -- ANALYSIS --

def get_total_actes(df: pd.DataFrame):
    """Calculate the total number of actes."""
    total_actes = df.groupby('acte')['nb_actes'].sum().reset_index()
    return total_actes

def get_total_actes_per_year(df: pd.DataFrame):
    """Calculate the total number of actes per year."""
    total_per_year = df.groupby(['year', 'acte'])['nb_actes'].sum().reset_index()
    return total_per_year

#def get_total_actes_per_region(df: pd.DataFrame):
#    """Calculate the total number of actes per region."""
#    total_per_region = df.groupby(['reg', 'acte'])['nb_actes'].sum().reset_index()
#    return total_per_region

#def get_total_actes_per_reg_per_year(df: pd.DataFrame):
#    """Calculate the total number of actes per region per year."""
#    total_per_reg_per_year = df.groupby(['reg', 'year', 'acte'])['nb_actes'].sum().reset_index()
#    return total_per_reg_per_year

# -- INIT --

def initialize():
    import_years = ['15', '16', '17', '18', '19', '20', '21', '22', '23']
    actes_to_keep = ['JPHJ0010', 'JPHJ0020', 'JPHB0010', 'JPHB0020'] # maybe 'JQHB0020', 'JQHF0010', 'JQHF0020'

    data_frames_hopitaux = [import_data_hopital(year) for year in import_years]
    data_frames_liberal = [import_data_liberal(year) for year in import_years]

    data_frames_hopitaux_cleaned = [data_cleanup(df) for df in data_frames_hopitaux]
    data_frames_liberal_cleaned = [cleanup_liberal(df) for df in data_frames_liberal]

    merged_data = merge_dataframes(data_frames_hopitaux_cleaned + data_frames_liberal_cleaned)
    merged_data = keep_actes(merged_data, actes_to_keep)

    merged_data.to_excel('./data/merged_data.xlsx', index=False)

    return merged_data