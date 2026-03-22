col1 = set(map(int, input().split()))
col2 = set(map(int, input().split()))
res = col1 & col2
res = filter(lambda x: not x % 2, res)
print(*sorted(res))
