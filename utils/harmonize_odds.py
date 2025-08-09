import numpy as np

def harmonize_odds(pred_odds, target_overround=1.1, round_decimals=2, eps=1e-9):
    """
    Pred_odds: list/np.array of predicted odds, e.g. [odds1, oddsX, odds2]
    target_overround: if None -> normalize to sum=1 (no margin).
                     if >1 -> impose that sum(prob)=target_overround (bookmaker style)
                     if None, target_overround = 1.0 (i.e. probabilities sum to 1)
    return: list of harmonized odds
    """
    pred_odds = np.array(pred_odds, dtype=float)
    # Avoid division by zero
    pred_odds = np.maximum(pred_odds, eps)
    
    p = 1.0 / pred_odds

    
    sum_p = p.sum()
    if sum_p <= 0:
        raise ValueError("Non-positive implied probability sum")

    p_norm = p / sum_p  

    p_target = p_norm * target_overround

    new_odds = 1.0 / p_target

    
    new_odds = np.round(new_odds, round_decimals)

    return new_odds.tolist()
