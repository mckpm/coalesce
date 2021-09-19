from random import choice

# Strategies

def average(rs):
    """Average the values for each key."""
    data = gather_values(rs)
    return {k:int(sum(v)/len(v)) for (k,v) in data.items()}

def minimum(rs):
    """Choose the smallest number for each key."""
    data = gather_values(rs)
    return {k:min(v) for (k,v) in data.items()}

def maximum(rs):
    """Choose the largest number for each key."""
    data = gather_values(rs)
    return {k:max(v) for (k,v) in data.items()}

def frequent(rs):
    """Use the most frequently appearing value for each key."""
    data = gather_values(rs)
    return {k:freq_helper(v) for (k,v) in data.items()}

def random(rs):
    """Chooses a random value for each key."""
    data = gather_values(rs)
    return {k:choice(v) for (k,v) in data.items()}

def random2(rs):
    """Returns a randomly chosen set of source data."""
    return choice(rs)

# Helpers

def gather_values(rs):
    """Gather all values for every key."""
    all_data = {}
    for r in rs:
        for k, v in r.items():
            if k in all_data:
                all_data[k].append(v)
            else:
                all_data[k] = [v]
    return all_data

def freq_helper(xs):
    """Get most frequently appearing element in a list."""
    counts = {}
    for x in xs:
        counts[x] = counts.get(x, 0) + 1
    return max(counts, key=lambda x: counts[x])
