# 计算完整payload的长度
full_payload = '<img src=x onerror=alert("XSS")>'
print(f'Full payload: {full_payload}')
print(f'Character length: {len(full_payload)}')
print(f'Byte length (UTF-8): {len(full_payload.encode("utf-8"))}')
