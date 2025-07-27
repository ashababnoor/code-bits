import itertools

'''
You are given two integers:
 - N: the largest number you need to construct (you must be able to construct all numbers from 1 to N).
 - M: the maximum number of distinct positive integers you are allowed to choose.

Your task is to choose a set S of at most M distinct positive integers.
For example, S = {s₁, s₂, …, sₖ} where k ≤ M.

Using the numbers in S, you need to construct every integer from 1 to N by performing the following:
 - Pick any subset of S (you can choose one, two, or all of them — or even none if allowed).
 - Assign to each number you picked a sign: either positive (+) or negative (−).
 - Each number from S can appear at most once in a construction. You cannot use the same number multiple times in a single construction.
 - Then sum up the selected signed numbers to get a result.

You must make sure that for every number x from 1 to N, there exists a choice of subset of S and signs such that the sum equals x.

In other words, the set of all sums you can generate by adding or subtracting the numbers from S (each used at most once in a construction, and any subset of S) must include all numbers from 1 to N.

The goal is to find such a set S of at most M numbers, or decide that no such set exists.
'''


def generate_all_signed_sums_with_exprs(nums):
    """
    Given a list of distinct positive integers, return a dictionary:
    key = constructible number
    value = one possible expression that evaluates to it
    """
    results = {}

    n = len(nums)
    for r in range(1, n + 1):
        for subset in itertools.combinations(nums, r):
            for signs in itertools.product([1, -1], repeat=r):
                terms = [s * sign for s, sign in zip(subset, signs)]
                total = sum(terms)
                if total == 0:
                    continue
                expr = " ".join(
                    f"{'+' if sign > 0 else '-'}{abs(num)}"
                    for num, sign in zip(subset, signs)
                ) + f" = {total}"
                if total not in results:
                    results[total] = expr
    return results

def find_valid_set(N, M, max_candidate=30):
    candidates = range(1, max_candidate + 1)

    for k in range(1, M + 1):
        for combo in itertools.combinations(candidates, k):
            expr_map = generate_all_signed_sums_with_exprs(combo)
            if all(x in expr_map for x in range(1, N + 1)):
                print(f"\n✅ Found valid set: {combo}\n")
                for i in range(1, N + 1):
                    print(f"{i}: {expr_map[i]}")
                return
    print("❌ No valid set found that can construct all numbers from 1 to", N)


