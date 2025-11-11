# SANER2026
This Repository has been created as a replication package of the paper titled 'Studying multifaceted hero developers and their performance in the bug fixing process' which is under review at SANER 2026. The Repository contains the python scripts and other resources that have been used across this study.

## Repository Structure
The code has been segregated based on the objective it was written for. The broader objectives have been segregated in the form of folders, and detail oriented objectives are divided either by code files, or by functions within them. Some pickle files have been added in the 'Pickle Files' directory, for the ease of execution. However, the scripts to generate these pickles are also included within their respective task folders. Some pickle files are also available in the task folders. There is a possibility of duplicacy (same file being in the folder and outside), but it would not affect the code or its execution in any manner. All of these pickle files are generated from the same 'SmartShark' dataset that has been used throughout the project.

## IDE
Ideally, Pycharm IDE shall be used for executing these files. However, any other popular IDE would also do the job. For data manipulation, MongoDB is required and Studio 3t would help with the data visualization.

## Libraries
Various libraries have been used in the development of this project. They can be installed by running "pip install requirements.txt" after downloading the requirements.txt file.

## Other Important Information
Identity merging is the process of linking various accounts used by a person to one unique ID associated with him. Thus, it becomes an important step in the preprocessing of the data. Wherever required, the files present in the 'IdentityMerging' directory need to be imported in the same folder for smooth operation of the code, or the import address can be modified as per usage.

## Steps to Replicate

To reproduce the results of the study, follow these steps in sequence:

1. **Generate Hero CSV Files**  
   Run all `.py` files located in the following folders:
   - `SocialHeroism`
   - `SocioTechnicalHeroism`
   - `SuperHeroism`
   - `TechnicalHeroism`
   - `TechnoSocialHeroism`  
   These scripts will generate CSV files representing different hero developer categories.

2. **Generate Pickle Files**  
   Run the script `avg_time_pickles.py` to get the average time each severity-hero pair.

3. **Create Fixed and Reopened Issue Severity Pickles**  
   Execute the scripts `fixed_issues.py` and `reopened_issues.py` sequentially.  
   These scripts generate severity-level pickle files for both fixed and reopened issues.
 
4. **Compute Jaccard Coefficients (RQ2)**  
   Run the script `rq2_jaccard.py`.  
   This script generates Jaccard coefficient heatmaps showing the similarity between different hero types.

5. **Compute Scott-Knott Rankings (RQ3)**  
   Run the script `rq3_scott-knot.py` and `rq3_scott-knot_esd.py`.  
   This will produce the Scott-Knott rankings for each severity level across both fixed and reopened issue categories.

6. **Compute Kendall’s Tau Correlations (RQ3)**  
   Run the script `rq3_kendall-tau.py`.  
   This script calculates Kendall’s Tau correlations between the severity rankings of each category (fixed and reopened).

---

### Summary of Output

After completing the above steps, you will obtain:
- **Hero CSV files** — representing different hero developer categories.  
- **Pickle files** — intermediate data representations for further processing.  
- **Fixed and Reopened Severity Pickles** — categorized issue severity data.  
- **Jaccard Heatmaps** — similarity visualizations among hero categories.
- **Scott-Knott Rankings** — comparative rankings of hero groups by severity.  
- **Kendall’s Tau Correlations** — statistical correlations across rankings.

These outputs together replicate the full experimental workflow and results presented in the paper.

## 📄 Paper

You can read the full paper here:  
[🔗 Download Paper (PDF)]
