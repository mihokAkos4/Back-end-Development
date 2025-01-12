from itertools import permutations

def binary_permutations(binary_str):
    # Generate all unique permutations
    perm = set(permutations(binary_str))
    
    # Convert each permutation from tuple to string
    perm_list = [''.join(p) for p in perm]
    
    # Return the list of permutations and the number of unique permutations
    return perm_list, len(perm_list)

def is_binary(binary_str):
    # Check if the input contains only 0 or 1
    return all(char in '01' for char in binary_str)

# Get user input
binary_number = input("Enter a binary number: ")

# Check if the input is binary
if not is_binary(binary_number):
    print("Not a binary number")
else:
    perms, num_perms = binary_permutations(binary_number)
    print("Permutations:", perms)
    print("Number of unique permutations:", num_perms)
