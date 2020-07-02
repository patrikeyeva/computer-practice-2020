# -*- coding: utf-8 -*-
"""Работа с векторами и матрицами в NumPy"""


"""
1.
Генерация матрицы, состоящей из 1000 строк и 50 столбцов, 
элементы которой являются случайными из 
нормального распределения N(1,100).
"""

import numpy as np
M = np.random.normal(loc=1, scale=10, size=(1000, 50)) # ф-ция генерации чисел из норм. распр-ния
print M

"""
2.
Произвести нормировку матрицы
(вычесть из каждого столбца его среднее значение, 
а затем поделить на его стандартное отклонение)
"""
mean = np.mean(M, axis = 0) # среднее значение по столбцам (матрица или число)
std = np.std(M, axis = 0) # стандартное отклонение 
M_norm = (M - mean)/std
print M_norm  

"""
3.
Вывод для заданной матрицы номера строк, 
сумма элементов в которых превосходит 9
"""
M2 = np.array([[5, 4, 0], 
               [8, 5, 9],              
               [3, 1, 1],
               [2, 2, 2], 
               [4, 2, 4], 
               [9, 8, 2]])

M2_sum = np.sum(M2, axis = 1)
res = np.nonzero(M2_sum > 9) # логическая операция применяется поэлементно
print res

"""
4.
Генерация двух единичных матриц (т.е. с единицами на диагонали) размера 3x3. 
Соединение двух матриц в одну размера 6x3.
"""
X = np.eye(3) # геерация единичной матрицы
Y = np.eye(3)
XY = np.vstack((X,Y)) # вертикальная стыковка матриц
YX = np.hstack((X,Y)) # горизонтальная стыковка 
print YX
print("")
print XY

