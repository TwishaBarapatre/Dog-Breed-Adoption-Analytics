"""
STEP 3: DATA ANALYSIS & STATISTICS
===================================
This script analyzes cleaned dog adoption data and creates analytics tables

INPUT:  dogs_cleaned.csv (600 rows, 9 columns)
OUTPUT: 
  - breed_adoption_stats.csv (breed-wise analytics)
  - location_adoption_stats.csv (location-wise analytics)

ANALYSIS:
1. Breed Adoption Speed Analysis
2. Location-Wise Adoption Patterns
3. Fast vs Slow Adoption Scoring
"""

import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

print("=" * 70)
print("📊 STEP 3: DATA ANALYSIS & STATISTICS")
print("=" * 70)

# ============================================================================
# LOAD CLEANED DATA
# ============================================================================
print("\n📂 Loading dogs_cleaned.csv...")

try:
    df = pd.read_csv('dogs_cleaned.csv')
    print(f"✅ Loaded {len(df)} records with {len(df.columns)} columns")
    print(f"\nColumns: {list(df.columns)}")
except FileNotFoundError:
    print("❌ ERROR: dogs_cleaned.csv not found!")
    print("Please ensure dogs_cleaned.csv is in the same directory.")
    exit()

print("\n" + "=" * 70)
print("📊 DATA OVERVIEW")
print("=" * 70)
print(df.info())

# ============================================================================
# ANALYSIS 1: BREED ADOPTION STATISTICS
# ============================================================================

print("\n" + "=" * 70)
print("🐕 ANALYSIS 1: BREED ADOPTION STATISTICS")
print("=" * 70)

# Group by breed
breed_stats = df.groupby('breed').agg({
    'dog_id': 'count',  # Total listings
    'days_listed': 'mean',  # Average days to adopt
    'status': lambda x: (x == 'Adopted').sum()  # Count of adopted
}).reset_index()

# Rename columns
breed_stats.columns = ['breed', 'total_listings', 'avg_days_to_adopt', 'adopted_count']

# Round average days
breed_stats['avg_days_to_adopt'] = breed_stats['avg_days_to_adopt'].round(1)

# Calculate fast adoption score
# Logic: Fast adoption = high adoption rate + low avg days
# Score = (adoption_rate * 100) - (avg_days / 10)
breed_stats['adoption_rate'] = (breed_stats['adopted_count'] / breed_stats['total_listings'] * 100).round(1)

# Fast Adoption Score (higher is better)
# Fast = adopted quickly (low days) AND high adoption rate
breed_stats['fast_adoption_score'] = (
    (breed_stats['adoption_rate'] / 100 * 50) +  # 50% weight to adoption rate
    ((365 - breed_stats['avg_days_to_adopt']) / 365 * 50)  # 50% weight to speed
).round(2)

# Slow Adoption Score (higher means slower)
# Slow = took longer days OR low adoption rate
breed_stats['slow_adoption_score'] = (
    ((100 - breed_stats['adoption_rate']) / 100 * 50) +  # 50% weight to low adoption
    (breed_stats['avg_days_to_adopt'] / 365 * 50)  # 50% weight to time
).round(2)

# Select final columns for breed_adoption_stats table
breed_final = breed_stats[[
    'breed',
    'total_listings',
    'avg_days_to_adopt',
    'fast_adoption_score',
    'slow_adoption_score'
]].copy()

# Sort by total listings (descending)
breed_final = breed_final.sort_values('total_listings', ascending=False)

print(f"\n✅ Analyzed {len(breed_final)} unique breeds")
print(f"\n📊 Top 10 Breeds by Total Listings:")
print(breed_final.head(10).to_string(index=False))

print(f"\n🚀 Top 5 FASTEST Adopted Breeds:")
top_fast = breed_final.nlargest(5, 'fast_adoption_score')[['breed', 'avg_days_to_adopt', 'fast_adoption_score']]
print(top_fast.to_string(index=False))

print(f"\n🐌 Top 5 SLOWEST Adopted Breeds:")
top_slow = breed_final.nlargest(5, 'slow_adoption_score')[['breed', 'avg_days_to_adopt', 'slow_adoption_score']]
print(top_slow.to_string(index=False))

# ============================================================================
# ANALYSIS 2: LOCATION ADOPTION STATISTICS
# ============================================================================

print("\n" + "=" * 70)
print("📍 ANALYSIS 2: LOCATION ADOPTION STATISTICS")
print("=" * 70)

# Group by state and city
location_stats = df.groupby(['state', 'city']).agg({
    'dog_id': 'count',  # Total listings
    'days_listed': 'mean',  # Average days listed
    'status': lambda x: (x == 'Adopted').sum()  # Fast adoptions (adopted dogs)
}).reset_index()

# Rename columns
location_stats.columns = ['state', 'city', 'total_listings', 'avg_days_listed', 'fast_adoptions']

# Round average days
location_stats['avg_days_listed'] = location_stats['avg_days_listed'].round(1)

# Sort by state and total listings
location_stats = location_stats.sort_values(['state', 'total_listings'], ascending=[True, False])

