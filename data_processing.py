import csv, os

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

cities = []
with open(os.path.join(__location__, 'Cities.csv')) as f:
    rows = csv.DictReader(f)
    for r in rows:
        cities.append(dict(r))

countries = []
with open(os.path.join(__location__, 'Countries.csv')) as f:
    rows = csv.DictReader(f)
    for r in rows:
        countries.append(dict(r))

titanic = []
with open(os.path.join(__location__, 'Titanic.csv')) as f:
    rows = csv.DictReader(f)
    for r in rows:
        titanic.append(dict(r))

Players = []
with open(os.path.join(__location__, 'Players.csv')) as f:
    rows = csv.DictReader(f)
    for r in rows:
        Players.append(dict(r))

Teams = []
with open(os.path.join(__location__, 'Teams.csv')) as f:
    rows = csv.DictReader(f)
    for r in rows:
        Teams.append(dict(r))


class DB:
    def __init__(self):
        self.database = []

    def insert(self, table):
        self.database.append(table)

    def search(self, table_name):
        for table in self.database:
            if table.table_name == table_name:
                return table
        return None
    
import copy
class Table:
    def __init__(self, table_name, table):
        self.table_name = table_name
        self.table = table
    
    def join(self, other_table, common_key):
        joined_table = Table(self.table_name + '_joins_' + other_table.table_name, [])
        for item1 in self.table:
            for item2 in other_table.table:
                if item1[common_key] == item2[common_key]:
                    dict1 = copy.deepcopy(item1)
                    dict2 = copy.deepcopy(item2)
                    dict1.update(dict2)
                    joined_table.table.append(dict1)
        return joined_table
    
    def filter(self, condition):
        filtered_table = Table(self.table_name + '_filtered', [])
        for item1 in self.table:
            if condition(item1):
                filtered_table.table.append(item1)
        return filtered_table
    
    def aggregate(self, function, aggregation_key):
        temps = []
        for item1 in self.table:
            temps.append(float(item1[aggregation_key]))
        return function(temps)
    
    def select(self, attributes_list):
        temps = []
        for item1 in self.table:
            dict_temp = {}
            for key in item1:
                if key in attributes_list:
                    dict_temp[key] = item1[key]
            temps.append(dict_temp)
        return temps

    def __str__(self):
        return self.table_name + ':' + str(self.table)

table1 = Table('cities', cities)
table2 = Table('countries', countries)
table3 = Table('players', Players)
table4 = Table('teams', Teams)
table5 = Table('titanic', titanic)
my_DB = DB()
my_DB.insert(table1)
my_DB.insert(table2)
my_DB.insert(table3)
my_DB.insert(table4)
my_DB.insert(table5)
my_table1 = my_DB.search('cities')
my_table3 = my_DB.search('players')

# World cup 2010 part
my_table4 = table3.join(table4, 'team').filter(lambda x: 'ia' in x['team']).filter(lambda x: int(x['minutes']) < 200).filter(lambda x: int(x['passes']) > 100)
print(my_table4.select(['surname', 'team', 'position']))
team_ranking_below_10 = table4.filter(lambda x: int(x['ranking']) < 10).aggregate(lambda x: sum(x)/len(x), 'games')
team_ranking_more_than_10 = table4.filter(lambda x: int(x['ranking']) >= 10).aggregate(lambda x: sum(x)/len(x), 'games')
print(f'Average games played for teams ranking below 10: {team_ranking_below_10:.3f}')
print(f'Average games played for teams ranking above 10: {team_ranking_more_than_10:.3f}')
forward_passes = table3.filter(lambda x: x['position'] == 'forward').aggregate(lambda x: sum(x)/len(x), 'passes')
midfield_passes = table3.filter(lambda x: x['position'] == 'midfielder').aggregate(lambda x: sum(x)/len(x), 'passes')
print(f'Forward passes: {forward_passes:.3f}')
print(f'Midfielder passes: {midfield_passes:.3f}')

# Titanic part
first_class_passenger_average_paid = table5.filter(lambda x: int(x['class']) == 1).aggregate(lambda x: sum(x)/len(x), 'fare')
third_class_passenger_average_paid = table5.filter(lambda x: int(x['class']) == 3).aggregate(lambda x: sum(x)/len(x), 'fare')
print(f'Average fare paid by first class passenger: {first_class_passenger_average_paid:.3f}')
print(f'Average fare paid by third class passenger: {third_class_passenger_average_paid:.3f}')
all_female_passengers = table5.filter(lambda x: x['gender'] == 'F').select(['survived'])
female_passengers = table5.filter(lambda x: x['gender'] == 'F').filter(lambda x: x['survived'] == 'yes').select(['survived'])
all_male_passengers = table5.filter(lambda x: x['gender'] == 'M').select(['survived'])
male_passengers = table5.filter(lambda x: x['gender'] == 'M').filter(lambda x: x['survived'] == 'yes').select(['survived'])
print(f'Survival rate of female passengers: {len(female_passengers)/len(all_female_passengers):.2f} ')
print(f'Survival rate of male passengers: {len(male_passengers)/len(all_male_passengers):.2f} ')

# Find the total number of male passengers embarked at Southampton
Southampton_passengers = table5.filter(lambda x: x['gender'] == 'M').filter(lambda x: x['embarked'] == 'Southampton').select(['embarked'])
print(f'The total number of male passengers embarked at Southampton are {len(Southampton_passengers)} passengers.')