class Person:
    def __init__(abc,name,age):
        abc.name = name
        abc.age = age
        
    def __str__(dfg):
        return f"{dfg.name} and my age is {dfg.age}"
    
    def myfunction(xyz):
        print(f"hello my name is {xyz.name}")
        
obj = Person("satyaranjan",36)
obj.myfunction()
print(obj)
del obj.age
print(obj)

# class Person:
#     pass


# inheritance

# class Person:
#     def __init__(self,name,age):
#         self.name = name
#         self.age = age
        
#     def myfunction(self):
#         print(f"hello my name is {self.name}")
        
# class Student(Person):
#     pass

# obj = Student("satyaranjan",36)
# obj.myfunction()


# class Person:
#     def __init__(self,name,age):
#         self.name = name
#         self.age = age
        
#     def myfunction(self):
#         print(f"hello my name is {self.name}")
        
# class Student(Person):
#     def __init__(self,name,age,year):
#         super().__init__(name,age)
#         self.graduation_year = year

#     def welcome(self):
#         print(f"welcome to {self.name} and to your age {self.age} and final year {self.graduation_year}")
# obj = Student("satyaranjan",36,2020)
# obj.myfunction()
# obj.welcome()

#python Iterators

# mytuple = ("apple","banana","cherry")
# myit = iter(mytuple)

# print(next(myit))
# print(next(myit))
# print(next(myit))
# print(next(myit))


# mytuple = "banana"
# myit = iter(mytuple)

# print(next(myit))
# print(next(myit))
# print(next(myit))
# print(next(myit))


# Create an Iterator
# class Mynumber:
#     def __iter__(self):
#         self.a = 1
#         return self
    
#     def __next__(self):
#         x = self.a
#         self.a += 1
#         return x
    
# obj = Mynumber()
# myit = iter(obj)

# print(next(myit))
# print(next(myit))
# print(next(myit))
# print(next(myit))
# print(next(myit))
# print(next(myit))
# print(next(myit))
# print(next(myit))
# print(next(myit))
# print(next(myit))
# print(next(myit))
# print(next(myit))
# print(next(myit))
# print(next(myit))
# print(next(myit))
# print(next(myit))
# print(next(myit))
# print(next(myit))
# print(next(myit))
# print(next(myit))
# print(next(myit))
# print(next(myit))
# print(next(myit))
# print(next(myit))


# class Mynumber:
#     def __iter__(self):
#         self.a = 1
#         return self
    
#     def __next__(self):
#         if self.a <= 20:
#             x = self.a
#             self.a += 1
#             return x
#         else:
#             raise StopIteration
# obj = Mynumber()
# myit = iter(obj)

# print(next(myit))
# print(next(myit))
# print(next(myit))
# print(next(myit))
# print(next(myit))
# print(next(myit))
# print(next(myit))
# print(next(myit))
# print(next(myit))
# print(next(myit))
# print(next(myit))
# print(next(myit))
# print(next(myit))
# print(next(myit))
# print(next(myit))
# print(next(myit))
# print(next(myit))
# print(next(myit))
# print(next(myit))
# print(next(myit))
# print(next(myit))
# print(next(myit))

# python polymorphism

# x = "hello world"
# print(len(x))
# y = ["apple","banana","cherry"]
# print(len(y))



# class Car:
#     def __init__(self,brand,model):
#         self.model = model
#         self.brand = brand
        
#     def move(self):
#         print("Dive")
        
# class Boat:
#     def __init__(self,brand,model):
#         self.model = model
#         self.brand = brand
        
#     def move(self):
#         print("Sail")
        
# class Plane:
#     def __init__(self,brand,model):
#         self.model = model
#         self.brand = brand
        
#     def move(self):
#         print("fly")
        
# car1 = Car("ford","mustang")
# boat1 = Boat("ibiza","Touring 20")
# plane1 = Plane("boeing","747")

# for x in (car1,boat1,plane1):
#     x.move()



# class Vehicle:
#     def __init__(self,brand,model):
#         self.model = model
#         self.brand = brand
        
#     def move(self):
#         print("Dive")

# class Car(Vehicle):
#     pass
 
# class Boat(Vehicle):
#     def move(self):
#         print("Sail")
        
# class Plane(Vehicle):
#     def move(self):
#         print("fly")
        
# car1 = Car("ford","mustang")
# boat1 = Boat("ibiza","Touring 20")
# plane1 = Plane("boeing","747")

# for x in (car1,boat1,plane1):
#     x.move()

# Python scope

# def myfunc():
#     x = 300
#     print(x)
    
# myfunc()
# print(x)

# def myfunc():
#     x = 300
#     def myinnerfunction():
#         print(x)
#     myinnerfunction()
# myfunc()


# x  = 300

# def myfunction():
#     print(x)
    
# myfunction()
# print(x)


# x = 300

# def myfunction():
#     global x
#     x  = 200
#     print(x)

# myfunction()
# print(x)


# def myfunc():
#     x = 300
#     def myinnerfunction():
#         nonlocal x
#         x = 200
#         print(x)
#     myinnerfunction()
#     print(x)
# myfunc()


#python modules

# import test

# test.greeting("satyaranjan")

# print(test.person1['name'])

# from test import Name


# obj = Name()
# print(obj.x)


# import test as t
# t.greeting("satyaranjan")

# import platform

# x = platform.system()
# print(x)

# import platform

# x = dir(platform)
# print(x)
# print(len(x))

# from  test import person1
# print(person1)

#python datetime


# import datetime
# x = datetime.datetime.now()
# print(x)



# import datetime
# x = datetime.datetime.now()
# print(x.year)

# import datetime
# x = datetime.datetime.now()
# print(x.year)

# import datetime
# x = datetime.datetime.now()
# print(x.year)

# import datetime
# x = datetime.datetime(2020,5,17)
# print(x)


# import datetime
# x = datetime.datetime(2020,1,17)
# print(x.strftime("%b"))


# Directive	Description	Example	
# %a	Weekday, short version	Wed	
# %A	Weekday, full version	Wednesday	
# %w	Weekday as a number 0-6, 0 is Sunday	3	
# %d	Day of month 01-31	31	
# %b	Month name, short version	Dec	
# %B	Month name, full version	December	
# %m	Month as a number 01-12	12	
# %y	Year, short version, without century	18	
# %Y	Year, full version	2018	
# %H	Hour 00-23	17	
# %I	Hour 00-12	05	
# %p	AM/PM	PM	
# %M	Minute 00-59	41	
# %S	Second 00-59	08	
# %f	Microsecond 000000-999999	548513	
# %z	UTC offset	+0100	
# %Z	Timezone	CST	
# %j	Day number of year 001-366	365	
# %U	Week number of year, Sunday as the first day of week, 00-53	52	
# %W	Week number of year, Monday as the first day of week, 00-53	52	
# %c	Local version of date and time	Mon Dec 31 17:41:00 2018	
# %C	Century	20	
# %x	Local version of date	12/31/18	
# %X	Local version of time	17:41:00	
# %%	A % character	%	
# %G	ISO 8601 year	2018	
# %u	ISO 8601 weekday (1-7)	1	
# %V	ISO 8601 weeknumber (01-53)	01