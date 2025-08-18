from matplotlib import pyplot as plt
import numpy as np
import pandas as pd


popularity = [64,56,48,47,35,33,30,27,27,24]
programming_laguages = ["Javascript","HTML/CSS","Python","SQL","Java","Node","Typerscript","C#","Bash/Shell","C++"]


plt.title('Programming languages popularity')
plt.ylabel("Programming Languages")
plt.xlabel("Popularity")
popularity.reverse()
programming_laguages.reverse()

plt.barh(programming_laguages,popularity,color='#00DFFF')


plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
