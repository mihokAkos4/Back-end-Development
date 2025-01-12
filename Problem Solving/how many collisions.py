numbers = [1,45,5,34,23,5,82,12,35,21,8,9]
mod_list = [n % 6 for n in numbers]  # Hash values using modulus 7

collisions = 0
for i in set(mod_list):  # Iterate through unique hash values
    count = 0
    for j in mod_list:  # Count occurrences of each hash value
        if i == j:
            count += 1
    if count > 1:  # A collision occurs if a hash value appears more than once
        collisions += count - 1

print(f"Total collisions: {collisions}")
