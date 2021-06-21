amountRaw = '12003.4567.89'

lHalf = amountRaw[:-3]
lHalf = lHalf.replace("3","")
rHalf = amountRaw[-3:]

amountRaw = lHalf + rHalf

print(amountRaw)