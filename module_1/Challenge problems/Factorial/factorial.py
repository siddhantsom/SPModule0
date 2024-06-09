#Script to compute the factorial of a large number

import argparse

def compute_factorial(n, filename):
    """
    Computes factorial for n and outputs it to a txt file.

    Parameters
    ----------
    n : int
    filename : str

    Returns 
    -------
    None
    """
    result = [1]

    for i in range(2, n+1):
        carry = 0
        for j in range(len(result)):
            product = result[j]*i + carry 
            result[j] = product%10
            carry = product//10
        while carry!=0:
            result.append(carry%10)
            carry = carry // 10
    
    result_string = ''.join(str(digit) for digit in reversed(result))
    print('The number of digits in the result is: ', len(result_string))
    k = len(result_string) if len(result_string)<100 else 100 #limiting digits per line in output file 
    with open(filename, 'w') as file:
        for i in range(0, len(result_string), k):
            line = result_string[i:i+k]
            file.write(line+'\n')
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--number", type = int)
    parser.add_argument("--filename", type = str)

    args = parser.parse_args()
    compute_factorial(args.number, args.filename)

if __name__ == "__main__":
    main()

#Example usage - python factorial.py --number 1000 --filename fact.txt