def can_construct_all_numbers(numbers: list[int], N: int) -> bool:
    """
    Checks if all integers from 1 to N can be constructed using a brute-force
    approach from the given list of numbers, and prints the equations.

    Construction involves:
    1. Taking prefixes of the input list (e.g., [a], then [a, b], then [a, b, c]).
    2. For each prefix, considering all combinations of adding or subtracting
       each number in that prefix.
    3. ONLY considering sums that are strictly POSITIVE.
    4. Checking if the resulting positive sums cover all integers from 1 to N.

    Args:
        numbers: A list of integers to use for construction.
        N: The upper limit (inclusive) to check for constructible numbers.
           The function will check if all numbers from 1 to N are constructible.

    Returns:
        True if all numbers from 1 to N are constructible, False otherwise.
    """
    
    # Dictionary to store unique positive numbers and their corresponding equations.
    # Key: positive number (int), Value: equation string (str)
    reachable_numbers_with_equations = {}

    # Iterate through all possible prefixes of the input 'numbers' list.
    # A prefix of length 'i+1' includes numbers[0] up to numbers[i].
    for i in numbers:
        reachable_numbers_with_equations[i] = f"{i}"  # Initialize with the number itself
    
    for i in range(len(numbers)):
        # Get the current prefix of the list.
        current_prefix = numbers[:i+1]
        
        # Define the possible signs for each number: -1 (subtract) or +1 (add).
        signs_options = [-1, 1]
        
        # Generate all possible combinations of signs for the numbers in the current prefix.
        # For a prefix of length k, there will be 2^k sign combinations.
        for sign_combination in itertools.product(signs_options, repeat=len(current_prefix)):
            current_sum = 0
            equation_parts = []
            
            # Calculate the sum and build the equation string for the current sign combination.
            for j in range(len(current_prefix)):
                num = current_prefix[j]
                sign = sign_combination[j]
                current_sum += num * sign
                
                # Build the equation string.
                # For the first number, just add it (with its sign if negative, or positive if positive)
                if j == 0:
                    equation_parts.append(f"{num * sign}")
                else:
                    # For subsequent numbers, add "+ " or "- "
                    if sign == 1:
                        equation_parts.append(f"+ {num}")
                    else: # sign == -1
                        equation_parts.append(f"- {num}")
            
            equation_str = " ".join(equation_parts).strip()
            # Clean up the equation string: if it starts with a positive sign for the first number, remove it.
            # Example: "+1 + 2" becomes "1 + 2"
            if equation_str.startswith('+'):
                equation_str = equation_str[1:].strip()
            
            # --- IMPORTANT CHANGE HERE ---
            # Only consider the sum if it's strictly positive.
            if current_sum > 0:
                # Add the positive sum and its equation to the dictionary if not already present.
                # We only store the first equation found for a given positive number.
                if current_sum not in reachable_numbers_with_equations:
                    reachable_numbers_with_equations[current_sum] = equation_str

    print(f"\n--- Checking constructibility for N={N} with numbers {numbers} ---")
    all_constructible = True
    # After generating all possible reachable numbers, check if all integers
    # from 1 to N are present in the dictionary.
    for num in range(1, N + 1):
        if num in reachable_numbers_with_equations:
            print(f"  {num} can be constructed: {reachable_numbers_with_equations[num]} = {num}")
        else:
            print(f"  {num} CANNOT be constructed.")
            all_constructible = False
            
    return all_constructible


# --- Example Usage ---
if __name__ == "__main__":
    # Example 1: Should return True (1, 2, 3, 4, 5, 6 can be made)
    # 1: 1
    # 2: 2
    # 3: 1+2
    # 4: 1+2+3-2 = 4
    # 5: 1+2+3-1 = 5
    # 6: 1+2+3 = 6
    # numbers1 = [1, 2, 3]
    # N1 = 6
    # print(f"Result: {can_construct_all_numbers(numbers1, N1)}") # Expected: True

    # Example 2: Should return False (2 cannot be made, 1+3=4, 1-3=-2 (ignored), 3-1=2, 3)
    # This will now be True because 3-1 = 2
    # numbers2 = [1, 3]
    # N2 = 3
    # print(f"\nResult: {can_construct_all_numbers(numbers2, N2)}") # Expected: True (1, 3, 3-1=2)

    # Example 3: Larger numbers, N = 10
    # numbers3 = [5, 2, 8]
    # N3 = 10
    # Possible positive numbers:
    # Prefix [5]: 5
    # Prefix [5, 2]: 5+2=7, 5-2=3
    # Prefix [5, 2, 8]:
    # 5+2+8=15, 5+2-8=-1 (ignored), 5-2+8=11, 5-2-8=-5 (ignored)
    # -5+2+8=5, -5+2-8=-11 (ignored), -5-2+8=1, -5-2-8=-15 (ignored)
    # All reachable positive: {1, 3, 5, 7, 11, 15}
    # Missing: 2, 4, 6, 8, 9, 10
    # print(f"\nResult: {can_construct_all_numbers(numbers3, N3)}") # Expected: False

    # Example 4: Empty list
    # numbers4 = []
    # N4 = 5
    # print(f"\nResult: {can_construct_all_numbers(numbers4, N4)}") # Expected: False (cannot construct 1)

    # Example 5: N = 0
    # numbers5 = [1, 2, 3]
    # N5 = 0
    # print(f"\nResult: {can_construct_all_numbers(numbers5, N5)}") # Expected: True (no numbers from 1 to 0 to check)

    numbers6 = [1, 3, 9, 27]
    N6 = 40
    print(f"\nResult: {can_construct_all_numbers(numbers6, N6)}")

    N = 50
    M = 5
    result = find_valid_set(N, M)
