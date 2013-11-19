import pickle
import numpy as np
import matplotlib.pyplot as plt

data = pickle.load(open("data.pkl", "rb"))

X = np.array([x for x,y in data])
Y = np.array([y for x,y in data])

X = np.log(X)
Y = np.log(Y)



plt.plot(X, Y, 'ro')


from scipy.optimize import curve_fit

def func(x, a, b):
    return a * x + b

popt, pcov = curve_fit(func, X, Y)


plt.margins(0.2)
plt.plot(X, func(X, *popt), 'r-', label="Fitted Curve")
plt.subplots_adjust(bottom=0.15)
plt.show()

print popt
print pcov
