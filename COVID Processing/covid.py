import csv
import re
import math
from collections import defaultdict, Counter

# reading csv file, storing data in data and columns in columns
def readdata(f):
    with open(f) as covidfile:
        reader = csv.reader(covidfile)
        columns = next(reader)
        data = list(reader)
    return data, columns

# 2.1 Convert age range to average value
def replacerangewithavg(data):
    for line in data:
        age = line[1]
        if re.search(r'\d-\d', age):
            one, two = [int(x) for x in age.split('-')]
            average = round(float((one + two)/2))
            line[1] = str(average)
    return data

# 2.2.1 Convert date from dd.mm.yyyy to mm.dd.yyyy given data and column number
def convertdate(data, colnum):
    for line in data:
        date = line[colnum]
        dd, mm, yyyy = [str(x) for x in date.split('.')]
        newdate = str(f"{mm}.{dd}.{yyyy}")
        line[colnum] = newdate
    return data
# 2.2.2 Apply date change to date_onset_symptoms,date_admission_hospital, and date_confirmation
def datecols(data):
    data = convertdate(data=data, colnum=8) #date_onset_symptoms
    data = convertdate(data=data, colnum=9) #date_admission_hospital
    data = convertdate(data=data, colnum=10) #date_confirmation
    return data

# 2.3.1 create a lat dict with each province and their avg lat and a long dict with each province and their avg long
def avglongandlat(data):
    latprovcoords = defaultdict(list)
    lonprovcoords = defaultdict(list)
    for line in data:
        prov = line[4]
        lat = float(line[6])
        lon = float(line[7])
        if not math.isnan(lat):
            latprovcoords[prov].append(lat)
        if not math.isnan(lon):
            lonprovcoords[prov].append(lon)
    
    latavgcoords = defaultdict(list)
    for prov, latlist in lonprovcoords.items():
        lattotal = 0.0
        latcounter = 0.0
        for lat in latlist:
            lattotal += lat
            latcounter += 1.0
        latavg = round(float(lattotal/latcounter), 2)
        latavgcoords[prov].append(latavg)
    
    lonavgcoords = defaultdict(list)
    for prov, lonlist in lonprovcoords.items():
        lontotal = 0.0
        loncounter = 0.0
        for lon in lonlist:
            lontotal += lon
            loncounter += 1.0
        lonavg = round(float(lontotal/loncounter), 2)
        lonavgcoords[prov].append(lonavg)
    
    return latavgcoords, lonavgcoords
# 2.3.2 taking in avglat and avglong dict, replace NaN lat and long with avg based on province
def replacenanwithavg(data, latavgcoords, lonavgcoords):
    for line in data:
        prov = line[4]
        lat = float(line[6])
        lon = float(line[7])
        if math.isnan(lat):
            # if the lat is nan, go through latavgcoords dictionary looking for province
            for province, latavg in latavgcoords.items():
                if prov == province:
                     # replace nan with average
                    line[6] = round(latavg[0], 2)
        if math.isnan(lon):
            # if the lon is nan, go through lonavgcoords dictionary looking for province
            for province, lonavg in lonavgcoords.items():
                if prov == province:
                     # replace nan with average
                    line[7] = round(lonavg[0], 2)
    return data

# 2.4.1 creating a city Counter dict with each province and the most occuring city in that province
def findmostcommoncity(data):
    commoncity = {}
    for line in data:
        city = line[3]
        prov = line[4]
        if city != 'NaN':
            if prov not in commoncity:
                commoncity[prov] = Counter()
            commoncity[prov][city] += 1
    mostcommoncity = {}
    for province, citycount in commoncity.items():
        mcc = citycount.most_common(1)
        if mcc:
            mostcommoncity[province] = mcc[0][0]
    return mostcommoncity
# 2.4.2 taking in city dict, replacing NaN city with most common city based on province
def replacenancity(data, mostcommoncity):
    for line in data:
        city = line[3]
        prov = line[4]
        if city == 'NaN':
            for province, commoncity in mostcommoncity.items():
                if prov == province:
                    line[3] = commoncity
    return data

# 2.5.1 creating a symptom Counter dict with each province and the most occurring symptom in that province
def findmostcommonsymptom(data):
    commonsymptom = {}
    for line in data:
        prov = line[4]
        symptoms = re.split(r';\s*|\s*,\s*', line[11])
        for symptom in symptoms:
            if symptom != 'NaN':
                if prov not in commonsymptom:
                    commonsymptom[prov] = Counter()
                commonsymptom[prov][symptom] += 1
    mostcommonsymptom = {}
    for province, symptomlst in commonsymptom.items():
        mcs = symptomlst.most_common(1)
        if mcs:
            mostcommonsymptom[province] = mcs[0][0]
    return mostcommonsymptom
# 2.5.2 taking in symptom dict, replacing NaN symptom with most common symptom based on province
def replacenansymptom(data, mostcommonsymptom):
    for line in data:
        prov = line[4]
        symptoms = line[11]
        if symptoms == 'NaN':
            for province, commonsymptom in mostcommonsymptom.items():
                if prov == province:
                    line[11] = commonsymptom
    return data

# 2.6 creating covidResult.csv
def covidresult():
    # 2.0
    data, columns = readdata('covidTrain.csv')
    # 2.1
    data = replacerangewithavg(data= data)
    # 2.2
    data = datecols(data= data)
    # 2.3
    latavgcoords, lonavgcoords = avglongandlat(data= data)
    data = replacenanwithavg(data=data, latavgcoords=latavgcoords, lonavgcoords=lonavgcoords)
    # 2.4
    mostcommoncity = findmostcommoncity(data)
    data = replacenancity(data=data, mostcommoncity=mostcommoncity)
    # 2.5
    mostcommonsymptom = findmostcommonsymptom(data)
    data = replacenansymptom(data=data, mostcommonsymptom=mostcommonsymptom)
    # creating covidResult.csv with all the modified data
    with open('covidResult.csv', 'w', newline='') as covidResult:
        writer = csv.writer(covidResult, delimiter = ',')
        writer.writerow(columns)
        writer.writerows(data)
           
covidresult()
