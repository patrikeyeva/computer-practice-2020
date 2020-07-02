# -*- coding: utf-8 -*-
"""
Предобработка данных в Pandas
"""
import pandas

data = pandas.read_csv('titanic.csv')
"""index_col задаёт нумерацию строк данного dataFrame"""

max_pas = data['PassengerId'].size # общее кол-во пассажиров

sex_static = data['Sex'].value_counts() # собирает статистику по датафрейму
male = sex_static['male'] # кол-во мужчин на корабле
female = sex_static['female'] #кол-во женщин на корабле
# print male
# print female

survived_static = data['Survived'].value_counts()
survived = survived_static[1] # кол-во выживших на корабле
share_of_surv_pass = survived.astype(float)/max_pas # доля выживших пассажиров
#print share_of_surv_pass

pclass_static = data['Pclass'].value_counts() 
first_class_number = pclass_static[1] # кол-во пассажиров 1го класса
share_of_firstClass_pass = first_class_number.astype(float)/max_pas
#print share_of_firstClass_pass

age_static = data['Age'].value_counts()
age_general = data.sum(axis = 0) # суммирование всех возрастов пассажиров
age_static_sort = age_static.index.sort_values() #отсортированные возраста

age_sort =  data['Age'].sort_values()
age_sort = age_sort[:714]
age_mean = age_sort.sum()/age_sort.size #среднее значение
age_median = age_sort.median() # медиана возраста
#print age_mean
#print age_median

data2 = pandas.read_csv('titanic.csv', usecols=['SibSp', 'Parch'])
data2_corr = data2.corr(method ='pearson') # корреляция
#print data2_corr
