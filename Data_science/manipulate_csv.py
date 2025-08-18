import numpy as np
import pandas as pd
from itertools import count
import random
import time

csv_path = ".\\scratch.csv"
dataset = pd.read_csv(csv_path)
df = dataset

i_count = 20
index = count()
x_vals = []

while i_count != 0:

	x_vals.append(next(index))
	df1 = pd.DataFrame([[x_vals[-1],random.randint(0, 10)]], columns=['random_number0', 'random_number1'],)
		
	df = pd.concat([df, df1],ignore_index = True)
	print(df)

	time.sleep(1)
	i_count -= 1

	df.to_csv(csv_path,index=False)


dataset.to_csv(csv_path,index=False)