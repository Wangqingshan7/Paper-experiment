

# class Person:
#     def __init__(self,id,name,sex,birth):
#         self.id = id;
#         self.name = name
#         self.sex = sex
#         self.birth = birth;
#
#     def speak(self,word):
#         print(f'{self.name}说：{word}')
#
# zhangsan = Person(110,'张三','男',20151203)
# zhangsan.speak('hello world')


# str1 = '11,127.0.0.1,871212312324234242423eqweqweasdadsa'
# str1 = str1[:str1.find('')]
# print(str1)

# j = 0
# for i in range(len(str1)-1,0,-1):
#     if(str1[i]==''):
#         j+=1
#         continue
#     else:
#         print(j)
#         break
# str1 = str1[:-j]
# print(str1)


# print(str1[-1])
# print(ord(str1[-1]))
# print(str1[:-1])
# str2 = str1[:-(len(str1)-i)]
# str1 = str1[:-ord(str1[-1])]
# print(str1)
# print(str2)

# i=0
# while i<5:
#     print("1")
#     i+=1
#     j=0
#     while j<3:
#         print("2")
#         j+=1
#         k=0
#         while k<3:
#             print(3)
#             k+=1
# import re
# data = b'\x00\x00123ssada'
# d = re.search(b'1',data).span()
# print(d[0])


# print(str(1))

students = [[3,'Jack',12],[2,'Rose',13],[1,'Tom',10],[5,'Sam',12],[4,'Joy',8]]
s = sorted(students,key=(lambda x:x[0]))
print(s)
