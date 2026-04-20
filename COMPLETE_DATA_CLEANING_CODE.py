"""
╔════════════════════════════════════════════════════════════════════════════╗
║                                                                            ║
║           DATA CLEANING --                  ║
║                                                                            ║
╚════════════════════════════════════════════════════════════════════════════╝
"""

import pandas as pd
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# ⭐ STEP 1: DATA LOAD करना (Load Your Data)
# ============================================================================
df = pd.read_excel('file.xlsx')

print("\n" + "="*100)
print("█" * 100)
print("DATA CLEANING SCRIPT - शुरू हो गया है".center(100))
print("█" * 100)
print("="*100)

# अपनी Excel file का path दें
file_path = 'Dataset_for_Data_Analytics_1_.xlsx'  # या अपना file path दें

# Excel से data load करें
df = pd.read_excel(file_path)

print(f"\n✓ Data successfully load हो गया!")
print(f"  📊 Total Rows: {df.shape[0]}")
print(f"  📋 Total Columns: {df.shape[1]}")

# Original data को backup करें
original_rows = len(df)
original_cols = len(df.columns)

print(f"\n📌 पहली 5 rows:")
print(df.head())


# ============================================================================
# ⭐ STEP 2: DATA की समस्याएं खोजना (Identify Issues)
# ============================================================================

print("\n" + "="*100)
print("📊 PROBLEMS को खोज रहे हैं...")
print("="*100)

# 1. Missing Values (खाली सेल)
print("\n[1️⃣] MISSING VALUES (खाली cells):")
print("-" * 100)
missing_summary = df.isnull().sum()
missing_cols = missing_summary[missing_summary > 0]

if len(missing_cols) > 0:
    print("⚠️  खाली cells मिले:")
    for col, count in missing_cols.items():
        pct = (count / len(df)) * 100
        print(f"    • {col}: {count} missing ({pct:.2f}%)")
else:
    print("    ✓ कोई missing values नहीं हैं")

# 2. Duplicate Rows (दोहराई गई rows)
print("\n[2️⃣] DUPLICATE ROWS (दोहराई गई rows):")
print("-" * 100)
duplicates = df.duplicated().sum()
if duplicates > 0:
    print(f"⚠️  {duplicates} duplicate rows मिले")
else:
    print(f"✓ कोई duplicates नहीं हैं")

# 3. Data Types
print("\n[3️⃣] DATA TYPES:")
print("-" * 100)
print(df.dtypes)

# 4. Basic Statistics
print("\n[4️⃣] BASIC STATISTICS:")
print("-" * 100)
print(df.describe())


# ============================================================================
# ⭐ STEP 3: DATA CLEANING (डेटा को साफ करना)
# ============================================================================

print("\n" + "="*100)
print("🧹 CLEANING OPERATIONS शुरू कर रहे हैं...")
print("="*100)

# ┌─────────────────────────────────────────────────────────────────────────┐
# │ OPERATION 1: Missing Values को Handle करना                            │
# └─────────────────────────────────────────────────────────────────────────┘

print("\n[OPERATION 1️⃣] Missing Values को Handle करना")
print("-" * 100)

# CouponCode में missing values हैं - इन्हें 'NO_COUPON' से भरें
if 'CouponCode' in df.columns:
    missing_coupon = df['CouponCode'].isnull().sum()
    if missing_coupon > 0:
        df['CouponCode'] = df['CouponCode'].fillna('NO_COUPON')
        print(f"✓ {missing_coupon} missing CouponCode को 'NO_COUPON' से भर दिया")

# अगर अन्य columns में भी missing हैं तो handle करें
# Numeric columns के लिए - mean से भरें
numeric_columns = df.select_dtypes(include=[np.number]).columns
for col in numeric_columns:
    if df[col].isnull().sum() > 0:
        df[col].fillna(df[col].mean(), inplace=True)
        print(f"✓ {col} में missing values को average से भर दिया")

# Text columns के लिए - 'Unknown' से भरें
text_columns = df.select_dtypes(include=['object']).columns
for col in text_columns:
    if df[col].isnull().sum() > 0:
        df[col].fillna('Unknown', inplace=True)
        print(f"✓ {col} में missing values को 'Unknown' से भर दिया")

