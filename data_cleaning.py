"""
Data cleaning module for the ASPIRES3 Career Uncertainty Analysis project.

This script handles:
- Loading raw ASPIRES3 data
- Replacing missing codes (998, 999) with NaN
- Creating derived variables (CONCERN_R, parent_uni, composites)
- Converting categorical variables to proper types
- Exporting cleaned data for analysis
"""

import pandas as pd
import numpy as np
import os
from pathlib import Path

# =============================================================================
# CONFIGURATION
# =============================================================================

# File paths (adjust these to your actual file locations)
RAW_DATA_PATH = "data/aspires3_data.tab"  # or .csv
CLEAN_DATA_PATH = "data/aspires3_clean.csv"
TABLEAU_EXPORT_PATH = "data/aspires3_tableau_final.csv"

# Columns of interest (based on top correlates and demographics)
PREDICTOR_COLS = [
    'COVID_ASP', 'LIFESAT', 'JOBPER1', 'CONF_FUTJOB', 'JOBPER7',
    'RIGHT_DEC_WORK', 'JOBPER5', 'JOBPER4', 'NO_CAR_RES_05', 'PREV_PG_02',
    'BROAD', 'NO_CAR_RES_01', 'NO_CAR_RES_03', 'BELONG', 'JOBPER2',
    'CAR_SAT_EMP', 'GAD1', 'GAD2', 'PHQ1', 'PHQ2'
]

DEMOGRAPHIC_COLS = ['GENDER', 'ETH', 'REGION', 'PAR1UNI', 'PAR2UNI']


# =============================================================================
# LOADING FUNCTIONS
# =============================================================================

def load_raw_data(filepath):
    """
    Load the raw ASPIRES3 data file.
    
    Parameters:
    -----------
    filepath : str
        Path to the data file (.tab or .csv)
    
    Returns:
    --------
    pd.DataFrame
        Raw data with missing codes not yet replaced
    """
    print(f"Loading data from {filepath}...")
    
    # Determine file extension and load accordingly
    ext = os.path.splitext(filepath)[1].lower()
    
    if ext == '.tab':
        df = pd.read_table(filepath)
    elif ext == '.csv':
        df = pd.read_csv(filepath)
    else:
        raise ValueError(f"Unsupported file format: {ext}")
    
    print(f"Loaded {df.shape[0]} rows, {df.shape[1]} columns")
    return df


# =============================================================================
# CLEANING FUNCTIONS
# =============================================================================

def replace_missing_codes(df, codes=[998, 999]):
    """
    Replace missing value codes with NaN.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Dataframe to clean
    codes : list
        List of numeric codes representing missing values
    
    Returns:
    --------
    pd.DataFrame
        Dataframe with missing codes replaced by NaN
    """
    print(f"Replacing missing codes {codes} with NaN...")
    df_clean = df.replace(codes, np.nan)
    return df_clean


def create_derived_variables(df):
    """
    Create derived variables needed for analysis.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Dataframe with missing codes already replaced
    
    Returns:
    --------
    pd.DataFrame
        Dataframe with additional derived columns
    """
    print("Creating derived variables...")
    
    # Reverse-code CONCERN so higher = more concern
    if 'CONCERN' in df.columns:
        df['CONCERN_R'] = 6 - df['CONCERN']
        print("  - Created CONCERN_R (reverse-coded concern)")
    
    # Parent university attendance (binary)
    if 'PAR1UNI' in df.columns and 'PAR2UNI' in df.columns:
        # Convert to numeric if categorical
        for col in ['PAR1UNI', 'PAR2UNI']:
            if pd.api.types.is_categorical_dtype(df[col]):
                df[col + '_num'] = df[col].cat.codes.replace(-1, np.nan)
            else:
                df[col + '_num'] = df[col]
        
        # Create binary flag (1 if either parent attended)
        df['parent_uni'] = ((df['PAR1UNI_num'] == 1) | (df['PAR2UNI_num'] == 1)).astype(float)
        df['parent_uni'] = df['parent_uni'].replace(0, np.nan)  # where both missing
        print("  - Created parent_uni (binary parental university attendance)")
    
    return df


def convert_to_numeric(df, columns):
    """
    Convert categorical columns to numeric codes.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Dataframe to process
    columns : list
        List of column names to convert (if categorical)
    
    Returns:
    --------
    pd.DataFrame
        Dataframe with _num versions of specified columns
    """
    print("Converting categorical columns to numeric...")
    
    for col in columns:
        if col in df.columns:
            if pd.api.types.is_categorical_dtype(df[col]):
                df[col + '_num'] = df[col].cat.codes.replace(-1, np.nan)
                print(f"  - Created {col}_num from categorical")
            elif pd.api.types.is_numeric_dtype(df[col]):
                # Already numeric, just create a copy for consistency
                df[col + '_num'] = df[col]
                print(f"  - Copied {col} to {col}_num")
    
    return df


