# fruits = ["apple","banana","cherry"]
# for x in fruits:
#     if x == "banana":
#         continue
#     print(x)

# the range() function

# for x in range(10):
#     print(x)

# for x in range(2,10):
#     print(x)

# for x in range(2,30,4):
#     print(x)

# for x in range(6):
#     print(x)
# else:
#     print("finally finsihed")

# for x in range(6):
#     if x ==3 :break
#     print(x)
# else:
#     print("finally finished")

# nested loops

# fruits = ["apple","banana","cherry"]
# adj = ["red","blue","green"]
# for x in adj:
#     for y in fruits:
#         print(x,y)

# for x in [0,1,2]:
#     pass

# Python Functions

# def my_function():
#     print("welcome to my frist function")
    
# my_function()


# def my_function(fname):
#     print(f"welcome to my frist function {fname}")
    
# my_function("satyaranjan")


# def my_function(fname,lname):
#     print(f" {fname} , {lname}")
    
# my_function("satyaranjan","swain")


# def my_function(fname,lname):
#     print(f" {fname} , {lname}")
    
# my_function("satyaranjan")

# def  myfunnction(*kids):
#     print("the fist name of child is "+ kids[2])
    
# myfunnction("emmail","amit","rahul")


# def  myfunnction(child1,child2,child3):
#     print("the fist name of child is "+ child3)
    
# myfunnction("emmail","amit","rahul")


# def  myfunnction(**kids):
#     print("the fist name of child is "+ kids['lname'])
    
# myfunnction(fname = "amit",lname = "rahul")

# def  myfunnction(child1,child2,child3):
#     print("the fist name of child is "+ child3)
    
# myfunnction(child1 = "emmail",child2 = "amit",child3  = "rahul")

# def my_function(country = "norway"):
#     print("i am from "+country)
    
# my_function("sweden")
# my_function("india")
# my_function()
# my_function("brazil")

# def my_function(food):
#     for x in food:
#         print(x)
        
# fruits = ["apple","banana","cherry"]
# my_function(fruits)


# def my_funnction(x):
#     return 5*x
    

# print(my_funnction(11))
# print(my_funnction(10))
# print(my_funnction(12))

# def my_function():
#     pass

# def my_function(x,/):
#     print(x)
    
# my_function(3)


# def my_function(x,/):
#     print(x)
    
# my_function(3)


# def my_function(*,x):
#     print(x)

# my_function(x=3)


# def my_functionn(a,b,/,*,c,d):
#     print(a+b+c+d)
    
# my_functionn(5,6,c=7,d=8)

# python lambda

# x = lambda a: a+10
# print(x(5))

# x = lambda a,b: a+b
# print(x(5,10))


# x = lambda a,b: a*b
# print(x(5,10))



# x = lambda a,b,c: a*b*c
# print(x(5,10,15))


# def my_funnction(n):
#     return lambda a:a*n


# mydouble = my_funnction(10)
# print(mydouble(11))

# mydouble = my_funnction(100)
# print(mydouble(111))
