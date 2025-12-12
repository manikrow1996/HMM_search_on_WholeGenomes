
#!/usr/bin/env python3
import os
import sys
import subprocess
import pandas as pd

# Check for input argument
if len(sys.argv) < 2:
    print("Usage: python nifH_pipeline.py <input_folder_with_faa_files>")
    sys.exit(1)

input_dir = sys.argv[1]  # Folder passed as $1
hmm_profile = "4.nifH.hmm"  # Path to Nitrogenase deaminase HMM
output_candidates = "nifH_candidates_allgenomes.csv"
output_matrix = "nifH_presence_absence_allgenomes.csv"
EVALUE_THRESHOLD = 1e-5
threads = 4

# Create output folder for HMMER results
os.makedirs("hmmer_results", exist_ok=True)

# STEP 1: Run hmmsearch for each .faa file
for file in os.listdir(input_dir):
    if file.endswith(".faa"):
        genome_name = file.replace(".faa", "")
        faa_path = os.path.join(input_dir, file)
        tblout_path = os.path.join("hmmer_results", f"{genome_name}.tbl")

        cmd = [
            "hmmsearch", "--cpu", str(threads), "--tblout", tblout_path,
            hmm_profile, faa_path
        ]
        print(f"Running: {' '.join(cmd)}")
        subprocess.run(cmd, check=True)

# STEP 2: Parse tblout files
candidates = []
presence = {}

for file in os.listdir("hmmer_results"):
    if file.endswith(".tbl"):
        genome = file.replace(".tbl", "")
        presence[genome] = 0
        with open(os.path.join("hmmer_results", file)) as f:
            for line in f:
                if line.startswith("#") or not line.strip():
                    continue
                parts = line.split()
                if len(parts) >= 19:
                    try:
                        evalue = float(parts[4].replace("e", "E"))
                        score = float(parts[5])
                    except ValueError:
                        continue
                    target = parts[0]
                    description = " ".join(parts[18:])
                    if evalue <= EVALUE_THRESHOLD:
                        candidates.append([genome, target, evalue, score, description])
                        presence[genome] = 1

# STEP 3: Save outputs
df_candidates = pd.DataFrame(candidates, columns=["genome", "protein_id", "evalue", "score", "description"])
df_candidates.to_csv(output_candidates, index=False)

df_matrix = pd.DataFrame(list(presence.items()), columns=["genome", "nifH_present"])
df_matrix.to_csv(output_matrix, index=False)

print(f"Processed {len(df_candidates)} strong Nitrogenase deaminase hits across {len(df_matrix)} genomes.")
print("Detailed candidates table:", output_candidates)
print("Presence/absence matrix:", output_matrix)
