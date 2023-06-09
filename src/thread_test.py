import concurrent.futures
import requests 

def req():
    r = requests.get("https://ru-ru.openfoodfacts.org/category/сметана/1.json")
    r_j = r.json()
    ugl = -1 
    i = 0;
    rangeAmount = 0
    if (r_j["page_count"] > 5):
        rangeAmount = 5
    else:
        rangeAmount = r_j["page_count"]
    
    for i in range(rangeAmount):
        try: r_j["products"][i]["nutriments"]["carbohydrates"]
        except:
            i = i + 1
            continue
        else:
            ugl = float(r_j["products"][i]["nutriments"]["carbohydrates"])
    if (ugl < 0):
        return [0, "Продукт не найден "]
    else:
        return [1, "В продукте " + str(ugl) + " углеводов "]
        
with concurrent.futures.ThreadPoolExecutor() as executor:
    future = executor.submit(req, 'world!')
    return_value = future.result()
    print(return_value)




print(req())