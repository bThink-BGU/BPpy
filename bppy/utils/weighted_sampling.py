from random import choices
import itertools

# from https://stackoverflow.com/a/43649323

def weighted_sample_without_replacement(population, weights, k=1):
    weights = list(weights)
    positions = range(len(population))
    indices = []
    while True:
        needed = k - len(indices)
        if not needed:
            break
        for i in choices(positions, weights, k=needed):
            if weights[i]:
                weights[i] = 0.0
                indices.append(i)
    return [population[i] for i in indices]

def sequence_probability_nr_s(choice, sequence):
    total_prob = 0
    for perm in itertools.permutations(sequence):
        left_prob = 1
        cum_prob = 1
        for event in perm:
            cum_prob *= (choice[event])/left_prob
            left_prob -= choice[event]
        total_prob += cum_prob
    return (sequence, total_prob)