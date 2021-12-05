
def calculate_reward(user_id: int , recommended: list):
    reward = 0
    # items reccomended first valued more importantly
    position_weights = []
    weight = 1
    length = len(recommended)
    for i in range(length):
        position_weights.insert(0, weight)
        weight += 1
    for article in recommended:
        position = article[5]
        pos_weight = position_weights[position]
        # if clicked on
        if article[3]:
            reward += 1 * pos_weight
        else:
            reward -= 1 * pos_weight
        # check if rated
        rated = article[5]
        if rated:
            rating = article[7]
            if rating >= 3:
                reward += rating * pos_weight
            else:
                reward -= rating * pos_weight
