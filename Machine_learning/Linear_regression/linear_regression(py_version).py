import numpy as np
import pandas as pd
import sklearn as sk
from sklearn import linear_model

dataset = pd.read_csv(".\\students_performance.csv")
df = dataset

df = df.drop(columns=['reading score','writing score'])

print(df.head())

#Here I'm converting each different value from each categorical column to a number
categorical_columns = ["gender","race/ethnicity","parental level of education","lunch","test preparation course"]
for column in categorical_columns:
    df[column] = pd.factorize(df[column])[0]


y_column = 'math score'
x_columns = df.columns.tolist()
x_columns.remove(y_column)


df_test = df.loc[0:100]
df_train = df.drop(df.index[0:100])

df_test.reset_index()
df_train.reset_index()

#df_test and df_train rows converted to np for model training and testing

#================================================================================
x_columns_train = np.array(df_train[x_columns])#.reshape(-1, 1)
y_column_train = np.array(df_train[y_column])

x_columns_test = np.array(df_test[x_columns])
y_column_test = np.array(df_test[y_column])
#================================================================================

df_test_without_y_column = df_test.drop(columns=[y_column])


#The Model
algorithm = linear_model.LinearRegression()
algorithm.fit(x_columns_train,y_column_train)



print("==============================")
accu = algorithm.score(x_columns_test, y_column_test)
print(f"Accuracy: {accu * 100}%")
print("==============================")




row_index= 50
row = np.array(df_test_without_y_column.loc[row_index])
prediction = algorithm.predict([row])

print("============================================================================")
print(f'{y_column}: {prediction}')
print("============================================================================")

print(dataset.loc[row_index])