def create_composites(df):
    """
    Create composite variables from related items.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Dataframe with numeric versions of items
    
    Returns:
    --------
    pd.DataFrame
        Dataframe with composite variables added
    """
    print("Creating composite variables...")
    
    # Mental health composite (PHQ2 + GAD2 items)
    mental_items = ['PHQ1_num', 'PHQ2_num', 'GAD1_num', 'GAD2_num']
    available_items = [col for col in mental_items if col in df.columns]
    
    if len(available_items) >= 2:
        # Only create composite for rows with all items present
        df_mental = df[available_items].copy()
        df['mental_health'] = df_mental.mean(axis=1)
        print(f"  - Created mental_health composite from {available_items}")
        
        # Calculate Cronbach's alpha for documentation
        try:
            from pingouin import cronbach_alpha
            alpha = cronbach_alpha(df_mental.dropna())
            print(f"    Cronbach's alpha = {alpha[0]:.3f}")
        except:
            pass
    
    # Job perception composite (JOBPER1, JOBPER5, JOBPER4)
    job_items = ['JOBPER1_num', 'JOBPER5_num', 'JOBPER4_num']
    available_job = [col for col in job_items if col in df.columns]
    
    if len(available_job) >= 2:
        df_job = df[available_job].copy()
        df['job_perception'] = df_job.mean(axis=1)
        print(f"  - Created job_perception composite from {available_job}")
        
        # Calculate Cronbach's alpha
        try:
            from pingouin import cronbach_alpha
            alpha = cronbach_alpha(df_job.dropna())
            print(f"    Cronbach's alpha = {alpha[0]:.3f}")
        except:
            pass
    
    return df


# =============================================================================
# SUBSETTING FUNCTIONS
# =============================================================================

def select_columns(df, columns):
    """
    Select only specified columns, ignoring any that don't exist.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Source dataframe
    columns : list
        List of column names to keep
    
    Returns:
    --------
    pd.DataFrame
        Dataframe with only existing columns from the list
    """
    existing = [col for col in columns if col in df.columns]
    print(f"Selecting {len(existing)} of {len(columns)} requested columns")
    return df[existing].copy()


def prepare_tableau_export(df, final_predictors, demographic_cols, outcome='CONCERN_R'):
    """
    Prepare a clean dataset for Tableau visualization.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Cleaned dataframe
    final_predictors : list
        List of predictor column names
    demographic_cols : list
        List of demographic column names
    outcome : str
        Name of outcome variable
    
    Returns:
    --------
    pd.DataFrame
        Dataframe with complete cases on all columns
    """
    all_cols = final_predictors + [outcome] + demographic_cols
    existing = [col for col in all_cols if col in df.columns]
    
    df_export = df[existing].dropna()
    print(f"Tableau export: {df_export.shape[0]} rows, {df_export.shape[1]} columns")
    
    return df_export


# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def save_dataframe(df, filepath):
    """
    Save dataframe to CSV.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Dataframe to save
    filepath : str
        Output file path
    """
    # Create directory if it doesn't exist
    Path(os.path.dirname(filepath)).mkdir(parents=True, exist_ok=True)
    
    df.to_csv(filepath, index=False)
    print(f"Saved to {filepath}")


def check_missing(df, columns=None):
    """
    Print missing value summary for specified columns.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Dataframe to check
    columns : list, optional
        Columns to check; if None, check all
    """
    if columns is None:
        columns = df.columns
    
    missing = df[columns].isna().sum()
    missing_pct = (missing / len(df)) * 100
    
    summary = pd.DataFrame({
        'Missing': missing,
        'Percent': missing_pct
    }).sort_values('Missing', ascending=False)
    
    print("\nMissing value summary:")
    print(summary[summary['Missing'] > 0].head(20))


# =============================================================================
# MAIN PIPELINE
# =============================================================================

def run_cleaning_pipeline(raw_path, clean_path=None, tableau_path=None):
    """
    Run the complete data cleaning pipeline.
    
    Parameters:
    -----------
    raw_path : str
        Path to raw data file
    clean_path : str, optional
        Path to save cleaned data
    tableau_path : str, optional
        Path to save Tableau export
    
    Returns:
    --------
    pd.DataFrame
        Cleaned dataframe
    """
    print("=" * 60)
    print("ASPIRES3 DATA CLEANING PIPELINE")
    print("=" * 60)
    
    # Step 1: Load raw data
    df = load_raw_data(raw_path)
    
    # Step 2: Replace missing codes
    df = replace_missing_codes(df)
    
    # Step 3: Create derived variables
    df = create_derived_variables(df)
    
    # Step 4: Convert key columns to numeric
    all_cols = PREDICTOR_COLS + DEMOGRAPHIC_COLS + ['CONCERN']
    all_cols = list(set(all_cols))  # remove duplicates
    df = convert_to_numeric(df, all_cols)
    
    # Step 5: Create composites
    df = create_composites(df)
    
    # Step 6: Check missing values
    check_missing(df, PREDICTOR_COLS + DEMOGRAPHIC_COLS + ['CONCERN_R', 'mental_health', 'job_perception'])
    
    # Step 7: Save cleaned data
    if clean_path:
        save_dataframe(df, clean_path)
    
    # Step 8: Prepare Tableau export (if requested)
    if tableau_path:
        final_predictors = [
            'COVID_ASP_num', 'LIFESAT_num', 'job_perception', 'CONF_FUTJOB_num',
            'JOBPER7_num', 'RIGHT_DEC_WORK_num', 'JOBPER5_num', 'NO_CAR_RES_05',
            'PREV_PG_02', 'BROAD_num', 'NO_CAR_RES_01', 'NO_CAR_RES_03', 'mental_health'
        ]
        demo = ['GENDER', 'parent_uni', 'REGION', 'ETH']
        
        df_tableau = prepare_tableau_export(df, final_predictors, demo, 'CONCERN_R')
        save_dataframe(df_tableau, tableau_path)
    
    print("\n" + "=" * 60)
    print("CLEANING COMPLETE")
    print("=" * 60)
    
    return df


# =============================================================================
# SCRIPT EXECUTION
# =============================================================================

if __name__ == "__main__":
    # Run the pipeline (adjust paths as needed)
    df_clean = run_cleaning_pipeline(
        raw_path="data/aspires3_data.tab",
        clean_path="data/aspires3_clean.csv",
        tableau_path="data/aspires3_tableau_final.csv"
    )
    
    print("\nFirst 5 rows of cleaned data:")
    print(df_clean.head())
