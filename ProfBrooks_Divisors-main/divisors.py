def divisors(num):
    possibles = list(range(1, num+1))

    divisorList = []

    for number in possibles:
        if num % number == 0:
            divisorList.append(number)

    return divisorList
