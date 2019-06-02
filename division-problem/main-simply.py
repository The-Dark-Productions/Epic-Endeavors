import threading

"""
The main idea is to try different element of the list when we divide the number for the first time. 
Since the next element of the list only divides the remainder of previous division operation, using different divisors 
for first operation will yield different outcomes every time.
We'll store them and get the one with lowest elements.

We'll use threading to speedup the operation.
"""

weights = [[11, 9, 7, 5, 1]]                                        # List of lists with different first elements.
results = []                                                        # To hold all possible outcomes.

for i in range(1, 5):                                               # Creating lists with different first element.
    current_list = [11, 9, 7, 5, 1]
    current_list.insert(0, current_list.pop(i))
    weights.append(current_list)

threads = []                                                        # Creating array to store all the threads created.


def get_result():
    for entry in weights:                                           # Creating threads for every list entry.
        threads.append(threading.Thread(target=calculate(entry)))
        threads[-1].start()

    for t in threads:                                               # Waiting for every thread to finish.
        t.join()

    for entry in weights:                                           # Appending outcomes. (refer - line 46)
        results.append(entry[-1])

    print("\nAll possible outcomes : " + repr(results))             # Displaying all possible outcomes.
    return min(results)                                             # Finding the minimum of all outcomes.


def calculate(selected_list):                                       # Calculating total weights required to get number.
    remainder = number                                              # Initiating remainder = number.
    total = 0

    for divisor in selected_list:                                   # Iterating through divisors (list entries).
        quotient, remainder = divmod(int(remainder), int(divisor))
        total += quotient
        selected_list[selected_list.index(divisor)] = [divisor, quotient]   # Adding quotient along with the divisor.
    selected_list.append(total)                                     # Appending total(outcome) at the end of list.


number = 20                                                         # Play with input
min_cost = repr(get_result())
print("\nMinimum Cost : " + min_cost)
print("Weights :")

for entry in weights:
    if min_cost == repr(entry[-1]):                                 # Find the entry with min_cost and display.
        print(entry[:-1])

