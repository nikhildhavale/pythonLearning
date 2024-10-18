x = 2
y = 10
if x > 2 or y > 10:
    print("or case")
while x < 30:
    x+=1
    if x > 20:
        continue
    else:
        print(x)
else:
    print("The loop is over")

list = [1,2,3,4,5,5,6,7]
for item in list:
    print(item)