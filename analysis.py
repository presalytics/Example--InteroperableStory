import presalytics
import matplotlib.pyplot as plt
from sklearn import datasets, linear_model
import numpy as np

# Use sklearn to generate a test dataset
x, y_prime, coef = datasets.make_regression(n_samples=30,
                                            n_features=1,
                                            n_informative=1, 
                                            noise=500*np.random.rand(),
                                            coef=True, 
                                            random_state=0)

# Add some more randomness to the generated dataset
y = (-1 if np.random.rand() < 0.5 else 1) * np.random.rand() * y_prime

# Run a linear regression on the dataset
lr = linear_model.LinearRegression(fit_intercept=False)
lr.fit(x, y, sample_weight=np.ones(len(x)))

#Build a trendline
x_arr = np.arange(x.min(), x.max())[:, np.newaxis]
y_predict = lr.predict(x_arr)

# Plot the Dataset
# Use `plt.subplots()` to ensure takes a `canvas` attribute
fig, ax = plt.subplots()
ax.scatter(x, y, color='red', marker='.')
ax.plot(x_arr, y_predict, color='black', linestyle='--')
ax.set_title('Example Analysis')
ax.set_xlabel('X-Axis')
ax.set_ylabel('Y-Axis')

# Calculate some metrics
r_squared = lr.score(x, y)
beta = lr.coef_[0]

# Wrap the figure in the presaltyics middleware
example_plot = presalytics.MatplotlibResponsiveFigure(fig, "Regression Example")
