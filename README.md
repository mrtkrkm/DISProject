# Temperature Predicting

To find the best features based on the different shift values run FeatureSelection.ipynb
After it choose the best features from the results dataframe based on the their results.

To see the results with different features and different train and test size run Results.ipynb
```python
pr=PreProcess(df, ddir='data/output.txt', target_col='T (degC)', shift_day=7)
```

df is DataFrame
shift_y is desired shifting value

```python
X_train, y_train, X_test, y_test=pr.split_data(day_number=30, day_pred=1, day_start=0)
```