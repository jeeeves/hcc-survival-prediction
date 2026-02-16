# HCC Dataset Documentation

## Files in This Directory

### hcc-data.csv
- **Description**: Original HCC patient dataset
- **Rows**: 165 patients
- **Columns**: 50 (49 clinical features + 1 one-year survival outome)
- **Format**: CSV with headers
- **Missing values**: Denoted by "?"
- **Target variable**: `Class` (0 = dies, 1 = lives)
- **Collection Period**: 2015, based on citation

## Data Characteristics

### Class Distribution
- **Imbalanced dataset**:
	- Dies (0): 63 patients (38.2%)
	- Lives (1): 102 patients (61.8%)
	- **Imbalance ratio**: 1.62: 1

Class imbalance affects model training, evaluation and clinical utility:

1. **Training Bias**: Models naturally favour the majority class ("lives"), learnign to predict it more often since it appears 62% of the time. This can result in poor detection of the minority class ("dies").

2. **Misleading Metrics**: A naive model that always predicts "lives" achieves 62% accuracy without even learning anything meaningful. This makes accuracy unreliable, so we must use precision, recall, F1-score and ROC-AUC instead.

3. **Clinical Consequences**: Failing to identify patients who will die within one year means missing opportunities for palliative care, aggressive treatment or family preparation. The minority class is usually **more important** to predict correctly.

4. **Stratified splitting**: There is a need to use stratified train / test splits to ensure both sets maintain the 38% / 62% class distribution, making evaluation representative of real-world performance.


### Missing Data
- **Overall missing data**: 10.22%
- **Complete cases**: Only 8 patients (4.85%)
- **Features with highest missing data**:
	1. Oxygen Saturation: 48.48%
	2. Ferritin: 48.48%
	3. Iron: 47.88%
	4. Direct Bilirubin: 26.67%

Healthcare data is often incomplete because tests are ordered based on clinical need, not research requirements. In this dataset, high missingness in features like Oxygen Saturation (48%) and Ferritin (48%) likely indicates these tests were only performed when clinically warranted, meaning the absence of the data itself carries information about patient stability.

With only 8 complete cases (4.85%), we cannot simply delete rows with missing values. Instead, we must use sophisticated imputation techniques that represent the clinical context: missing O2 saturation may indicate a stable patient, not truly "missing" data. This requires creating missingness indicators as features and using multiple imputation methods that leverage relationships between variables. 

The non-random (MNAR) nature of this missingness means that our imputation strategy directly impacts model validity and clinical interpretability.

### Feature Types
- **Quantitative**: 23 variables
	- Discrete: 2 (age, number of nodules)
	- Continuous: 21 (lab values, measurements, etc.)
- **Qualitative**: 26 variables (1/0, categorical)
	- Ordinal: 3 (PS, Encephalopathy, Ascites Degree)
	- Binary variables (Nominal): 23 (mostly yes/no clinical factors)

## Dataset Strengths
- Real clinical data (not synthetic)
- Follows EASL-EORTC guidelines
- Includes diverse risk factors, lab values and tumour characteristics
- Realistic class imbalance and missing data patterns

## Dataset Limitations
- **Small sample size (165 patients)**: limits model complexity
- **High missingness in some features**: requires imputation
- **Class imbalance**: requires appropriate handling
- **Single-center study**: may not generalise to all populations
- **Limited to 1-year survival**: does not capture longer-term outcomes

This project uses the **original, unprocessed HCC dataset** rather than preprocessed 
versions to demonstrate real-world situations:
- Handling missing data with clinical justification
- Addressing class imbalance appropriately
- Data cleaning and validation
- Working with imperfect, real healthcare data

### Data Privacy Note
This dataset contains de-identified patient data from a University Hospital in Portugal.
No personally identifiable information is included.

## Citation
Miriam Seoane Santos, Pedro Henriques Abreu, Pedro J. García-Laencina, Adélia Simão, Armando Carvalho, “A new cluster-based oversampling method for improving survival prediction of hepatocellular carcinoma patients”, Journal of biomedical informatics, 58, 49-59, 2015.
