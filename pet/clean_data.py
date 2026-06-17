"""
STEP 2: DATA CLEANING & FEATURE ENGINEERING
============================================
This script cleans the raw dog adoption data and creates dogs_cleaned.csv

INPUT:  dogs_raw.csv (600 rows, 12 columns)
OUTPUT: dogs_cleaned.csv (cleaned data with new features)

CLEANING TASKS:
1. Standardize breed names
2. Create age_group from age
3. Calculate days_listed
4. Handle missing values
5. Standardize city/state names
6. Clean gender and size values
"""

import pandas as pd
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

print("=" * 70)
print("🧹 STEP 2: DATA CLEANING & FEATURE ENGINEERING")
print("=" * 70)

# ============================================================================
# LOAD RAW DATA
# ============================================================================
print("\n📂 Loading dogs_raw.csv...")

try:
    df_raw = pd.read_csv('dogs_raw.csv')
    print(f"✅ Loaded {len(df_raw)} records with {len(df_raw.columns)} columns")
    print(f"\nColumns: {list(df_raw.columns)}")
except FileNotFoundError:
    print("❌ ERROR: dogs_raw.csv not found!")
    print("Please ensure dogs_raw.csv is in the same directory.")
    exit()

print("\n" + "=" * 70)
print("📊 RAW DATA SUMMARY")
print("=" * 70)
print(df_raw.info())
print("\n🔍 Missing Values:")
print(df_raw.isnull().sum())

# ============================================================================
# DATA CLEANING FUNCTIONS
# ============================================================================

def clean_breed(breed_primary, breed_secondary):
    """
    Combine primary and secondary breed into single breed field
    """
    if pd.isna(breed_primary):
        return 'Unknown'
    
    breed = str(breed_primary).strip()
    
    # If secondary breed exists and is not 'Mixed' or 'Unknown'
    if pd.notna(breed_secondary) and breed_secondary not in ['Mixed Breed', 'Mixed', 'Unknown', None]:
        breed = f"{breed} Mix"
    
    # Standardize common variations
    breed = breed.replace('Indie', 'Indian Pariah Dog')
    
    return breed

def create_age_group(age):
    """
    Create age groups from age field
    """
    if pd.isna(age):
        return 'Unknown'
    
    age = str(age).strip().lower()
    
    if 'puppy' in age or 'pup' in age:
        return 'Puppy'
    elif 'young' in age or 'junior' in age:
        return 'Young'
    elif 'senior' in age or 'old' in age:
        return 'Senior'
    elif 'adult' in age:
        return 'Adult'
    else:
        return 'Adult'  # Default

def calculate_days_listed(published_at, status):
    """
    Calculate how many days the dog has been/was listed
    """
    try:
        # Parse published date
        if pd.isna(published_at):
            return np.nan
        
        published = pd.to_datetime(published_at)
        current = datetime.now()
        
        # Calculate days
        days = (current - published).days
        
        # Ensure non-negative
        return max(0, days)
        
    except:
        return np.nan

def clean_text_field(value):
    """
    Clean and standardize text fields
    """
    if pd.isna(value):
        return None
    return str(value).strip().title()

# ============================================================================
# STEP-BY-STEP CLEANING
# ============================================================================

print("\n" + "=" * 70)
print("🔧 CLEANING OPERATIONS")
print("=" * 70)

# Create cleaned dataframe
df_cleaned = df_raw.copy()

# 1. Combine and clean breed
print("\n1️⃣  Cleaning breed information...")
df_cleaned['breed'] = df_cleaned.apply(
    lambda row: clean_breed(row['breed_primary'], row['breed_secondary']), 
    axis=1
)
print(f"   ✅ Created 'breed' column")
print(f"   📊 Unique breeds: {df_cleaned['breed'].nunique()}")

# 2. Create age_group
print("\n2️⃣  Creating age groups...")
df_cleaned['age_group'] = df_cleaned['age'].apply(create_age_group)
print(f"   ✅ Created 'age_group' column")
print(f"   📊 Age group distribution:")
print(f"      {df_cleaned['age_group'].value_counts().to_dict()}")

# 3. Calculate days_listed
print("\n3️⃣  Calculating days listed...")
df_cleaned['days_listed'] = df_cleaned.apply(
    lambda row: calculate_days_listed(row['published_at'], row['status']), 
    axis=1
)
print(f"   ✅ Created 'days_listed' column")
print(f"   📊 Average days listed: {df_cleaned['days_listed'].mean():.1f} days")

# 4. Standardize size
print("\n4️⃣  Standardizing size values...")
df_cleaned['size'] = df_cleaned['size'].apply(clean_text_field)
# Fill missing with 'Medium' (most common)
df_cleaned['size'].fillna('Medium', inplace=True)
print(f"   ✅ Size standardized")
print(f"   📊 Size distribution: {df_cleaned['size'].value_counts().to_dict()}")

