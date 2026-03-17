# import warnings
# import itertools
# import numpy as np
# import pandas as pd
# from scipy import linalg
# from scipy.stats import chi2

# # ── Lightweight Auto-ARIMA using NumPy/SciPy ─────────────────────────────────
# # pmdarima and statsmodels are not available in this environment.
# # We implement a minimal ARIMA(p,d,q) fitter using the Yule-Walker / OLS
# # approach for the AR component and log-likelihood for AIC computation.

# def _diff(series, d):
#     """Apply d-order differencing."""
#     _x = series.copy()
#     for _ in range(d):
#         _x = np.diff(_x)
#     return _x

# def _adf_pvalue(series):
#     """
#     Augmented Dickey-Fuller approximation via OLS regression
#     Returns approximate p-value (rough but adequate for d selection).
#     """
#     _y = np.array(series, dtype=float)
#     _dy = np.diff(_y)
#     _y_lag = _y[:-1]
#     _X = np.column_stack([_y_lag, np.ones(len(_y_lag))])
#     _b, _res, _, _ = np.linalg.lstsq(_X, _dy, rcond=None)
#     _n = len(_dy)
#     _sigma2 = np.sum((_dy - _X @ _b) ** 2) / (_n - 2) if _n > 2 else 1.0
#     _se_beta = np.sqrt(_sigma2 / (np.sum((_y_lag - _y_lag.mean()) ** 2) + 1e-10))
#     _tau = _b[0] / (_se_beta + 1e-10)
#     # Approximate p-value from tau statistic critical values
#     if   _tau < -3.5:  return 0.01
#     elif _tau < -2.9:  return 0.05
#     elif _tau < -2.6:  return 0.10
#     else:              return 0.99

# def _fit_arima(series, p, d, q):
#     """
#     Fit ARIMA(p,d,q) by:
#     1. Differencing d times
#     2. Using OLS to estimate AR coefficients
#     3. Computing residuals and MA via iterative filtering
#     Returns (aic, bic, residuals, ar_coefs, ma_coefs)
#     """
#     _y = np.array(series, dtype=float)
#     _yd = _diff(_y, d)
#     _n = len(_yd)
#     if _n < max(p, q) + 5:
#         return None

#     # Build lag matrix for AR estimation
#     _max_lag = max(p, q, 1)
#     _valid = _n - _max_lag
#     if _valid < 5:
#         return None

#     _Y = _yd[_max_lag:]
#     if p > 0:
#         _X_ar = np.column_stack([_yd[_max_lag - i - 1:_n - i - 1] for i in range(p)] + [np.ones(_valid)])
#     else:
#         _X_ar = np.ones((_valid, 1))

#     _b, _, _, _ = np.linalg.lstsq(_X_ar, _Y, rcond=None)
#     _resid = _Y - _X_ar @ _b

#     # Simple MA estimation: iterative residual regression
#     _ma_coefs = np.zeros(q)
#     if q > 0:
#         _eps = _resid.copy()
#         for _ in range(3):  # 3 iterations is typically enough
#             _E = np.column_stack([
#                 np.concatenate([np.zeros(i + 1), _eps[:_valid - i - 1]])
#                 for i in range(q)
#             ])
#             _b_ma, _, _, _ = np.linalg.lstsq(_E, _resid, rcond=None)
#             _ma_coefs = _b_ma
#             _resid_new = _resid - _E @ _b_ma
#             _eps = _resid_new

#         _resid = _resid_new

#     # Log-likelihood, AIC, BIC
#     _sigma2 = np.var(_resid) + 1e-10
#     _loglik = -0.5 * _valid * (np.log(2 * np.pi * _sigma2) + 1)
#     _k = p + q + 1 + (1 if p == 0 else 0)  # params: AR + MA + intercept + sigma
#     _aic = -2 * _loglik + 2 * _k
#     _bic = -2 * _loglik + _k * np.log(_valid)

#     return {
#         'aic': _aic,
#         'bic': _bic,
#         'residuals': _resid,
#         'ar_coefs': _b[:p] if p > 0 else np.array([]),
#         'ma_coefs': _ma_coefs,
#         'sigma2': _sigma2,
#         'n': _valid,
#         'loglik': _loglik,
#     }

# def auto_arima(series, max_p=3, max_d=2, max_q=3,
#                information_criterion='aic', verbose=True):
#     """
#     Automated ARIMA order selection via grid search on AIC/BIC.
#     Uses pure NumPy/SciPy — no external time-series libraries required.

#     Parameters
#     ----------
#     series : array-like     – univariate time series
#     max_p, max_d, max_q     – upper bounds for ARIMA orders
#     information_criterion   – 'aic' or 'bic'
#     verbose                 – print progress

#     Returns
#     -------
#     dict: order, aic, bic, residuals, ar_coefs, ma_coefs
#     """
#     _s = pd.Series(series).dropna().values

#     # Select differencing order d
#     best_d = 0
#     for _d in range(max_d + 1):
#         _sd = _diff(_s, _d)
#         if len(_sd) < 4:
#             break
#         _pval = _adf_pvalue(_sd)
#         if _pval < 0.05:
#             best_d = _d
#             break
#         best_d = _d

#     _candidates = list(itertools.product(range(max_p + 1), [best_d], range(max_q + 1)))
#     if verbose:
#         print(f"Auto-ARIMA: d={best_d}, searching {len(_candidates)} (p,d,q) combinations …")

#     best_ic    = np.inf
#     best_fit   = None
#     best_order = (0, best_d, 0)

#     for _order in _candidates:
#         _fit = _fit_arima(_s, *_order)
#         if _fit is None:
#             continue
#         _ic = _fit[information_criterion]
#         if _ic < best_ic:
#             best_ic    = _ic
#             best_fit   = _fit
#             best_order = _order

#     if best_fit:
#         best_fit['order'] = best_order

#     return best_fit


# # ── Run on total annual visits across all branches ────────────────────────────
# annual_ts = (
#     df_visits
#     .groupby('Year')['Visits']
#     .sum()
#     .sort_index()
# )

# print("Annual visits time series:")
# print(annual_ts.to_string())
# print()

# arima_result = auto_arima(annual_ts.values, max_p=3, max_d=2, max_q=3, verbose=True)
# best_order   = arima_result['order']
# arima_model  = arima_result  # dict acting as the fitted model

# print(f"\n✅ Best ARIMA order : {best_order}")
# print(f"   AIC             : {arima_result['aic']:.4f}")
# print(f"   BIC             : {arima_result['bic']:.4f}")
# print(f"   Log-likelihood  : {arima_result['loglik']:.4f}")
# print(f"   σ²              : {arima_result['sigma2']:.4f}")
# if len(arima_result['ar_coefs']) > 0:
#     print(f"   AR coefficients : {np.round(arima_result['ar_coefs'], 4)}")
# if len(arima_result['ma_coefs']) > 0:
#     print(f"   MA coefficients : {np.round(arima_result['ma_coefs'], 4)}")