print(f"\n✅ Analyzed {len(location_stats)} unique city-state combinations")
print(f"\n📊 Top 10 Locations by Total Listings:")
print(location_stats.head(10).to_string(index=False))

# State-level summary
print(f"\n🏙️  State-Level Summary:")
state_summary = location_stats.groupby('state').agg({
    'total_listings': 'sum',
    'avg_days_listed': 'mean',
    'fast_adoptions': 'sum'
}).round(1).sort_values('total_listings', ascending=False)
print(state_summary)

# ============================================================================
# ADDITIONAL INSIGHTS
# ============================================================================

print("\n" + "=" * 70)
print("💡 ADDITIONAL INSIGHTS")
print("=" * 70)

# Age group impact
print("\n👶 Age Group vs Days Listed:")
age_impact = df.groupby('age_group')['days_listed'].agg(['mean', 'count']).round(1)
age_impact.columns = ['avg_days', 'count']
print(age_impact.sort_values('avg_days'))

# Size impact
print("\n📏 Size vs Days Listed:")
size_impact = df.groupby('size')['days_listed'].agg(['mean', 'count']).round(1)
size_impact.columns = ['avg_days', 'count']
print(size_impact.sort_values('avg_days'))

# Gender impact
print("\n🚹 Gender vs Days Listed:")
gender_impact = df.groupby('gender')['days_listed'].agg(['mean', 'count']).round(1)
gender_impact.columns = ['avg_days', 'count']
print(gender_impact.sort_values('avg_days'))

# Overall adoption rate
total_dogs = len(df)
total_adopted = (df['status'] == 'Adopted').sum()
adoption_rate = (total_adopted / total_dogs * 100)

print(f"\n📊 Overall Statistics:")
print(f"   Total Dogs Listed: {total_dogs}")
print(f"   Total Adopted: {total_adopted}")
print(f"   Overall Adoption Rate: {adoption_rate:.1f}%")
print(f"   Average Days to Adopt: {df['days_listed'].mean():.1f} days")
print(f"   Median Days to Adopt: {df['days_listed'].median():.1f} days")

# ============================================================================
# SAVE ANALYTICS FILES
# ============================================================================

print("\n" + "=" * 70)
print("💾 SAVING ANALYTICS FILES")
print("=" * 70)

# Save breed_adoption_stats.csv
breed_output = 'breed_adoption_stats.csv'
breed_final.to_csv(breed_output, index=False)
print(f"\n✅ Created: {breed_output}")
print(f"   📊 Records: {len(breed_final)}")
print(f"   📊 Columns: {list(breed_final.columns)}")

# Save location_adoption_stats.csv
location_output = 'location_adoption_stats.csv'
location_stats.to_csv(location_output, index=False)
print(f"\n✅ Created: {location_output}")
print(f"   📊 Records: {len(location_stats)}")
print(f"   📊 Columns: {list(location_stats.columns)}")

# ============================================================================
# FINAL SUMMARY
# ============================================================================

print("\n" + "=" * 70)
print("🎯 ANALYSIS COMPLETE - KEY FINDINGS")
print("=" * 70)

# Find extremes
fastest_breed = breed_final.nsmallest(1, 'avg_days_to_adopt').iloc[0]
slowest_breed = breed_final.nlargest(1, 'avg_days_to_adopt').iloc[0]
most_listed_breed = breed_final.nlargest(1, 'total_listings').iloc[0]

fastest_city = location_stats.nsmallest(1, 'avg_days_listed').iloc[0]
slowest_city = location_stats.nlargest(1, 'avg_days_listed').iloc[0]
most_listed_city = location_stats.nlargest(1, 'total_listings').iloc[0]

print(f"\n🏆 BREED INSIGHTS:")
print(f"   Fastest Adopted: {fastest_breed['breed']} ({fastest_breed['avg_days_to_adopt']:.1f} days)")
print(f"   Slowest Adopted: {slowest_breed['breed']} ({slowest_breed['avg_days_to_adopt']:.1f} days)")
print(f"   Most Listed: {most_listed_breed['breed']} ({most_listed_breed['total_listings']} dogs)")

print(f"\n📍 LOCATION INSIGHTS:")
print(f"   Fastest City: {fastest_city['city']}, {fastest_city['state']} ({fastest_city['avg_days_listed']:.1f} days)")
print(f"   Slowest City: {slowest_city['city']}, {slowest_city['state']} ({slowest_city['avg_days_listed']:.1f} days)")
print(f"   Most Active: {most_listed_city['city']}, {most_listed_city['state']} ({most_listed_city['total_listings']} dogs)")

print("\n" + "=" * 70)
print("🎯 STEP 3: DATA ANALYSIS - COMPLETED!")
print("=" * 70)

print("\n📁 Files Created:")
print(f"   1. {breed_output} ✅")
print(f"   2. {location_output} ✅")

print("\n✅ ALL CSV FILES READY FOR POWER BI:")
print("   1. dogs_raw.csv ✅")
print("   2. dogs_cleaned.csv ✅")
print("   3. breed_adoption_stats.csv ✅")
print("   4. location_adoption_stats.csv ✅")

print("\n💬 Reply 'Step 3 Done' to proceed to Step 4: Power BI Dashboards")
print("=" * 70)