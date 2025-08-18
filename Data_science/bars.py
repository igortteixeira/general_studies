from matplotlib import pyplot as plt
import numpy as np
import pandas as pd


programming_languages = ["PhP","C","C++","Python","Java","Javasript"]
people = [30,40,50,60,70,80]
data = (programming_languages,people)

plt.title('Popular Programming Languages')
plt.ylabel("People")
plt.xlabel("Programming language")

plt.bar(data[0],data[1],label="Analyzes",color='#979796')
plt.legend()

plt.grid(True)
plt.tight_layout()
plt.show()