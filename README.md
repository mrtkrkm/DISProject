# Temperature Predicting

For preprocessing

python day_avg.py jena_climate_2009_2016.csv >> <output_file>

python api_parse.py api.f >> <output_file>

OR with hadoop

python day_avg.py --hadoop-streaming-jar /usr/hdp/current/hadoop-mapreduce-client/hadoop-streaming.jar -r 
hadoop hdfs:///jena/jena_climate_2009_2016.csv 
--output-dir hdfs:///jena/output --no-output

python api_parse.py --hadoop-streaming-jar /usr/hdp/current/hadoop-mapreduce-client/hadoop-streaming.jar -r 
hadoop hdfs:///api.f 
--output-dir hdfs:///api/output --no-output


both inputs jena_climate_2009_2016.csv or api.f must be at the same folder with python files.
If hadoop way is going to be used, corresponding configuration and hadoop/file folder paths must be organized.

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

