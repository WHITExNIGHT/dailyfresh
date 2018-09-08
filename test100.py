n = int(input('n='))
num = []
for i in range(n + 1):
    num.append([])
for i in range(n + 1):
    num[i] = i
m = 1
while len(num) - 1 != 1:
    m += 2
    if m > len(num) - 1:
        m = m - len(num) - 1
    tem = num[m]
    num.remove(tem)
print(num[1])
