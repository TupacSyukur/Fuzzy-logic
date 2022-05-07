from asyncore import read
import pandas as pd


def fuzzification(shop):
    service = shop["service"]
    price = shop["price"]
    shop["value_service"] = []
    # fuzzification service
    if service <= 20:
        shop["value_service"].append(1)
    elif service > 40:
        shop["value_service"].append(0)
    elif service > 20 and service <= 40:
        shop["value_service"].append((40 - service)/(40 - 20))
    if service > 50 and service <= 70:
        shop["value_service"].append(1)
    elif service <= 30 or service > 80:
        shop["value_service"].append(0)
    elif service > 30 and service <= 50:
        shop["value_service"].append((service - 30)/(50 - 30))
    elif service > 70 and service <= 80:
        shop["value_service"].append((80 - service)/(80 - 70))
    if service > 85:
        shop["value_service"].append(1)
    elif service <= 75:
        shop["value_service"].append(0)
    elif service > 75 and service <= 85:
        shop["value_service"].append((service - 75)/(85 - 75))

    shop["value_price"] = []
    # fuzzification price
    if price <= 3:
        shop["value_price"].append(1)
    elif price > 6:
        shop["value_price"].append(0)
    elif price > 3 and price <= 6:
        shop["value_price"].append((6 - price)/(6 - 3))
    if price <= 3 or price > 8:
        shop["value_price"].append(0)
    elif price == 5:  # > 4 and price <= 6
        shop["value_price"].append(1)
    elif price > 3 and price < 5:
        shop["value_price"].append((price - 3)/(5 - 3))
    elif price > 5 and price <= 8:
        shop["value_price"].append((8 - price)/(8 - 5))
    if price > 8:
        shop["value_price"].append(1)
    elif price <= 4:
        shop["value_price"].append(0)
    elif price > 4 and price <= 8:
        shop["value_price"].append((price - 4)/(8 - 6))


def inference(shop):
    shop["value"] = [[] for _ in range(3)]
    for i in range(len(shop["value_service"])):
        for j in range(len(shop["value_price"])):
            select = min(shop["value_service"][i], shop["value_price"][j])
            if i == 0 and j == 0:
                shop["value"][1].append(select)
            elif i == 0 and j == 1:
                shop["value"][0].append(select)
            elif i == 0 and j == 2:
                shop["value"][0].append(select)
            elif i == 1 and j == 0:
                shop["value"][1].append(select)
            elif i == 1 and j == 1:
                shop["value"][1].append(select)
            elif i == 1 and j == 2:
                shop["value"][1].append(select)
            elif i == 2 and j == 0:
                shop["value"][2].append(select)
            elif i == 2 and j == 1:
                shop["value"][2].append(select)
            elif i == 2 and j == 2:
                shop["value"][1].append(select)


def defuzzification(shop):
    sum_1 = 0
    sum_2 = 0
    for i in range(len(shop["value"])):
        select = max(shop["value"][i])
        if i == 0:
            sum_1 += select*40
        elif i == 1:
            sum_1 += select*65
        elif i == 2:
            sum_1 += select*90
        sum_2 += select

    shop["z_value"] = sum_1/sum_2


data = pd.read_excel(
    r'C:\Users\rifqi\OneDrive\Documents\Folder Tugas Iqi\Semester 4\Pengantar Kecerdasan Buatan\Fuzzy Logic\bengkel.xlsx')

price_column = data["Price"]
service_column = data["Service"]
id_column = data["ID"]


shops = []
for i in range(100):
    shop = {}
    shop["id"] = id_column[i]
    shop["service"] = service_column[i]
    shop["price"] = price_column[i]
    shops.append(shop)

for i in range(100):
    fuzzification(shops[i])
    inference(shops[i])
    defuzzification(shops[i])

bests = []
for i in range(10):
    best = max(shops, key=lambda x: x["z_value"])
    bests.append(best)
    shops.remove(best)

print(bests)
data_best = pd.DataFrame(bests, columns=['id', 'service', 'price'])
print(data_best)
data_best.to_excel('10_best_shops.xlsx', sheet_name='10_best')
# print(max(shops, key=lambda x: x["z_value"]))
