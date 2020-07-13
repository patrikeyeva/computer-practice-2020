import collections
import pandas
import numpy
from sklearn.linear_model import LinearRegression

football = pandas.read_csv("Football statistics.csv", delimiter=';')  # статистика игр 
teams = pandas.read_csv('Teams.csv')
print football
teams = teams['Team Name'].tolist()  # команды которые играют в 2019
team_delete = [x for x in pandas.unique(football['Соперник']) if x not in teams]
team_list = pandas.unique(football['Команда'])
for team in team_delete:
    football = football[football['Команда'] != team]
    football = football[football['Соперник'] != team]
football = football.reset_index(drop=True)


def full_team_statistics(year):
    total_stats = collections.defaultdict(list)
    for team in teams:
        team_stat = team_statistics(team, year)
        total_stats[team] = team_stat
    return total_stats


def team_statistics(team, year):
    matches_won = 0 
    matches_draw = 0 
    matches_lost = 0 
    
    goals_scored = 0 
    goals_conceded = 0  # Пропущено
    
    shots = 0  # Удары по воротам
    shots_on_goal = 0  # Удары в створ ворот
    
    cross = 0  # Навесы
    accurate_cross = 0  # Точные навесы
    
    ball_possession = 0  # Владение мячом
    average_ball_possession = 0  # Среднее владение мячом за матч
    
    soccer_pass = 0 
    accurate_soccer_pass = 0 
    total_score = 0 
    
    matches = 0  # Сыгранные матчи
    xG = 0  # Ожидаемые голы
    ppda = 0  # Прессинг
    
    number = len(football)

    for n in range(number):
        if (((football['Год'][n] == year) and (football['Команда'][n] == team) and (football['Часть'][n] == 2)) or ((football['Год'][n] == year-1) and (football['Команда'][n] == team) and (football['Часть'][n] == 1))):
            matches += 1
            
            goals_conceded += football['Пропущено'][n]
            goals_scored += football['Забито'][n]

            if (football['Победитель'][n] == team):
                total_score += 3
                matches_won += 1
            elif (football['Проигравший'][n] == team):
                matches_lost += 1
            else:
                total_score += 1
                matches_draw += 1
            
            ball_possession += football['Владение'][n]
            
            shots += football['Удары'][n]
            shots_on_goal += football['Удары в створ'][n]
            
            soccer_pass += football['Передачи'][n]
            accurate_soccer_pass += football['Точные передачи'][n]
            
            cross += football['Навесы'][n]
            accurate_cross += football['Точные навесы'][n]
            
            xG += football['xG'][n]
            ppda += football['PPDA'][n]

    average_ball_possession = round(ball_possession/matches, 5)  # Владение мячом в среднем за матч
    
    return [matches_won,
            matches_draw, 
            matches_lost, 
            total_score,
            goals_scored, goals_conceded, 
            shots, shots_on_goal,
            soccer_pass, accurate_soccer_pass,
            round(xG, 5), round(ppda, 5),
            cross, accurate_cross,
            round(average_ball_possession, 5)]


def training_data(years):
    number = 0
    for year in years:
        yearly = football[football['Год'] == year]
        number += len(yearly.index)
    num_feature = len(team_statistics('Урал', 2016))
    train_x = numpy.zeros((number, num_feature))
    train_y = numpy.zeros((number))
    ind = 0
    for year in years:
        team_stat = full_team_statistics(year)
        yearly = football[football['Год'] == year]
        matches_year = len(yearly.index)
        train_x_yearly = numpy.zeros((matches_year, num_feature))
        train_y_yearly = numpy.zeros((matches_year))
        count = 0
        for index, row in yearly.iterrows():
            team = row['Команда']
            vector_t = team_stat[team]
            opponent = row['Соперник']
            vector_o = team_stat[opponent]
            
            difference = [v1 - v2 for v1, v2 in zip(vector_t, vector_o)]
            
            if len(difference) != 0:
                train_x_yearly[count] = difference
            if team == row['Победитель']:
                train_y_yearly[count] = 1
            else: 
                train_y_yearly[count] = 0
            count += 1   
        train_x[ind:matches_year+ind] = train_x_yearly
        train_y[ind:matches_year+ind] = train_y_yearly
        ind += matches_year
    return train_x, train_y


def predict_result(first_team_stat, second_team_stat):
    difference = [[v1 - v2 for v1, v2 in zip(first_team_stat, second_team_stat)]]
    result = model.predict(difference)
    return result


years = range(2016, 2019)
train_x, train_y = training_data(years)
print '\n', train_x, '\n\n', train_y, '\n'

model = LinearRegression()
model.fit(train_x, train_y)

first_team = "Урал"
second_team = "Краснодар"
first_team_stat = team_statistics(first_team, 2019)
second_team_stat = team_statistics(second_team, 2019)

print "Победа Урала: ", predict_result(first_team_stat, second_team_stat)
print "Победа Краснодара: ", predict_result(second_team_stat, first_team_stat)
print("\n")

for team_name in teams:
    first_team = "Зенит"
    second_team = team_name
    
    if(first_team != second_team):
        first_team_stat = team_statistics(first_team, 2019)
        second_team_stat = team_statistics(second_team, 2019)
        print first_team, predict_result(first_team_stat, second_team_stat), " - ", second_team, predict_result(second_team_stat, first_team_stat,)
