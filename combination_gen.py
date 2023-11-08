def gen_comb_list(list_set):
    if len(list_set) == 1:
        return [[i] for i in list_set[0]]

    new_set = []
    first_list = list_set[0]
    for i in first_list:
        remaining_list = gen_comb_list(list_set[1:])
        for combine in remaining_list:
            new_set.append([i] + combine)
    return new_set


print(gen_comb_list([[1, 2, 3], [4, 5]]))