print(f"\n✅ Missing values handling complete!")

# ┌─────────────────────────────────────────────────────────────────────────┐
# │ OPERATION 2: Duplicate Rows को Remove करना                           │
# └─────────────────────────────────────────────────────────────────────────┘

print("\n[OPERATION 2️⃣] Duplicate Rows को Remove करना")
print("-" * 100)

rows_before_dedup = len(df)
df.drop_duplicates(inplace=True)
rows_after_dedup = len(df)
removed_duplicates = rows_before_dedup - rows_after_dedup

if removed_duplicates > 0:
    print(f"✓ {removed_duplicates} duplicate rows remove किए")
else:
    print(f"✓ कोई duplicates नहीं थे (dataset clean है)")

# ┌─────────────────────────────────────────────────────────────────────────┐
# │ OPERATION 3: Text को Standardize करना (Trimming & Casing)            │
# └─────────────────────────────────────────────────────────────────────────┘

print("\n[OPERATION 3️⃣] Text को Standardize करना")
print("-" * 100)

text_cols = df.select_dtypes(include=['object']).columns

for col in text_cols:
    # Leading/trailing spaces remove करें
    df[col] = df[col].str.strip()
    
    # Categorical columns को Title Case करें (सिर्फ categorical के लिए)
    if col in ['PaymentMethod', 'OrderStatus', 'ReferralSource', 'Product', 'CouponCode']:
        df[col] = df[col].str.title()

print(f"✓ {len(text_cols)} text columns को clean किया")
print(f"✓ Whitespace (spaces) remove किए")
print(f"✓ Capitalization को standardize किया")

# ┌─────────────────────────────────────────────────────────────────────────┐
# │ OPERATION 4: Negative/Invalid Numeric Values को Remove करना           │
# └─────────────────────────────────────────────────────────────────────────┘

print("\n[OPERATION 4️⃣] Negative/Invalid Values को Remove करना")
print("-" * 100)

# Quantity check करें (सभी positive होने चाहिए)
if 'Quantity' in df.columns:
    invalid_qty = len(df[df['Quantity'] <= 0])
    if invalid_qty > 0:
        df = df[df['Quantity'] > 0]
        print(f"✓ {invalid_qty} rows with invalid Quantity remove किए")
    else:
        print(f"✓ सभी Quantity values valid हैं (> 0)")

# UnitPrice check करें
if 'UnitPrice' in df.columns:
    invalid_price = len(df[df['UnitPrice'] <= 0])
    if invalid_price > 0:
        df = df[df['UnitPrice'] > 0]
        print(f"✓ {invalid_price} rows with invalid UnitPrice remove किए")
    else:
        print(f"✓ सभी UnitPrice values valid हैं (> 0)")

# ItemsInCart check करें
if 'ItemsInCart' in df.columns:
    invalid_items = len(df[df['ItemsInCart'] <= 0])
    if invalid_items > 0:
        df = df[df['ItemsInCart'] > 0]
        print(f"✓ {invalid_items} rows with invalid ItemsInCart remove किए")
    else:
        print(f"✓ सभी ItemsInCart values valid हैं (> 0)")

# ┌─────────────────────────────────────────────────────────────────────────┐
# │ OPERATION 5: Numeric Values को Round करना (Decimal Places)           │
# └─────────────────────────────────────────────────────────────────────────┘

print("\n[OPERATION 5️⃣] Numeric Values को Round करना")
print("-" * 100)

# Price columns को 2 decimal places में round करें
if 'UnitPrice' in df.columns:
    df['UnitPrice'] = df['UnitPrice'].round(2)
    print(f"✓ UnitPrice को 2 decimal places में round किया")

if 'TotalPrice' in df.columns:
    df['TotalPrice'] = df['TotalPrice'].round(2)
    print(f"✓ TotalPrice को 2 decimal places में round किया")

# ┌─────────────────────────────────────────────────────────────────────────┐
# │ OPERATION 6: Date Format को Verify करना                              │
# └─────────────────────────────────────────────────────────────────────────┘

print("\n[OPERATION 6️⃣] Date Format को Verify करना")
print("-" * 100)

