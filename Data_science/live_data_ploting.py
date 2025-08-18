from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
import pandas as pd


fig,(ax) = plt.subplots()


def animate(i):
	dataset = pd.read_csv(".\\scratch.csv")
	df = dataset
	x_axis = df["random_number0"]
	y_axis = df["random_number1"]

	ax.cla()
	ax.plot(x_axis,y_axis,label="Live Data",linestyle='-')
	ax.grid(True)

ani = FuncAnimation(fig,animate, interval=1000)

plt.tight_layout()
plt.show()