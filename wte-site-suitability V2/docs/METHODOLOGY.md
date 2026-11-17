# Methodology, provenance and limitations

## Source
Sumantra Chaudhuri, *Development of Location Suitability Index for Waste-to-Energy plant by MCDM & ANN techniques*. Supplied internship report and presentation; source files are in `reports/`. The presentation identifies SVNIT Surat. No publication year, DOI or journal publication is invented here.

## Implemented calculation
Ten factors are ordered DR, CV, GF, DW, LN, ES, HD, LC, DD, AI. Table 4 supplies factor weights, Table 8 supplies Q for four sites. Suitability is the sum of weight times Q divided by the sum of weights. All Q must be finite in [0.1,0.9]. All weights must be finite and nonnegative with positive sum. Higher Q always means greater desirability in this subindex workflow.

The published factor weights do not sum to one. The denominator in the published SI equation is retained, rather than silently treating the weights as normalized. The software deliberately does NOT reconstruct missing 10-by-10 pairwise judgments from final weights.

## AHP audit
The three-criterion matrix (report Table 3; presentation slide 21) is [[1,3,7],[1/3,1,5],[1/7,1/5,1]]. Python uses its principal right eigenvector, CI=(lambda_max-3)/2, RI=0.58 and CR=CI/RI. Recomputed values can differ from the report's displayed eigenvector and CR; see results/audit.json. The 10-by-10 source matrices are unavailable, so their reported overall CR=0.0647 is not independently reproducible.

## Important unresolved source issues
- Table 8's displayed Q values and Table 4 weights reproduce reported SI to rounding precision. Both versions are preserved and tiny numerical differences exported.
- Raw geological-fault values are NA, while Table 8 assigns nonmissing geological-fault subindices. Their derivation is undocumented.
- Raw-to-Q mappings are not reproducible from the available tables. For example, the two identical energy-saving measurements in A1 and A2 map to different Q values. Residential distance and haul distance mappings also do not consistently follow the displayed extrema.
- Main-road distance is not silently asserted to be the definitive infrastructure mapping. The raw maintenance-cost variable has no direct named factor among the ten.
- The report refers to Wu et al. (2015). This repository preserves that attribution but has not independently verified the original external case-study dataset.
- Raw measurements are supplied as historical source data, not contemporary measurements or legal exclusion thresholds.

## ANN component
The original MATLAB weights, complete training dataset and exact training procedure are unavailable. The original 10–5–1 topology is not a recoverable fitted model. `report_ann_rows.csv` contains all extractable twelve-number rows from Table 6, report pages 22–25. Those rows are originally randomized model data, not field observations, and are not asserted to be the complete training dataset. Published predictions are used only to calculate descriptive metrics; their train/test membership is unknown.

`python analysis.py --train-ann` performs a NEW experiment: seed 42; 4000 synthetic ten-feature samples on {0.1,...,0.9}; exact SI formula as target; 70/15/15 train/validation/test; single hidden layer of five tanh neurons; L-BFGS training; validation selection over three regularization strengths. The test set is used only after selection. This is an architectural reimplementation, not numerical reproduction of MATLAB R2014b or its reported iteration count. No synthetic samples are described as actual candidate-site measurements.

Because the target is a weighted linear formula, a neural network is unnecessary for exact evaluation. A fitted linear regression baseline is included to expose this limitation. High surrogate accuracy does not establish environmental validity or model unknown interactions.

## Metric definitions
RMSE=sqrt(mean((observed-predicted)^2)); MAE=mean(abs(error)); NSE=1-SSE/sum((observed-mean)^2); PBIAS=100*sum(observed-predicted)/sum(observed); RSR=sqrt(SSE/centered_sum_squares). Covariance uses sample normalization (n-1). Covariance is not correlation and need not approach one for an accurate model. Degenerate denominators are exported as null.

## Use boundary
No GIS exclusions, statutory buffers, emissions evaluation, transport model, public-consultation score, uncertainty distribution or field validation is supplied. Do not treat a weighted compensatory ranking as permission to site a facility. The interactive interface is a transparent research portfolio and scenario exploration tool.
