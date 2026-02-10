def check_var_breach(var, limit=-0.02):
    if var < limit:
        return "🔴 VaR Breach Detected"
    return "🟢 VaR Within Limits"