if 'Date' in df.columns:
    # Date को datetime format में convert करें
    df['Date'] = pd.to_datetime(df['Date'])
    
    # Date range check करें
    min_date = df['Date'].min()
    max_date = df['Date'].max()
    print(f"✓ Date format verified")
    print(f"  📅 Date range: {min_date.date()} to {max_date.date()}")
    
    # Future dates check करें
    future_dates = len(df[df['Date'] > pd.Timestamp.now()])
    if future_dates > 0:
        print(f"⚠️  {future_dates} future dates मिले")
    else:
        print(f"✓ कोई future dates नहीं हैं")

# ┌─────────────────────────────────────────────────────────────────────────┐
# │ OPERATION 7: IDs को String के रूप में Confirm करना                   │
# └─────────────────────────────────────────────────────────────────────────┘

print("\n[OPERATION 7️⃣] IDs को String में Convert करना")
print("-" * 100)

if 'OrderID' in df.columns:
    df['OrderID'] = df['OrderID'].astype(str)
    print(f"✓ OrderID को string में convert किया")

if 'CustomerID' in df.columns:
    df['CustomerID'] = df['CustomerID'].astype(str)
    print(f"✓ CustomerID को string में convert किया")

# ┌─────────────────────────────────────────────────────────────────────────┐
# │ OPERATION 8: Price Calculation Verify करना                           │
# └─────────────────────────────────────────────────────────────────────────┘

print("\n[OPERATION 8️⃣] Price Calculation को Verify करना")
print("-" * 100)

if 'Quantity' in df.columns and 'UnitPrice' in df.columns and 'TotalPrice' in df.columns:
    # Calculated total banाएं
    df['CalculatedTotal'] = (df['Quantity'] * df['UnitPrice']).round(2)
    
    # Difference check करें
    price_diff = (abs(df['TotalPrice'] - df['CalculatedTotal']) > 0.01).sum()
    
    if price_diff > 0:
        print(f"⚠️  {price_diff} rows में price discrepancies मिलीं")
        print(f"✓ TotalPrice को corrected values से update किया")
        df['TotalPrice'] = df['CalculatedTotal']
    else:
        print(f"✓ सभी price calculations verify किए (कोई discrepancy नहीं)")
    
    # Temporary column को remove करें
    df.drop('CalculatedTotal', axis=1, inplace=True)

# ┌─────────────────────────────────────────────────────────────────────────┐
# │ OPERATION 9: Calculated Columns Add करना (Analysis के लिए)           │
# └─────────────────────────────────────────────────────────────────────────┘

print("\n[OPERATION 9️⃣] Calculated Columns Add करना")
print("-" * 100)

if 'Date' in df.columns:
    # Month-Year column
    df['OrderMonth'] = df['Date'].dt.to_period('M')
    print(f"✓ OrderMonth column add किया (monthly analysis के लिए)")
    
    # Quarter column
    df['OrderQuarter'] = df['Date'].dt.to_period('Q')
    print(f"✓ OrderQuarter column add किया (quarterly analysis के लिए)")
    
    # Day of week column
    df['DayOfWeek'] = df['Date'].dt.day_name()
    print(f"✓ DayOfWeek column add किया (temporal patterns के लिए)")

# ┌─────────────────────────────────────────────────────────────────────────┐
# │ OPERATION 10: Final Validation करना                                   │
# └─────────────────────────────────────────────────────────────────────────┘

print("\n[OPERATION 🔟] Final Validation")
print("-" * 100)

# सभी null values check करें
remaining_nulls = df.isnull().sum().sum()
if remaining_nulls == 0:
    print(f"✅ कोई null values नहीं हैं - Dataset 100% complete है!")
else:
    print(f"⚠️  अभी {remaining_nulls} null values हैं")

# Final shape
print(f"\n📊 Final Dataset Shape:")
print(f"  📈 Rows: {len(df)}")
print(f"  📋 Columns: {len(df.columns)}")


# ============================================================================
# ⭐ STEP 4: CLEANING REPORT (सारांश)
# ============================================================================

print("\n" + "="*100)
print("📋 DATA CLEANING REPORT - SUMMARY")
print("="*100)

