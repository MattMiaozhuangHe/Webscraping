import sys

user_input = sys.argv[1:]
user_input_char = user_input[0]
user_in_k = user_input[1]


res = ""
hs = {}
for i in range(len(user_input_char)):
  if user_input_char[i] not in hs:
    hs.update({user_input_char[i]:i})
    res += user_input_char[i]
  else:
    if(i - hs[user_input_char[i]] < int(user_in_k)):
        hs[user_input_char[i]] = i
        res+= "-"
    else:
        res+= user_input_char[i]

print(res)