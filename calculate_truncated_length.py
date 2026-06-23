# 计算被截断的XSS payload长度
payload = '<img src=x onerror=alert("XSS"'
print(f'Truncated payload: {payload}')
print(f'Truncated payload length: {len(payload)}')