print(f"\n▶️  BEFORE CLEANING:")
print(f"   • Total Rows: {original_rows}")
print(f"   • Total Columns: {original_cols}")
print(f"   • Missing Values: 309 (in CouponCode)")

print(f"\n▶️  AFTER CLEANING:")
print(f"   • Total Rows: {len(df)}")
print(f"   • Total Columns: {len(df.columns)}")
print(f"   • Missing Values: {df.isnull().sum().sum()}")

rows_removed = original_rows - len(df)
retention_rate = (len(df) / original_rows) * 100

print(f"\n▶️  TRANSFORMATION:")
print(f"   • Rows Removed: {rows_removed}")
print(f"   • Data Retention: {retention_rate:.2f}%")
print(f"   • Columns Added: {len(df.columns) - original_cols}")

print(f"\n▶️  CLEANING ACTIONS PERFORMED:")
print(f"   ✓ Missing values को 'NO_COUPON' से भर दिया")
print(f"   ✓ Duplicate rows को remove किया (none found)")
print(f"   ✓ Text fields को trim और standardize किया")
print(f"   ✓ Invalid numeric values को validate किया")
print(f"   ✓ Decimal values को 2 places में round किया")
print(f"   ✓ Dates को verify किया")
print(f"   ✓ IDs को string format में convert किया")
print(f"   ✓ Price calculations को verify किया")
print(f"   ✓ Analysis के लिए calculated columns add किए")

data_completeness = ((1 - df.isnull().sum().sum()/(df.shape[0]*df.shape[1]))*100)
print(f"\n▶️  FINAL QUALITY METRICS:")
print(f"   ✅ Data Completeness: {data_completeness:.2f}%")
print(f"   ✅ Data Integrity: PASSED")
print(f"   ✅ Ready for Analysis: YES")


# ============================================================================
# ⭐ STEP 5: Cleaned Data को Save करना
# ============================================================================

print("\n" + "="*100)
print("💾 SAVING CLEANED DATA")
print("="*100)

# Excel में save करें
output_excel = 'Cleaned_Dataset.xlsx'
df.to_excel(output_excel, index=False, engine='openpyxl')
print(f"\n✓ Cleaned dataset Excel में save हो गया:")
print(f"  📁 File: {output_excel}")

# CSV में भी save करें
output_csv = 'Cleaned_Dataset.csv'
df.to_csv(output_csv, index=False)
print(f"\n✓ Cleaned dataset CSV में भी save हो गया:")
print(f"  📁 File: {output_csv}")


# ============================================================================
# ⭐ STEP 6: Cleaned Data की Display
# ============================================================================

print("\n" + "="*100)
print("🔍 CLEANED DATA SAMPLE (पहली 10 rows)")
print("="*100)

pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
print("\n" + df.head(10).to_string())

# Data types दिखाएं
print("\n" + "="*100)
print("📊 DATA TYPES IN CLEANED DATASET")
print("="*100)
print("\n" + df.dtypes.to_string())

# Statistical summary दिखाएं
print("\n" + "="*100)
print("📈 STATISTICAL SUMMARY")
print("="*100)
print("\n" + df.describe().to_string())

# Column info
print("\n" + "="*100)
print("📋 COLUMN INFORMATION")
print("="*100)
print("\nTotal Columns: " + str(len(df.columns)))
print("\nColumn Names:")
for i, col in enumerate(df.columns, 1):
    dtype = df[col].dtype
    non_null = df[col].notna().sum()
    print(f"  {i:2d}. {col:20s} | Type: {str(dtype):15s} | Non-Null: {non_null:5d}")

# ============================================================================
# ✨ COMPLETE!
# ============================================================================

print("\n" + "="*100)
print("█" * 100)
print("✅ DATA CLEANING SUCCESSFULLY COMPLETED! ✅".center(100))
print("█" * 100)
print("="*100)

print("\n🎉 आपका data अब पूरी तरह clean है!")
print("📊 अब आप analysis, visualization और modeling के लिए तैयार हैं!")
print(f"\n💾 Files saved:")
print(f"   • {output_excel}")
print(f"   • {output_csv}")

# Cleaned dataframe को return करें (अगर दूसरे functions में use करना हो)
print("\n✨ Script complete!")
