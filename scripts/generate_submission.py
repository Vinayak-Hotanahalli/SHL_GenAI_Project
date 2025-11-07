import pandas as pd
import requests
import os
from tqdm import tqdm

# Configuration
API_URL = "http://127.0.0.1:8000/recommend"   # FastAPI endpoint
DATA_PATH = "data/Gen_AI Dataset.xlsx"        # Input Excel file
SHEET_NAME = "Test-Set"                       # Sheet name to read
OUTPUT_PATH = "submission.csv"                # Output CSV file
TOP_K = 5                                     # Number of recommendations per query

print("Reading Excel file:", DATA_PATH)
xls = pd.ExcelFile(DATA_PATH)
print("Found sheets:", xls.sheet_names)

# Check that the sheet exists
if SHEET_NAME not in xls.sheet_names:
    raise ValueError(f"Sheet '{SHEET_NAME}' not found in Excel. Found: {xls.sheet_names}")

# Read the correct sheet
df = pd.read_excel(DATA_PATH, sheet_name=SHEET_NAME)
print(f"Loaded {len(df)} rows from sheet: {SHEET_NAME}")
print("Columns:", df.columns.tolist())

# Identify the query column
query_col = None
for c in df.columns:
    if "query" in c.lower():
        query_col = c
        break

if query_col is None:
    raise ValueError("No column named like 'Query' found in Excel file.")

queries = df[query_col].dropna().astype(str).tolist()
print(f"Total queries to process: {len(queries)}")
if not queries:
    raise ValueError("No queries found in the selected sheet!")

rows = []
print("\nStarting recommendation generation...\n")

for q in tqdm(queries):
    print(f"\nQuery: {q}")
    try:
        response = requests.post(API_URL, json={"query": q, "k": TOP_K})
        print("Status Code:", response.status_code)

        if response.status_code == 200:
            recs = response.json().get("recommendations", [])
            print("Got", len(recs), "recommendations.")
            for r in recs:
                rows.append({
                    "Query": q,
                    "Assessment_url": r.get("url", "")
                })
        else:
            print(f"API returned error {response.status_code}: {response.text}")

    except Exception as e:
        print("Exception for query:", q, "->", e)

# Write output CSV
out = pd.DataFrame(rows)
print(f"\nWriting CSV with {len(out)} rows...")

out.to_csv(OUTPUT_PATH, index=False, encoding="utf-8")
abs_path = os.path.abspath(OUTPUT_PATH)
print(f"Wrote '{OUTPUT_PATH}' successfully at:\n{abs_path}")
