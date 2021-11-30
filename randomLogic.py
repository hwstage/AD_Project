import random

def tenRule(n):
    ls = [[n - 20, n - 10 , n], [n - 10, n, n + 10], [n, n + 10, n + 20]]
    return ls[random.randint(0, len(ls)- 1)]

def oneRule(n):
    ls = [[n - 2, n - 1 , n], [n - 1, n, n + 1], [n, n + 1, n + 2]]
    return ls[random.randint(0, len(ls)- 1)]

def randomRule(n):
    ls = [n, random.randint(1, 101), random.randint(1, 101)]
    return ls

def ruleSelect(n):
    ruleList = [tenRule, oneRule, randomRule]
    if n < 0 :
        ruleList = [tenRule, oneRule]
    return ruleList[random.randint(0, len(ruleList)-1)](n)