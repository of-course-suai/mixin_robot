import requests


acc = '''eyJhbGciOiJSUzUxMiIsInR5cCI6IkpXVCJ9.eyJhaWQiOiI5YTNhYjlmOS0yOGQ0LTQ1MTYtODVkNi0wMzBjOTQ2MTg4MjQiLCJleHAiOjE2NDI1Nzg4MDksImlhdCI6MTYxMTA0MjgwOSwiaXNzIjoiOTU5Zjk0NGYtNjAzZi00MzdjLWE1NjYtOWFjYzFjMGUwNzBlIiwic2NwIjoiUEhPTkU6UkVBRCBQUk9GSUxFOlJFQUQgQ09OVEFDVFM6UkVBRCJ9.DZmN_kqoCfUCSAnb2wOTIpfsIftTmC_rbgL-Y9wrNypV7LwaPaWqv_ecPn9awPrtSP-7i7GOtNG_J3Up42rEuUa0jNaOoqvYc3MqkbJbfAVfGeSs8xQpcDzQJTUqpA4oAHVe7ohwYYZb2kRwhlEXlmX8C0fmX1s5aW8zh3nxHNs'''

h = {"Authorization":"Bearer "+acc}
files = {'data':('pic.jpg',open('1.jpg','rb'),'image/jpeg')}
res = requests.post('https://api.mixin.one/attachments',files = files, headers=h)
print(res.content)
