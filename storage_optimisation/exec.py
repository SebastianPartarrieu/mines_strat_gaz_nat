from optimizer import Optimizer
from stockage import Stockage
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

plt.close()
path_spot = Path(__file__).parent.parent / 'Data' / 'spot_history_HH.csv'
path_simulations
data =  pd.read_csv(path_spot)
data = data.iloc[50:300]
data['Day'] = pd.to_datetime(data['Day'], format = '%Y-%m-%d')
#data['Price'] = np.sin(np.linspace(0,6,len(data['Day'])))+1
plt.plot(data['Day'], data['Price'])
plt.show()
plt.close()
X_0 = np.zeros( len(data['Day']))


stock = Stockage(100, 50, data, X_0)
stock.plot_threshold()

print('Volume',stock.volume_end)
print('Threshold', stock.threshold_con)

opti = Optimizer(stock) 
opti.contraints_init()
opti.optimize()
stock.plot_threshold()
stock.plot_volume()
plt.show()

plt.close()
stock.plot_injection()
plt.legend()
plt.show()

