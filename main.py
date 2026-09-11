# ============================================================
# AXIOMATIC SYSTEM — PYTHON EQUIVALENT
# ============================================================


# ------------------------------------------------------------
# 1. BASE SET
# ------------------------------------------------------------

# P0 = ∅
P0 = []


# ------------------------------------------------------------
# 2. CARDINALITY FUNCTION
# E(P) = |P|
# ------------------------------------------------------------

def E(P):
    return len(P)


# ------------------------------------------------------------
# 3. SUCCESSOR FUNCTION
#
# S(P) = P ∪ {αn}, where αn ∉ P
#
# IMPORTANT:
# We return a NEW list instead of modifying P.
# This keeps the input representation unchanged.
# ------------------------------------------------------------

def S(P):

    # Make a copy so P itself is not changed
    new_P = P.copy()

    # Choose a new unique element αn
    if E(new_P) == 0:
        alpha_n = 1
    else:
        alpha_n = max(new_P) + 1

    new_P.append(alpha_n)

    return new_P


# ------------------------------------------------------------
# 4. ITERATED SUCCESSOR
#
# S^k(P)
# ------------------------------------------------------------

def S_iterated(P, k):

    result = P.copy()

    for _ in range(k):
        result = S(result)

    return result


# ------------------------------------------------------------
# CONSTRUCT P1, P2, P3, ...
# ------------------------------------------------------------

P1 = S(P0)
P2 = S(P1)
P3 = S(P2)
P4 = S(P3)
P5 = S(P4)


# Check:
#
# E(P0) = 0
# E(P1) = 1
# E(P2) = 2
# etc.

print(E(P0))  # 0
print(E(P1))  # 1
print(E(P2))  # 2


# ============================================================
# DEFINING ADDITION
# ============================================================
#
# A(P1, P2) = E(S^(E(P2))(P1))
#
# In other words:
#
# Start with P1
# Apply S exactly E(P2) times
# Return the cardinality
# ------------------------------------------------------------

def A(P1, P2):

    result = P1.copy()

    for _ in range(E(P2)):
        result = S(result)

    return E(result)


# Example from paper:
#
# 1 + 2 = 3

print(A(P1, P2))  # 3
print(A(P2, P1))  # 3


# ============================================================
# SUBTRACTION ON NATURAL NUMBERS
# ============================================================


# ------------------------------------------------------------
# ELEMENT REMOVAL FUNCTION
#
# N(P) removes exactly one unique element.
# ------------------------------------------------------------

def N(P):

    if E(P) == 0:
        raise ValueError("N(P) is undefined for the empty set.")

    new_P = P.copy()

    # Remove exactly one element
    new_P.pop()

    return new_P


# ------------------------------------------------------------
# ITERATED REMOVAL
#
# N^k(P)
# ------------------------------------------------------------

def N_iterated(P, k):

    result = P.copy()

    for _ in range(k):
        result = N(result)

    return result


# ------------------------------------------------------------
# NATURAL SUBTRACTION
#
# D(P1, P2)
#
# Defined only if:
#
# E(P2) <= E(P1)
#
# D(P1,P2) = E(N^(E(P2))(P1))
# ------------------------------------------------------------

def D(P1, P2):

    if E(P2) > E(P1):
        raise ValueError(
            "Natural subtraction requires E(P2) <= E(P1)."
        )

    result = P1.copy()

    for _ in range(E(P2)):
        result = N(result)

    return E(result)


# Example:
#
# 3 - 1 = 2

print(D(P3, P1))  # 2


# ============================================================
# CONSTRUCTING NEGATIVE NUMBERS
# ============================================================


# ------------------------------------------------------------
# REDUCTION FUNCTION
#
# R[(Px, Py)]
#
# Remove one element from BOTH sets until one becomes empty.
#
# Then:
#
# Px remaining -> positive
# Py remaining -> negative
# both empty   -> zero
# ------------------------------------------------------------

def R(pair):

    Px, Py = pair

    Px = Px.copy()
    Py = Py.copy()

    # Repeatedly remove one element from both
    while E(Px) > 0 and E(Py) > 0:

        Px = N(Px)
        Py = N(Py)

    # Positive result
    if E(Px) > 0:
        return E(Px)

    # Negative result
    if E(Py) > 0:
        return -E(Py)

    # Both empty
    return 0


# ------------------------------------------------------------
# EXAMPLES FROM PAPER
# ------------------------------------------------------------

# 1 - 2 = -1
print(R((P1, P2)))  # -1

