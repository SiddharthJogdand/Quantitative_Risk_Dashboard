from scipy.stats import norm
import numpy as np

class GreeksEngine:

    def black_scholes_delta(self, S, K, T, r, sigma, option="call"):
        d1 = (np.log(S/K) + (r + 0.5*sigma**2)*T) / (sigma*np.sqrt(T))
        if option == "call":
            return norm.cdf(d1)
        else:
            return -norm.cdf(-d1)
