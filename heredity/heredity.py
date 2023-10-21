import csv
import itertools
import sys

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def gets_gene_from_parent(people, person, one_gene, two_genes):
    """
    Returns probability of person getting the gene from each parent
    """
    from_m = 0
    from_f = 0
    
    # pass the trait gene AND NOT mutated + pass the NOT trait gene AND mutated
    if people[person]["mother"] in one_gene:
        # 0.5 * (1 - MUT) + 0.5 * MUT
        from_m = 0.5
    elif people[person]["mother"] in two_genes:
        # 1 * (1 - MUT) + 0 * MUT
        from_m = 1 - PROBS["mutation"]
    else:  # people[person]["mother"] in zero_genes:
        # 0 * (1 - MUT) + 1 * MUT
        from_m = PROBS["mutation"]
    
    if people[person]["father"] in one_gene:
        # 0.5 * (1 - MUT) + 0.5 * MUT
        from_f = 0.5
    elif people[person]["father"] in two_genes:
        # 1 * (1 - MUT) + 0 * MUT
        from_f = 1 - PROBS["mutation"]
    else:  # people[person]["father"] in zero_genes:
        # 0 * (1 - MUT) + 1 * MUT
        from_f = PROBS["mutation"]

    return from_m, from_f


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """
    jp = 1

    for person in people:
        if people[person]["mother"] is None or people[person]["father"] is None:  # person is a parent
            if person in one_gene:
                if person in have_trait:
                    # prob of ONE copy of the gene and HAS the trait
                    jp *= PROBS["gene"][1] * PROBS["trait"][1][True]
                else:  # person has no trait
                    # prob of ONE copy of the gene and does NOT have the trait
                    jp *= PROBS["gene"][1] * PROBS["trait"][1][False]
            elif person in two_genes:
                if person in have_trait:
                    # prob of TWO copies of the gene and HAS the trait
                    jp *= PROBS["gene"][2] * PROBS["trait"][2][True]
                else:  # person has no trait
                    # prob of TWO copies of the gene and does NOT have the trait
                    jp *= PROBS["gene"][2] * PROBS["trait"][2][False]
            else:  # person has 0 copies of the gene
                if person in have_trait:
                    # prob of ZERO copies of the gene and HAS the trait
                    jp *= PROBS["gene"][0] * PROBS["trait"][0][True]
                else:  # person has no trait
                    # prob of ZERO copies of the gene and does NOT have the trait
                    jp *= PROBS["gene"][0] * PROBS["trait"][0][False]
        
        else:  # person is a child
            from_m, from_f = gets_gene_from_parent(people, person, one_gene, two_genes)
            
            if person in one_gene: 
                # gets the gene from mother and not father OR gets the gene from father and not mother
                jp *= (from_m * (1 - from_f)) + (from_f * (1 - from_m))

                if person in have_trait:
                    # given that has 1 copy of the gene, multply by prob of HAVING the trait
                    jp *= PROBS["trait"][1][True]
                else:  # person has no trait
                    # given that has 1 copy of the gene, multply by prob of NOT having the trait
                    jp *= PROBS["trait"][1][False]

            elif person in two_genes:
                # gets the gene from mother AND gets the gene from father
                jp *= (from_m * from_f)

                if person in have_trait:
                    # given that has 2 copies of the gene, multply by prob of HAVING the trait
                    jp *= PROBS["trait"][2][True]
                else:  # person has no trait
                    # given that has 2 copies of the gene, multply by prob of NOT having the trait
                    jp *= PROBS["trait"][2][False]

            else:  # person has 0 copies of the gene
                # does NOT get the gene from mother AND does NOT get the gene from father
                jp *= (1 - from_m) * (1 - from_f)
                
                if person in have_trait:
                    # given that has 0 copies of the gene, multply by prob of HAVING the trait
                    jp *= PROBS["trait"][0][True]
                else:  # person has no trait
                    # given that has 0 copies of the gene, multply by prob of NOT having the trait
                    jp *= PROBS["trait"][0][False]

    return jp


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    for person in probabilities:
        num_genes = 1 if person in one_gene else 2 if person in two_genes else 0
        has_trait = True if person in have_trait else False
        probabilities[person]["gene"][num_genes] += p
        probabilities[person]["trait"][has_trait] += p


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    for person in probabilities:
        # normalize "gene" distribution
        norm = probabilities[person]["gene"][0] + probabilities[person]["gene"][1] + probabilities[person]["gene"][2]
        probabilities[person]["gene"][0] /= norm
        probabilities[person]["gene"][1] /= norm
        probabilities[person]["gene"][2] /= norm

        # normalize "trait" distribution
        norm = probabilities[person]["trait"][True] + probabilities[person]["trait"][False]
        probabilities[person]["trait"][True] /= norm
        probabilities[person]["trait"][False] /= norm


if __name__ == "__main__":
    main()
