from matplotlib import pyplot as plt
import numpy as np
import pandas as pd


continents = ["Asia","Africa","Europe","North America","South America","Oceania"]
population = [59.8,16.7,9.8,7.6,5.6,0.5]
emphasize_africa = [0,0.1,0,0,0,0]


plt.pie(
population,labels=continents,wedgeprops={'edgecolor':'#000000'},
explode=emphasize_africa,shadow=True,startangle=90,
autopct="%1.1f%%")

plt.title('Population distribution (7.631 billion)')
plt.tight_layout()
plt.show()
