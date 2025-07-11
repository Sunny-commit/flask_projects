# file=open("example.txt",'r')
# print(file.read(5))
# file=open('example.txt','w')

# file.write("my name is chandu")
# file.write("i am studying b.tech")
# file1=open('example.txt','r')
# for word in file1:
#     print(word)
# file.close()
#file=open('example.txt','a')
#file.write("i like studying")
#file=open('example.txt','r')
#print(file.read())
# with open('example.txt','r') as file:
#     a=file.read()
#     print(a)
# file=open("greek.txt",'w')
# file.write(a)
# file.close()
# a=a[::-1]
# with open('example2.txt','w') as f:
#     f.write(a)
#     f.close()
# with open('example.txt','r') as f:
#     data=f.readlines()
#     print(data)
#     for line in data:
#         print(line.split())
def file(filename):
    try:
        with open(filename,'w') as f:
            f.write("hello world")
            f.close()
    except IOError:
        print("file is not file"+filename)
def read(filename):
    try:
        with open(filename,'r') as f:
            print(f.read())
            f.seek(4)
    except IOError:
        print("file enable read")
file('example3.txt')
read('example3.txt')