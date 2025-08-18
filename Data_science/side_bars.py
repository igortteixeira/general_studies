from matplotlib import pyplot as plt
import numpy as np
import pandas as pd


days = [2010,2011,2012,2013,2014,2016,2022,2025,2026,2027,2030]
python_popularity = [30,40,50,60,70,80,90,100,130,175,180]
javascript_popularity = [30,50,70,90,150,200,230,300,315,320,333]
x_indexes = np.arange(len(days))
w = 0.25


plt.title('Backend Language Popularity')
plt.ylabel("Popularity")
plt.xlabel("Time")

plt.bar(x_indexes,python_popularity,label="Python",color='#00DFFF',width=w)
plt.bar(x_indexes - w,javascript_popularity,label="javascript",color='#6A00FF',width=w)
plt.xticks(ticks=x_indexes,labels=days)

plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
