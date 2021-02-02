# File for writing functions that may not be needed

def get_highest_bid(all_bids):
    max = 0
    for bid in all_bids:
        price = bid.bid_price
        if price > max:
            max = price
    return max 
