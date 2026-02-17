"""
Data Loading and Preprocessing Utilities
"""
import pandas as pd
import numpy as np

print("__name__ is:", __name__, "\n")

def load_hcc_data(path = "../data/hcc-data.csv",
                  standardize_names = True,
                  convert_types = True,
                  verbose = True):
    """Load HCC dataset with fixes for idetified issues from data inspection."""

    df = pd.read_csv(path, na_values = ["?"])

    if standardize_names:
        rename_dict = {
            "Nodule": "Nodules"
        }

        df1 = df.rename(columns = rename_dict)
        if verbose and any(k in df.columns for k, v in rename_dict.items()):
            print(f"Renamed columns: {', '.join([k for k in rename_dict.keys() if k in df.columns])} to {", ".join([v for k, v in rename_dict.items() if k in df.columns])}")
            print()

        if convert_types:
            df2 = convert_data_types(df1)
            if verbose:
                print(f"Data types converted: ")
                print(f"    - Categorical: {len(df2.select_dtypes(include = "category").columns)} features, including target variable")
                print(f"    - Numeric: {len(df2.select_dtypes(include = "number").columns)} features")
                print()
            
        if verbose:
            print(f"Data loaded: {df2.shape[0]} rows, {df2.shape[1]} columns")

        return df2


def convert_data_types(df):
    """Fix data type issues identified during data inspection."""

    # Binary categorical features that are stored as numeric
    binary_features = ["Gender", "Symptoms", "Alcohol", "HBsAg", "HBeAg", "HBcAb", "HCVAb",
                   "Cirrhosis", "Endemic", "Smoking", "Diabetes", "Obesity", "Hemochro",
                   "AHT", "CRI", "HIV", "NASH", "Varices", "Spleno", "PHT", "PVT", "Metastasis",
                   "Hallmark", "Class"]
    
    for col in binary_features:
        if col in df.columns:
            df[col] = df[col].astype('category')
        else:
            print(f"Warning: Column '{col}' not found in data for type conversion.")
    
    # Ordinal feature conversion
    for col in ["PS", "Encephalopathy", "Ascites"]:
        if col in df.columns:
            df[col] = pd.Categorical(df[col], ordered = True)
        else:
            print(f"Warning: Column '{col}' not found in data for type conversion.")
    
    for col in ["Age", "Nodules"]:
        if col in df.columns:
            df[col] = df[col].astype("Int64") # Use Int64 to allow for missing values
        else:
            print(f"Warning: Column '{col}' not found in data for type conversion.")

    return df

def get_feature_groups():
    """
    Return dictionary of feature groups based on domain knowledge and data inspection.

    Returns:
        dict: Feature groups categorized by clinical relevance.
    """

    return {
        "demographics": ["Age", "Gender"],

        "viral_hepatitis_markers": ["HBsAg", "HBeAg", "HBcAb", "HCVAb"],

        "risk_factors": ["Cirrhosis", "Alcohol", "Grams_day", "Smoking",
                         "Packs_year", "Endemic"],

        "comorbidities": ["Diabetes", "Obesity", "Hemochro", "AHT", "CRI", "HIV", "NASH"],

        "tumour_charactersitics": ["Nodules", "Size", "Metastasis", "Hallmark", "AFP"],

        "liver_function": ["Total_Bil", "Dir_Bil", "Albumin", "INR", "ALT", "AST", "GGT", 
                           "ALP", "TP", "Creatinine"],

        "disease_severity": ["PS", "Encephalopathy", "Ascites", "Symptoms"],

        "complicatons": ["Varices", "Spleno", "PHT", "PVT"],

        "hematology": ["Hemoglobin", "MCV", "Leucocytes", "Platelets"],

        "other_labs": ["Iron", "Ferritin", "Sat"],

        "target": ["Class"]
    }

