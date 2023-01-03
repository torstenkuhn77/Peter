

import numpy as np

# x = np.array([1,2,3],dtype = float)
x = np.array(['hugo','egon',5.4])
y = np.array([[1, 2, 3] , [4, 5, 6], [7, 8, 9]],dtype = str)

print ('array x ',x)
print ('array y ',y)
print ()
print (x[0])
print ()
print (x[1])
print ()
print (y[1])
print ()
print("Die Dimensionen von x sind : 0 bis", np.ndim(x), ' --> x[0]...x[1]' )
print("Die Dimensionen von y sind : 0 bis", np.ndim(y), ' --> x[0]...x[1]...x[2]')
print ()
for i1 in range (np.ndim(x) - 1 , np.ndim(x) + 2) :
    print (x[i1])
print ()  
for i1 in range (0 , 3) :
    for i2 in range (0 , 3) :
        print (y[i1,i2])
    
print()
 
print ('Erzeugung und Aufbau eines ARRAY :')
a = np.array([])
print ('Test-array initial : ',a)
a = np.array([[1,2,3],[4,5,6]])
print ('Test-array filled : ',a) 
print ()  

print ('Appended elements to Test-array : ') 
print (np.append(a, [7,8,9])) 
print ()  

print ('Appended elements along axis 0:') 
print (np.append(a, [[7,8,9]],axis = 0)) 
print ()  

print ('Appended elements along axis 1:') 
print (np.append(a, [[5,5,5],[7,8,9]],axis = 1))
print ()