list1 = ['x1', 'x2', 'x3', 'x4']
list2 = ['y1', 'y2', 'y3', 'y4']

result_list = [item for pair in zip(list1, list2) for item in pair]

# If you want to split the result into two lists again
result_list1 = result_list[:len(result_list)//2]
result_list2 = result_list[len(result_list)//2:]

print(result_list1)
print(result_list2)
