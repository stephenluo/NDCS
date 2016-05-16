# -- coding: utf-8 --
import sys
import urllib.request
import os
import configparser
import hashlib
import timeit
import time



str1 = "D:\\fileLocation\\url"
str2 = "D:\\fileLocation\\url"

m1 = hashlib.new('md5');
m1.update(str2.encode("utf-8"))
print(m1.hexdigest())
time.sleep(1)

m1.update(str1.encode("utf-8"))
print(m1.hexdigest())


#读配置文件
cf = configparser.ConfigParser()
cf.read("config.conf")

s = cf.sections()
print("section", s)

print("*" * 70)
o2 = cf.options("文件目录")
print("options:文件目录",o2)

print("*" * 70)
v2 = cf.items("文件目录")
print("items:文件目录",v2)

print("*" * 70)
urlName = cf.get("文件目录", "url文件路径")

print("urlName:",  urlName)



#迭代
#list=[1,2,3,4]
#it = iter(list)

##print (next(it))
##for x in it:
##	print (x,  end=' ')

#while True:
#	try:
#		print (next(it))
#	except  StopIteration:
#		print('finish')
#		#sys.exit();

#def fun1():
#	a =0
#	while True:
#		if 3 > 2:
#			pass
#		else:
#			a = 3

# 生成器函数 
def fibonacci(n): 
    #a, b, counter = 0, 1, 0
	a = 0
	b = 1
	counter = 0
	while True:
		if counter > n: 
			return
		yield a
		a = b
		b = b+2
		#a, b = b, a + b
		counter += 1

#f = fibonacci(8);

	

def calc(a, b):
	return a**2 + b**2

def fun1(a, b):
	return calc(a,b)

def fun2(*tuple_n):
	for x in tuple_n:
		print(x,  end = ' ')

#c = fun1(3, 4);
#print(c)

#fun2(10,20,50)


#while True:
#    try:
#        print (next(f), end=" ")
#    except StopIteration:
#        input('finish:')



#x = 'runoob'; sys.stdout.write(x + '\n')

#paragraph = """这是一个段落，
#22222222222222
#333333333           333333333
#可以由多行组成"""
#print(paragraph)

input('输入：')


#s=['绳子',   '带子']
#for each in s:
#	print(each) 

#x= 2
#r = 0
#if x > 5 and x <= 10:		#选择语句
#	print("1")
#elif x  > 2 and  x <= 5:
#	print("2")
#else:
#	print(3)

#print(r)

'''print('hello', 'welcome')'''

#while循环
#例1
#n =1000
#sum = 0
#counter = 1

#while counter <= n:
#	sum+=counter
#	counter+=1

#print('1 到 %d 的和是： %d' % (n, sum))

#例2
#var = 1
#while var == 1 :  # 表达式永远为 true
#   num = input('输入')
#   print ("你输入的数字是: ", num)

#例3 while.. else ..
#count = 0
#while count < 5:
#   print (count, " 小于 5")
#   count = count + 1
#else:
#   print (count, " 大于或等于 5")

#for 语句
#sites = ["Baidu", "Google","Runoob","Taobao"]
#for site in sites:
#    if site == "Runoob1":
#        print("菜鸟教程!")
#        break
#    print("循环数据 " + site)
#else:
#    print("没有循环数据!")
#print("完成循环!")


#a = ['Google', 'Baidu', 'Runoob', 'Taobao', 'QQ']

#for i in range(len(a)):
#	print(i, a[i])

