# HCC Dataset Documentation

## Dataset Overview
-**Source**: University Hospital, Portugal
-**Patients**: 165 real HCC patients
-**Features**: 49 clinical features + 1 survival outcome
-**Target Variable**: 1-year survival (0 = dies, 1 = lives)
**Collection Period**: 2015, based on citation

## Data Characteristics

### Class Distribution
-**Imbalanced dataset**:
	- Dies (0): 63 patients (38.2%)
	- Lives (1): 102 patients (61.8%)
	- **Imbalance ratio**: (1.62: 1)

Class imbalance affects model training, evaluation and clinical utility:

1. **Training Bias**: Models naturally favour the majority class ("lives"), learnign to predict it more often since it appears 62% of the time. This can result in poor detection of the minority class ("dies").

2. **Misleading Metrics**: A naive model that always predicts "lives" achieves 62% accuracy without even learning anything meaningful. This makes accuracy unreliable, so we must use precision, recall, F1-score and ROC-AUC instead.

3. **Clinical Consequences**: Failing to identify patients who will die within one year means missing opportunities for palliative care, aggressive treatment or family preparation. The minority class is usually **more important** to predict correctly.

4. **Stratified splitting**: There is a need to use stratified train / test splits to ensure both sets maintain the 38% / 62% class distribution, making evaluation representative of real-world performance.


### Missing Data
-**Overall missing data**: 10.22%
-**Complete cases**: Only 8 patients (4.85%)
-**Features with highest missing data**:
	- Oxygen Saturation: 48.48%
	- Ferritin: 48.48%
	- Iron: 47.88%
	- Direct Bilirubin: 26.67%

Healthcare data is often incomplete because tests are ordered based on clinical need, not research requirements. In this dataset, high missingness in features like Oxygen Saturation (48%) and Ferritin (48%) likely indicates these tests were only performed when clinically warranted, meaning the absence of the data itself carries information about patient stability.

With only 8 complete cases (4.85%), we cannot simply delete rows with missing values. Instead, we must use sophisticated imputation techniques that represent the clinical context: missing O2 saturation may indicate a stable patient, not truly "missing" data. This requires creating missingness indicators as features and using multiple imputation methods that leverage relationships between variables. 

The non-random (MNAR) nature of this missingness means that our imputation strategy directly impacts model validity and clinical interpretability.

### Feature Types
- **Quantitative**: 23 variables (lab values, measurements)
- **Qualitative**: 26 variables (1/0, categorical)

## Dataset Strengths
- Real clinical data (not synthetic)
- Follows EASL-EORTC guidelines

## Dataset Limitations
- Small sample size (165 patients)
- High missingness in some features
- Class imbalance

## Citation
Miriam Seoane Santos, Pedro Henriques Abreu, Pedro J. García-Laencina, Adélia Simão, Armando Carvalho, “A new cluster-based oversampling method for improving survival prediction of hepatocellular carcinoma patients”, Journal of biomedical informatics, 58, 49-59, 2015.
