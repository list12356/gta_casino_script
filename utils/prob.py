PROB_LIST = [
    50, 33.33, 25, 20, 16.67, 14.29, 12.5, 11.11, 10,
    9.09, 8.33, 7.69, 7.14, 6.67, 6.25, 5.88, 5.56, 5.26,
    5, 4.76, 4.55, 4.35, 4.17, 4, 3.85, 3.7, 3.57, 3.45, 3.33, 3.23
]


def calc_return(odds):
    total_prob = 0
    total_reward = 0
    for odd in odds:
        total_prob += PROB_LIST[odd - 1]
    return 100/total_prob