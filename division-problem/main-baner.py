num = [11, 9, 7, 5, 1]
num.sort(reverse=True)


def divide(dividend, divisor_index=0, weights={k: 0 for k in num}):
    """
    The function returns False when it encounters a combination of weights which is
    worse than previously acquired results.
    """
    global global_min_count
    if sum(weights.values()) > global_min_count:
        return False
    quotient = dividend // num[divisor_index]
    remainder = dividend % num[divisor_index]

    if remainder == 0:
        weights[num[divisor_index]] = quotient
        return weights

    weights_list = []
    for count in range(quotient, -1, -1):
        temp_weights = {k: 0 for k in num}
        for i in range(divisor_index + 1):
            temp_weights[num[i]] = weights[num[i]]
        temp_weights[num[divisor_index]] = count
        temp_remainder = dividend - num[divisor_index]*count
        result = divide(temp_remainder, divisor_index + 1, temp_weights)
        if result is not False:
            weights_list.append(result)

    if len(weights_list) == 0:
        return False

    best_weight = False
    for weight in weights_list:
        if sum(weight.values()) <= global_min_count:
            global_min_count = sum(weight.values())
            best_weight = weight
    return best_weight


number = 198
global_min_count = number
weights = divide(number)
print("\nCost: {}\n".format(sum(weights.values())))
print("Weights")
for value, occurrence in weights.items():
    print(f"{value} : {occurrence}")