# 5. Standardize gender
print("\n5️⃣  Standardizing gender values...")
df_cleaned['gender'] = df_cleaned['gender'].apply(clean_text_field)
# Fill missing with random Male/Female
missing_gender = df_cleaned['gender'].isna()
if missing_gender.sum() > 0:
    df_cleaned.loc[missing_gender, 'gender'] = np.random.choice(['Male', 'Female'], size=missing_gender.sum())
print(f"   ✅ Gender standardized")
print(f"   📊 Gender distribution: {df_cleaned['gender'].value_counts().to_dict()}")

# 6. Clean city and state names
print("\n6️⃣  Cleaning location data...")
df_cleaned['city'] = df_cleaned['city'].apply(clean_text_field)
df_cleaned['state'] = df_cleaned['state'].apply(clean_text_field)
print(f"   ✅ Location data cleaned")
print(f"   📊 Cities: {df_cleaned['city'].nunique()}, States: {df_cleaned['state'].nunique()}")

# 7. Standardize status
print("\n7️⃣  Standardizing status values...")
df_cleaned['status'] = df_cleaned['status'].apply(clean_text_field)
print(f"   ✅ Status standardized")
print(f"   📊 Status distribution: {df_cleaned['status'].value_counts().to_dict()}")

# ============================================================================
# SELECT FINAL COLUMNS (as per dogs_cleaned table design)
# ============================================================================

print("\n" + "=" * 70)
print("📋 CREATING FINAL CLEANED TABLE")
print("=" * 70)

# Select only required columns for dogs_cleaned
final_columns = [
    'dog_id',
    'breed',
    'age_group',
    'size',
    'gender',
    'city',
    'state',
    'days_listed',
    'status'
]

df_final = df_cleaned[final_columns].copy()

# ============================================================================
# HANDLE REMAINING MISSING VALUES
# ============================================================================

print("\n🔍 Checking for missing values...")
missing_summary = df_final.isnull().sum()
print(missing_summary[missing_summary > 0])

# Fill any remaining missing values with appropriate defaults
if df_final['breed'].isna().sum() > 0:
    df_final['breed'].fillna('Unknown', inplace=True)

if df_final['age_group'].isna().sum() > 0:
    df_final['age_group'].fillna('Adult', inplace=True)

if df_final['days_listed'].isna().sum() > 0:
    df_final['days_listed'].fillna(df_final['days_listed'].median(), inplace=True)

print("✅ All missing values handled")

# ============================================================================
# DATA QUALITY CHECKS
# ============================================================================

print("\n" + "=" * 70)
print("✅ DATA QUALITY CHECKS")
print("=" * 70)

print(f"\n📊 Final Record Count: {len(df_final)}")
print(f"📊 Final Column Count: {len(df_final.columns)}")
print(f"\n📋 Column Names: {list(df_final.columns)}")

print("\n🔍 Data Types:")
print(df_final.dtypes)

print("\n📈 Summary Statistics:")
print(df_final.describe(include='all'))

# ============================================================================
# SAVE CLEANED DATA
# ============================================================================

print("\n" + "=" * 70)
print("💾 SAVING CLEANED DATA")
print("=" * 70)

output_file = 'dogs_cleaned.csv'
df_final.to_csv(output_file, index=False)

print(f"\n✅ SUCCESS! Created: {output_file}")
print(f"📊 Total Records: {len(df_final)}")
print(f"📊 Total Columns: {len(df_final.columns)}")

# ============================================================================
# FINAL SUMMARY
# ============================================================================

print("\n" + "=" * 70)
print("📊 CLEANED DATA SUMMARY")
print("=" * 70)

print("\n🐕 Top 10 Breeds:")
print(df_final['breed'].value_counts().head(10))

print("\n👶 Age Group Distribution:")
print(df_final['age_group'].value_counts())

print("\n📏 Size Distribution:")
print(df_final['size'].value_counts())

print("\n🚹 Gender Distribution:")
print(df_final['gender'].value_counts())

print("\n🏙️  Top 10 Cities:")
print(df_final['city'].value_counts().head(10))

print("\n📍 State Distribution:")
print(df_final['state'].value_counts())

print("\n📊 Status Distribution:")
print(df_final['status'].value_counts())

print(f"\n⏱️  Days Listed Statistics:")
print(f"   Mean: {df_final['days_listed'].mean():.1f} days")
print(f"   Median: {df_final['days_listed'].median():.1f} days")
print(f"   Min: {df_final['days_listed'].min():.0f} days")
print(f"   Max: {df_final['days_listed'].max():.0f} days")

print("\n" + "=" * 70)
print("🎯 STEP 2: DATA CLEANING - COMPLETED!")
print("=" * 70)

print("\n📄 Preview of cleaned data (first 5 rows):")
print(df_final.head())

print("\n✅ Next Step: Confirm dogs_cleaned.csv looks good")
print("💬 Reply 'Step 2 Done' to proceed to Step 3: Data Analysis")
print("=" * 70)