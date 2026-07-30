import pandas as pd
import numpy as np
from sklearn.metrics import roc_curve


def lift_func(model, test_proc, test_target):

    prob_yes = model.predict_proba(test_proc)[:, 1]
    test_set_target_encoded = (test_target == 'yes').astype(int)
    fpr, tpr, thresholds = roc_curve(test_set_target_encoded, prob_yes)
    lift_df = pd.DataFrame({"propensity":prob_yes, "outcome":test_set_target_encoded})
    lift_sorted = lift_df.sort_values("propensity",ascending=False)
    lift_sorted['conversion_rate']=lift_sorted['outcome'].expanding().mean()

    lift_sorted['LIFT'] = lift_sorted['conversion_rate']/lift_sorted['outcome'].mean()
    lift_sorted['depth'] = (1 - lift_sorted['propensity']).rank(pct=True)
    return(lift_sorted)