def get_binary_features():
    """
    Return list of binary (0/1) categorical features.
    
    Returns:
        list: Column names of binary features including the target variable.
    """

    return [
        "Gender", "Symptoms", "Alcohol", "HBsAg", "HBeAg", "HBcAb", "HCVAb",
        "Cirrhosis", "Endemic", "Smoking", "Diabetes", "Obesity", "Hemochro",
        "AHT", "CRI", "HIV", "NASH", "Varices", "Spleno", "PHT", "PVT", "Metastasis",
        "Hallmark", "Class"
    ]

def get_continuous_features():
    """
    Return list of continuous numeric features.
    
    Returns:
        list: Column names of continuous features
    """

    return [
        "Age", "Grams_day", "Packs_year", "INR", "AFP", "Hemoglobin", "MCV", "Leucocytes",
        "Platelets", "Albumin", "Total_Bil", "ALT", "AST", "GGT", "GGT", "ALP", "Creatinine",
        "Nodules", "Major_Dim", "Dir_Bil", "Iron", "Sat", "Ferritin"
    ]

def get_ordinal_features():
    """
    Return dictionary of ordinal features with their valid ranges.
    
    Returns:
        dict: {feature_name: (min_value, max_value, description)}
    """

    return {
        "PS": (0, 4, "Performance Status: 0 = Active, 1 = Restricted, 2 = Ambulatory, 3 = Selfcare, 4 = Disabled"),
        "Encephalopathy": (1, 3, "Encephalopathy degree: 1 = None, 2 = Grade I/II, 3 = Grade III/IV"),
        "Ascites": (1, 3, "Ascites degree: 1= None, 2 = Mild, 3 = Moderate / Severe")
    }

def get_numeric_features(df):
    """
    Get list of truly numeric features (excluding categorical).
    
    Args:
        df: DataFrame (after type conversion)
    
    Returns:
        list: Numeric column names
    """

    return df.select_dtypes(include = "number").columns.tolist()

def get_categorical_features(df):
    """
    Get list of categorical features.
    
    Args:
        df: DataFrame (after type conversion)
    
    Returns:
        list: Categorical column names
    """

    return df.select_dtypes(include = "category").columns.tolist()

def print_data_summary(df):
    """
    Print a quick summary of the dataset after loading and type conversion.
    
    Args:
        df (pd.DataFrame): Dataset to summarize
    """

    print("=" * 60)
    print("DATASET SUMMARY")
    print("=" * 60)

    print(f"Shape: {df.shape[0]} rows x {df.shape[1]} columns")
    print(f"Memory: {df.memory_usage(deep = True).sum() / 1024:.2f} KB")

    # Data types
    categorical_cols = df.select_dtypes(include = "category").columns
    numeric_cols = df.select_dtypes(include = "number").columns

    print(f"\nData Types:")
    print(f"\nCategorical: {len(categorical_cols)} features, \n{list(categorical_cols)}")
    print(f"\nNumeric: {len(numeric_cols)} features, \n{list(numeric_cols)}")

    # Missing data summary
    missing_counts = df.isnull().sum().sum()
    missing_pct = (missing_counts / (df.shape[0] * df.shape[1] - df.shape[0])) * 100 # Exclude target variable from denominator
    print(f"\nMissing Data: {missing_counts} total missing values ({missing_pct:.2f}%)")

    # Target variable distribution
    if "Class" in df.columns:
        class_counts = df["Class"].value_counts().sort_index()
        print(f"\nTarget Variable Distribution (Class):")
        print(f"    Dies (0): {class_counts[0]} ({class_counts[0] / len(df) * 100:.1f}%)")
        print(f"    Lives (1): {class_counts[1]} ({class_counts[1] / len(df) * 100:.1f}%)")

    print("=" * 60)

if __name__ == "__main__":
    print("Testing data_utils.py...\n")

    # Test loading
    df = load_hcc_data()
    print_data_summary(df)

    # Test feature group retrieval
    groups = get_feature_groups()
    print(f"\nFeature groups defined: {list(groups.keys())}")
    print()

    print("All functions working as expected.")