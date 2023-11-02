import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


# 2
dec_log = pd.read_csv(r'c:\Users\MSI\Desktop\study\pandas\data-analysis-pandas-main\solutions\ch_08\dec_2018_log.csv', parse_dates=True, index_col='datetime')

log_aggs = dec_log.assign(
    failures=lambda x: np.invert(x.success)
).groupby('source_ip').agg(
    {'username': 'nunique', 'success': 'sum', 'failures': 'sum'}
).assign(
    attempts=lambda x: x.success + x.failures,
    success_rate=lambda x: x.success / x.attempts,
    failure_rate=lambda x: 1 - x.success_rate
).dropna().reset_index()

log_aggs.head()

# 3 
is_attack_ip = log_aggs.source_ip.isin(
    pd.read_csv('dec_2018_attacks.csv').source_ip
)

fig, axes = plt.subplots(1, 2, figsize=(10, 3))

for ax, (x, y) in zip(axes, (('attempts', 'failures'), ('username', 'failure_rate'))):
    ax = sns.scatterplot(
        x=log_aggs[x], 
        y=log_aggs[y], 
        hue=is_attack_ip,
        ax=ax
    )
    ax.set_title(f'{y.title()} vs. {x.title()}')

# boundaries
axes[0].plot([0, 80], [80, 0], 'r--')
axes[1].axhline(0.5, color='red', linestyle='--')


# 4
hourly_ip_logs = dec_log.assign(
    failures=lambda x: np.invert(x.success)
).groupby('source_ip').resample('1H').agg(
    {'username': 'nunique', 'success': 'sum', 'failures': 'sum'}
).assign(
    attempts=lambda x: x.success + x.failures,
    success_rate=lambda x: x.success / x.attempts,
    failure_rate=lambda x: 1 - x.success_rate
).dropna().reset_index()

hourly_ip_logs.head()

def get_baselines(hourly_ip_logs, func, *args, **kwargs):

    if isinstance(func, str):
        func = getattr(pd.DataFrame, func)

    return hourly_ip_logs.assign(
        hour=lambda x: x.datetime.dt.hour
    ).groupby('hour').apply(
        lambda x: x.sample(10, random_state=0, replace=True).pipe(func, *args, **kwargs, numeric_only=True)
    )

medians = get_baselines(hourly_ip_logs, 'median')

flagged_ips = hourly_ip_logs.assign(
    hour=lambda x: x.datetime.dt.hour
).join(
    medians, on='hour', rsuffix='_median'
).assign(
    flag_median=lambda x: np.logical_or(
        np.logical_and(
            x.failures_median * 5 <= x.failures,
            x.attempts_median * 5 <= x.attempts
        ), x.username_median * 5 <= x.username
    )
).query('flag_median').source_ip.drop_duplicates()

# 5
def evaluate(alerted_ips, attack_ips, log_ips):

    tp = alerted_ips.isin(attack_ips).sum()
    tn = np.invert(np.isin(log_ips[~log_ips.isin(alerted_ips)].unique(), attack_ips)).sum()
    fp = np.invert(
        np.isin(log_ips[log_ips.isin(alerted_ips)].unique(), attack_ips)
    ).sum()
    fn = np.invert(
        np.isin(log_ips[log_ips.isin(attack_ips)].unique(), alerted_ips)
    ).sum()
    return tp, fp, tn, fn


from functools import partial
scores = partial(
    evaluate, 
    attack_ips=pd.read_csv('dec_2018_attacks.csv').source_ip, 
    log_ips=dec_log.source_ip.drop_duplicates()
)

def classification_stats(tp, fp, tn, fn):
    return {
        'FPR': fp / (fp + tn),
        'FDR': fp / (fp + tp),
        'FNR': fn / (fn + tp),
        'FOR': fn / (fn + tn)
    }

classification_stats(*scores(flagged_ips))