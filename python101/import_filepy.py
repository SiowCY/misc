import python101
from python101 import Class1
from python101 import Class2_child as child_class

print ("==== Import python101 to here!! ====")
my_class = python101.Class1("Using python101.Class1", 1)
print(my_class.method1())

my2_class = Class1('2', 2)
print("Using from python101 import Class1")
print(my2_class.method2())

my3_class = Class1(3, ") this is return function", "AND THE THIRD VARIABLE!")
print(my3_class.method3())

my4_class = Class1("Unuse var1", "Unuse var2")
my4_class.method4()

my5_class = Class1("Unuse var1", "Unuse var2", init_var4="Change 4th value!")
my5_class.init_var5 = "Changed 5th value!"
my5_class.method5()

my6_class = Class1("Unuse var1", "Unuse var2")
my6_class.method6("Changed 5th variable!")

# Testing on Class2_child
my_class2 = child_class(3,") I AM UPPER CASE CHILD CLASS","USING FROM PYTHON101 IMPORT CLASS2_CHILD AS CHILD_CLASS ")
print(my_class2.method3())

my2_class2 = python101.Class2_child("Unuse var1", "Unuse var2")
my2_class2.child_method1("Child Self Attr 1")

# Calling independent class method
my_ind_class = python101.Class2_child("Unuse var1", "Unuse var2")
my_ind_class.ind_class.ind_method()

print ("==== End import python101 to here!! ====")
