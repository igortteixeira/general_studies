import numpy as np
import pandas as pd
import sklearn as sk
from sklearn import linear_model


# Loading data and dropping columns that I think wouldn't help the model

dataset = pd.read_csv(".\\titanic.csv")
df = dataset
df = df.drop(columns=['embark_town','fare','parch','n_siblings_spouses'])



#Here I'm converting each different value from each categorical column to a number
#Example: on class column there are "First", "Second" and "Third" values. These will be converted to 1,2,3

categorical_columns =['sex','class','deck','alone']
for column in categorical_columns:
    df[column] = pd.factorize(df[column])[0]



#Here I'm getting a list of all columns except survived, for X values, and the column "survived" for Y values

x_columns = df.columns.tolist()
x_columns.remove('survived')
y_column = 'survived'


#Splitting dataset for testing and training the model

df_test = df.loc[0:100]
df_train = df.drop(df.index[0:100])

x_columns_train = np.array(df_train[x_columns])
y_column_train = np.array(df_train[y_column])

x_columns_test = np.array(df_test[x_columns])
y_column_test = np.array(df_test[y_column])



#I will use this df for testing the model manually (there is no "survived" column)

df_test_without_y_column = df_test.drop(columns=[y_column])

algorithm = linear_model.LogisticRegression(solver='liblinear', random_state=0)
algorithm.fit(x_columns_train, y_column_train)

print("==============================")
accu = algorithm.score(x_columns_test, y_column_test)
print(f"Accuracy: {accu * 100}%")
print("==============================")



#Each row from df_test_without_y_column will provide different information (X values)
#to test if they have chances of surviving (Y value)

row_index= 70
row = np.array(df_test_without_y_column.loc[row_index])
binary_chances = algorithm.predict_proba([row])

print("============================================================================")
print(f'Chances of not surviving (0): {binary_chances[0][0] * 100}%')
print(f'Chances of surviving (1): {binary_chances[0][1] * 100}%')
print("============================================================================")

print(dataset.loc[row_index])