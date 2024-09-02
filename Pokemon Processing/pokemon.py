import csv
from collections import defaultdict, Counter
import math

# 1.1 [CREATING pokemon1.txt]
def pokemonfirepercent():
    firetotal = 0.0
    fourtyandover = 0.0
    with open('pokemonTrain.csv') as pokemonfile:
        reader = csv.reader(pokemonfile)
        # skip first line
        next(reader)
        for line in reader:
            # type is line[4], line[2] is level
            type = str(line[4])
            level = float(line[2])
            if type == 'fire':
                firetotal += 1.0
                if level >= 40.0:
                    fourtyandover += 1.0
    
    percent = round(float((fourtyandover/firetotal) * 100.0))
    # writing to a text file called pokemon1.txt
    with open('pokemon1.txt', 'w') as txtfile:
        txtfile.write(f"Percentage of fire type Pokemons at or above level 40 = {percent}")

# 1.2
def readdata(f):
    with open(f) as pokemonfile:
        reader = csv.reader(pokemonfile)
        columns = next(reader)
        data = list(reader)
    return data, columns
def findcommonweakness(data): # find the common weakness for any type, puts this info in a dictionary (k = type, v = weakness), and returns the dictionary
    typetoweaknessdict = defaultdict(Counter)
    for line in data:
        pokemontype = line[4]
        pokemonweakness = line[5]
        if pokemontype != 'NaN':
            typetoweaknessdict[pokemontype][pokemonweakness] += 1
    typetoweaknessdict = dict(sorted(typetoweaknessdict.items()))

    # printing (testing)
    dicttoreturn = {}
    for pokemontype, weaknessc in typetoweaknessdict.items():
        mcw = weaknessc.most_common(1)
        if mcw:
            cw = mcw[0][0]
            # printing for debugging purposes
            # print(f"Most common weakness for type '{pokemontype}' is '{cw}'")
            if cw not in dicttoreturn:
                dicttoreturn[cw] = []
            dicttoreturn[cw].append(pokemontype)
    return dicttoreturn      
def fillintypebasedonweakness(dictionary, data): # fills in NaN type with type based on weakness in dictionary from ^
    for r, line in enumerate(data):
        pokemontype = line[4]
        weakness = line[5]
        if pokemontype == 'NaN':
            # go through the dictionary for the weakness
            for pweakness, ptype in dictionary.items():
                if weakness == pweakness:
                    data[r][4] = ptype[0]
    return data

# 1.3
def findaverages(data): # find the average atk/def/hp count based on threshold level and returns them
    # above fourty vars
    af_atk_total = 0.0
    af_atk_counts = 0.0
    af_defense_total = 0.0
    af_defense_counts = 0.0
    af_hp_total = 0.0
    af_hp_counts = 0.0
    # below fourty vars
    bf_atk_total = 0.0
    bf_atk_counts = 0.0
    bf_defense_total = 0.0
    bf_defense_counts = 0.0
    bf_hp_total = 0.0
    bf_hp_counts = 0.0
    for line in data:
        lvl = float(line[2])
        atk = float(line[6])
        defense = float(line[7])
        hp = float(line[8])
        if lvl > 40.0:
            if not math.isnan(atk):
                af_atk_total += atk
                af_atk_counts += 1.0
            if not math.isnan(defense):
                af_defense_total += defense
                af_defense_counts += 1.0
            if not math.isnan(hp):
                af_hp_total += hp
                af_hp_counts += 1.0
        else:
            if not math.isnan(atk):
                bf_atk_total += atk
                bf_atk_counts += 1.0
            if not math.isnan(defense):
                bf_defense_total += defense
                bf_defense_counts += 1.0
            if not math.isnan(hp):
                bf_hp_total += hp
                bf_hp_counts += 1.0
    # calculating averages - above 40.0
    af_atk_avg = round(float(af_atk_total/af_atk_counts), 1)
    af_defense_avg = round(float(af_defense_total/af_defense_counts), 1)
    af_hp_avg = round(float(af_hp_total/af_hp_counts), 1)
    # calculating averages - below 40.0
    bf_atk_avg = round(float(bf_atk_total/bf_atk_counts), 1)
    bf_defense_avg = round(float(bf_defense_total/bf_defense_counts), 1)
    bf_hp_avg = round(float(bf_hp_total/bf_hp_counts), 1)
    # return all values
    return af_atk_avg, af_defense_avg, af_hp_avg, bf_atk_avg, bf_defense_avg, bf_hp_avg
