from Levenshtein import distance


# No-split error correction
def no_split_error_correction(word, word_freq, conf):
    edit_dist = 0
    candidates = []
    edit_distances = []

    for candidate, freq in word_freq.items():
        edit_distance_to_candidate = distance(word, candidate)
        edit_distances.append([[candidate, freq], edit_distance_to_candidate])

    can, cost, freq = get_candidate(edit_distances, word, conf)

    return can, cost, freq


# Split error correction
def split_error_correction(word, word_freq, conf):
    splits = []
    candidates = []

    origin_can, origin_cost, origin_freq = no_split_error_correction(word, word_freq, conf)
    candidates.append([origin_can, origin_cost, origin_freq])

    # Split words into two
    for i in range(1, len(word)):
        splits.append([word[:i], word[i:]])

    for first, second in splits:
        first_edit_distances = []
        second_edit_distances = []

        for can, freq in word_freq.items():
            first_edit_distances.append([[can, freq], distance(first, str(can))])
            second_edit_distances.append([[can, freq], distance(second, str(can))])

        first_can, first_cost, first_freq = get_candidate(first_edit_distances, first, conf)
        second_can, second_cost, second_freq = get_candidate(second_edit_distances, second, conf)

        candidates.append([[first_can, second_can], first_cost + second_cost + 1, (first_freq + second_freq) / 2])

    b = sorted(candidates, key=lambda x: (-x[1], x[2]))
    winning_word, winning_cost, winning_freq = b[-1]

    return winning_word


def get_candidate(distance_list, word, conf):
    current_edit_distance = conf.min_edit_distance
    candidates = []
    while (current_edit_distance <= conf.max_edit_distance):
        for candidate, cost in distance_list:
            if (cost == current_edit_distance):
                candidates.append([candidate, cost])

        if (len(candidates) > 0):
            # Select candidate with greatest frequency
            winning_candidate = max(candidates, key=lambda x: int(x[1]))
            winning_word, winning_freq = winning_candidate[0]
            return winning_word, current_edit_distance, int(winning_freq)

        else:
            current_edit_distance += 1
    else:
        return word, conf.max_edit_distance, 0
