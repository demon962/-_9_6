from itertools import combinations

def all_variants(text):
    for char in text:
        yield char

    for length in range(2, len(text) + 1):
        for combo in combinations(text, length):
            yield ''.join(combo)

text = "abc"
generator = all_variants(text)

for variant in generator:
    print(variant)