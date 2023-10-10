from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

ABase = And(
    Or(AKnave, AKnight),
    Not(And(AKnight,AKnave))
)

BBase = And(
    Or(BKnave, BKnight),
    Not(And(BKnight,BKnave))
)

CBase = And(
    Or(CKnave, CKnight),
    Not(And(CKnight,CKnave))
)

def ASays(Sentence):
    return And(
        Implication(AKnight, Sentence),
        Implication(AKnave, Not(Sentence))
    )

def BSays(Sentence):
    return And(
        Implication(BKnight, Sentence),
        Implication(BKnave, Not(Sentence))
    )

def CSays(Sentence):
    return And(
        Implication(CKnight, Sentence),
        Implication(CKnave, Not(Sentence))
    )

# A knight will always tell the truth
# A knave will always lie

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    ABase,
    ASays(And(AKnave, AKnight))
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    ABase,
    BBase,
    ASays(And(AKnave, BKnave))
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    ABase,
    BBase,
    ASays(And(Biconditional(AKnave,BKnave), Biconditional(AKnight,BKnight))),
    BSays(And(Biconditional(AKnave,BKnight), Biconditional(AKnight,BKnave)))
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    ABase,
    BBase,
    CBase,
    Or(ASays(AKnight), ASays(AKnave)),
    BSays(ASays(AKnave)),
    BSays(CKnave),
    CSays(AKnight)
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