def fillinatkvalues(af_atk_avg, bf_atk_avg, data): # fills in NaN atk with average atk based on lvl
    for line in data:
        lvl = float(line[2])
        atk = float(line[6])
        if math.isnan(atk):
            if lvl <= 40.0:
                line[6] = bf_atk_avg
            else:
                line[6] = af_atk_avg
    return data
def fillindefensevalues(af_defense_avg, bf_defense_avg, data): # fills in NaN def with avg def based on lvl
    for line in data:
        lvl = float(line[2])
        defense = float(line[7])
        if math.isnan(defense):
            if lvl <= 40.0:
                line[7] = bf_defense_avg
            else:
                line[7] = af_defense_avg
    return data
def fillinhpvalues(af_hp_avg, bf_hp_avg, data): # fills in NaN hp with avg hp based on lvl
    for line in data:
        lvl = float(line[2])
        hp = float(line[8])
        if math.isnan(hp):
            if lvl <= 40.0:
                line[8] = bf_hp_avg
            else:
                line[8] = af_hp_avg
    return data

# compiling all data from 1.2 + 1.3 into one function [CREATING pokemonResult.csv]
def pokemonresult():
    data, columns = readdata('pokemonTrain.csv')
    weakness = findcommonweakness(data)
    af_atk_avg, af_defense_avg, af_hp_avg, bf_atk_avg, bf_defense_avg, bf_hp_avg = findaverages(data)
    # printing for debugging purposes
    # print(f"af_atk_avg:{af_atk_avg}, af_defense_avg:{af_defense_avg}, af_hp_avg:{af_hp_avg}, bf_atk_avg:{bf_atk_avg}, bf_defense_avg:{bf_defense_avg}, bf_hp_avg:{bf_hp_avg}")
    data = fillintypebasedonweakness(dictionary=weakness, data=data)
    data = fillinatkvalues(af_atk_avg=af_atk_avg, bf_atk_avg=bf_atk_avg, data=data)
    data = fillindefensevalues(af_defense_avg=af_defense_avg,bf_defense_avg=bf_defense_avg,data=data)
    data = fillinhpvalues(af_hp_avg=af_hp_avg,bf_hp_avg=bf_hp_avg,data=data)
    with open('pokemonResult.csv', 'w', newline='') as pokemonResult:
        writer = csv.writer(pokemonResult, delimiter = ',')
        writer.writerow(columns)
        writer.writerows(data)

# 1.4
def typetopersonalitymap():
    typetopersonalitiesdict = defaultdict(list)
    with open('pokemonResult.csv') as pokemonfile:
        reader = csv.reader(pokemonfile)
        next(reader)
        for line in reader:
            pokemontype = line[4]
            pokemonpersonality = line[3]
            if pokemonpersonality not in typetopersonalitiesdict[pokemontype]: 
                typetopersonalitiesdict[pokemontype].append(pokemonpersonality)
    # alphabetize keys
    typetopersonalitiesdict = dict(sorted(typetopersonalitiesdict.items()))
    # alphabetize values
    for ptype, ppersonality in typetopersonalitiesdict.items():
        # alphabetize values
        ppersonality.sort()
        # debug printing
        # print(f"{ptype}: {','.join(ppersonality)}")   
    return typetopersonalitiesdict
def pokemon4txt():
    dictionary = typetopersonalitymap()
    with open('pokemon4.txt', 'w') as txtfile:
        txtfile.write("Pokemon type to personality mapping:\n\n")
        for ptype,ppersonality in dictionary.items():
            txtfile.write(f"{ptype}: {', '.join(ppersonality)}\n")

# 1.5
def averagehp():
    hptotal = 0.0
    hpcounter = 0.0
    with open('pokemonResult.csv') as pokemonfile:
        reader = csv.reader(pokemonfile)
        next(reader) # skip first line
        for line in reader:
            hp = float(line[8])
            stage = float(line[9])
            if (stage == 3.0):
                hptotal += hp
                hpcounter += 1.0
    
    average = round(float((hptotal/hpcounter)))
    return average
def pokemon5txt():
    average = averagehp()
    with open('pokemon5.txt', 'w') as txtfile:
        txtfile.write(f"Average hit point for Pokemons of stage 3.0 = {average}")

# main
# 1.1
pokemonfirepercent()
# 1.2 + 1.3
pokemonresult()
# 1.4
pokemon4txt()
# 1.5
pokemon5txt()