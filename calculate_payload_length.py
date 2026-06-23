# 计算payload的长度
payload = '<img src=x onerror=alert("XSS"'
print(f'Payload: {payload}')
print(f'Character length: {len(payload)}')
print(f'Byte length (UTF-8): {len(payload.encode("utf-8"))}')
