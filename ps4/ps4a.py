# Problem Set 4A
# Name: <your name here>
# Collaborators:
# Time Spent: x:xx
def swap (string, pos1, pos2):
    char_list = []
    for letter in string:
        char_list.append(letter)
    holder = char_list[pos1]
    char_list[pos1] = char_list[pos2]
    char_list[pos2] = holder
    return ''.join(char_list)

def get_permutations(sequence):
    '''
    Enumerate all permutations of a given string

    sequence (string): an arbitrary string to permute. Assume that it is a
    non-empty string.  

    You MUST use recursion for this part. Non-recursive solutions will not be
    accepted.

    Returns: a list of all permutations of sequence

    Example:
    >>> get_permutations('abc')
    ['abc', 'acb', 'bac', 'bca', 'cab', 'cba']

    Note: depending on your implementation, you may return the permutations in
    a different order than what is listed here.
    '''
    permutation_list = []    
    if len(sequence) == 1:
        permutation_list.append(sequence)
        return permutation_list
    else: 
        lst = get_permutations(sequence[1::])
        for perm in lst:
            perm = sequence[0]+perm
            for x in range(len(perm)):
                permutation_list.append(swap(perm,0,x))
    return permutation_list

if __name__ == '__main__':
    print(get_permutations('aeiou'))
#    #EXAMPLE
#    example_input = 'abc'
#    print('Input:', example_input)
#    print('Expected Output:', ['abc', 'acb', 'bac', 'bca', 'cab', 'cba'])
#    print('Actual Output:', get_permutations(example_input))