# 2 - 1 = 1
print(R((P2, P1)))  # 1

# 2 - 2 = 0
print(R((P2, P2)))  # 0


# ============================================================
# SIGNED PAIR REPRESENTATIONS
# ============================================================
#
# Positive n:
#
# (Pn, P0)
#
# Negative n:
#
# (P0, Pn)
#
# Examples:
#
#  2 -> (P2, P0)
# -2 -> (P0, P2)
# ------------------------------------------------------------


positive_2 = (P2, P0)
negative_2 = (P0, P2)


# ============================================================
# HELPER:
#
# Construct Pn from an integer n >= 0
#
# Pn = S^n(P0)
# ============================================================

def make_P(n):

    if n < 0:
        raise ValueError("Pn requires n >= 0.")

    return S_iterated(P0, n)


# Examples:
#
# make_P(3) = P3
# make_P(100) = P100


# ============================================================
# ADDITION OF SIGNED PAIRS
# ============================================================
#
# For:
#
# (Pa, Pb)
# (Pc, Pd)
#
# positive side:
#
# A(Pa, Pc)
#
# negative side:
#
# A(Pb, Pd)
#
# Then construct:
#
# Ppos = S^(A(Pa,Pc))(P0)
# Pneg = S^(A(Pb,Pd))(P0)
#
# Finally reduce:
#
# R[(Ppos, Pneg)]
# ------------------------------------------------------------

def Add(pair1, pair2):

    Pa, Pb = pair1
    Pc, Pd = pair2

    # Determine total positive quantity
    positive_count = A(Pa, Pc)

    # Determine total negative quantity
    negative_count = A(Pb, Pd)

    # Construct the corresponding sets
    Ppos = S_iterated(P0, positive_count)
    Pneg = S_iterated(P0, negative_count)

    # Reduce
    return R((Ppos, Pneg))


# ============================================================
# SUBTRACTION OF SIGNED PAIRS
# ============================================================
#
# For:
#
# (Pa, Pb) - (Pc, Pd)
#
# positive side:
#
# A(Pa, Pd)
#
# negative side:
#
# A(Pb, Pc)
#
# Then reduce.
# ------------------------------------------------------------

def Subtract(pair1, pair2):

    Pa, Pb = pair1
    Pc, Pd = pair2

    positive_count = A(Pa, Pd)
    negative_count = A(Pb, Pc)

    Ppos = S_iterated(P0, positive_count)
    Pneg = S_iterated(P0, negative_count)

    return R((Ppos, Pneg))


# ============================================================
# EXACT EXAMPLES FROM THE PAPER
# ============================================================


# ------------------------------------------------------------
# 1. (-2) + (-1) = -3
#
# -2 = (P0, P2)
# -1 = (P0, P1)
# ------------------------------------------------------------

result1 = Add(
    (P0, P2),
    (P0, P1)
)

print(result1)      # -3


# ------------------------------------------------------------
# 2. (-2) + 1 = -1
# ------------------------------------------------------------

result2 = Add(
    (P0, P2),
    (P1, P0)
)

print(result2)      # -1


# ------------------------------------------------------------
# 3. 1 - 2 = -1
# ------------------------------------------------------------

result3 = Subtract(
    (P1, P0),
    (P2, P0)
)

print(result3)      # -1


# ------------------------------------------------------------
# 4. 1 - (-2) = 3
# ------------------------------------------------------------

result4 = Subtract(
    (P1, P0),
    (P0, P2)
)

print(result4)      # 3


# ============================================================
# OPTIONAL HELPER FUNCTIONS
# ============================================================


# Convert an ordinary integer into your signed-pair system.
#
# This is NOT part of the proof itself.
# It is just useful for testing the implementation.

def integer_to_pair(n):

    if n >= 0:
        return (make_P(n), P0)

    else:
        return (P0, make_P(-n))


# Interpret one of your signed pairs.

def pair_to_integer(pair):
    return R(pair)


# Example:
#
# -17 represented using your system

x = integer_to_pair(-17)

print(x)

print(pair_to_integer(x))  # -17


# ============================================================
# MORE TESTS
# ============================================================

for a in range(-5, 6):

    for b in range(-5, 6):

        pair_a = integer_to_pair(a)
        pair_b = integer_to_pair(b)

        our_addition = Add(pair_a, pair_b)
        normal_addition = a + b

        our_subtraction = Subtract(pair_a, pair_b)
        normal_subtraction = a - b

        assert our_addition == normal_addition
        assert our_subtraction == normal_subtraction


print("All tests passed.")