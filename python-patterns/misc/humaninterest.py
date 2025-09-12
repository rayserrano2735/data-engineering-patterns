def insertOrder(lst, num):
    lst.append(num)
    lst.sort()
    return lst

def insertOrder(lst, num):
    # Binary search to find insertion point
    left, right = 0, len(lst)

    while left < right:
        mid = (left + right) // 2
        if lst[mid] < num:
            left = mid + 1
        else:
            right = mid

    lst.insert(left, num)
    return lst


2.

def checkOrder(lst):
    for i in range(1, len(lst)):
        if lst[i] < lst[i-1]:
            return False
    return True