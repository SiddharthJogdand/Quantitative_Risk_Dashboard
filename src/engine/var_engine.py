import numpy as np
import pandas as pd

class VaREngine:

    def __init__(self, portfolio, returns):
        self.portfolio = portfolio
        self.returns = returns

    def _portfolio_returns(self):
        total_value = (self.portfolio.quantity * self.portfolio.current_price).sum()
        weights = {}

        for _, row in self.portfolio.iterrows():
            weights[row.instrument_id] = (
                row.quantity * row.current_price
            ) / total_value

        port_returns = pd.Series(0, index=self.returns.index)
        for inst, w in weights.items():
            port_returns += w * self.returns[inst]

        return port_returns

    def historical_var(self, confidence=0.95):
        pr = self._portfolio_returns()
        var = np.percentile(pr, (1-confidence)*100)
        es = pr[pr <= var].mean()
        return var, es

    def monte_carlo_var(self, confidence=0.95, n_sim=10000):
        pr = self._portfolio_returns()
        mu, sigma = pr.mean(), pr.std()

        sims = np.random.normal(mu, sigma, n_sim)
        var = np.percentile(sims, (1-confidence)*100)
        es = sims[sims <= var].mean()
        return var, es
    
    def parametric_var(self, confidence=0.95):
        pr = self._portfolio_returns()
        mu = pr.mean()
        sigma = pr.std()

        from scipy.stats import norm
        z = norm.ppf(1 - confidence)

        var = mu + z * sigma
        es = mu - sigma * (norm.pdf(z) / (1 - confidence))

        return var, es

    def rolling_var(self, window=252, confidence=0.95):
        pr = self._portfolio_returns()
        rolling_vars = pr.rolling(window).apply(
            lambda x: np.percentile(x, (1-confidence)*100),
            raw=True
        )
        return rolling_vars

    def backtest_var(self, confidence=0.95, window=252):
        pr = self._portfolio_returns()
        rolling_var = self.rolling_var(window, confidence)

        breaches = pr < rolling_var
        breach_count = breaches.sum()

        return rolling_var, breaches, breach_count

    def component_var(self, confidence=0.95):
        pr = self._portfolio_returns()
        total_value = (self.portfolio.quantity * self.portfolio.current_price).sum()

        weights = {}
        for _, row in self.portfolio.iterrows():
            weights[row.instrument_id] = (
                row.quantity * row.current_price
            ) / total_value

        cov_matrix = self.returns.cov()
        portfolio_var = np.dot(
            list(weights.values()),
            np.dot(cov_matrix, list(weights.values()))
        )

        marginal_contrib = np.dot(cov_matrix, list(weights.values())) / np.sqrt(portfolio_var)

        component_contrib = {
            asset: weights[asset] * mc
            for asset, mc in zip(weights.keys(), marginal_contrib)
        }

        return component_contrib
    
    def component_var(self):
        import numpy as np
        import pandas as pd

        total_value = (self.portfolio.quantity * self.portfolio.current_price).sum()

        weights = {}
        for _, row in self.portfolio.iterrows():
            weights[row.instrument_id] = (
                row.quantity * row.current_price
            ) / total_value

        weights_vector = np.array(list(weights.values()))

        cov_matrix = self.returns.cov().values

        portfolio_variance = weights_vector.T @ cov_matrix @ weights_vector

        marginal_contrib = cov_matrix @ weights_vector / np.sqrt(portfolio_variance)

        component_contrib = weights_vector * marginal_contrib

        contrib_series = pd.Series(
            component_contrib,
            index=list(weights.keys())
        )

        return contrib_series.sort_values(ascending=False)

    def cumulative_returns(self):
        pr = self._portfolio_returns()
        cumulative = (1 + pr).cumprod()
        return cumulative

    def drawdown(self):
        cumulative = self.cumulative_returns()
        running_max = cumulative.cummax()
        drawdown = (cumulative - running_max) / running_max
        return drawdown
