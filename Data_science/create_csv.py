import numpy as np
import pandas as pd
import random

data = {"random_number0": np.array([], dtype=int), "random_number1": np.array([], dtype=int)}
df= pd.DataFrame.from_dict(data)
df.to_csv('.\\scratch.csv',index=False)
