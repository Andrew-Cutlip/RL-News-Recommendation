
def calculate_reward(user_id: int , recommended: list):
    reward = 0
    # items recommended first valued more importantly
    position_weights = []
    weight = 1
    length = len(recommended)
    for i in range(length):
        position_weights.insert(0, weight)
        weight += 1
    for article in recommended:
        position = article[6]
        pos_weight = position_weights[position]
        # if clicked on
        if article[3]:
            reward += 1 * pos_weight
        else:
            reward -= 1 * pos_weight
        # check if rated
        rated = article[4]
        if rated:
            rating = article[6]
            if rating == 5:
                reward += 10 * pos_weight
            elif rating == 4:
                reward += 5 * pos_weight
            elif rating == 3:
                reward += pos_weight
            elif rating == 2:
                reward -= 5 * pos_weight
            else:
                reward -= 10 * pos_weight

    return reward
