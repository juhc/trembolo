d1 = {'2': {'description': 'Ветчина, моцарелла, фирменный соус альфредо', 'name': 'Ветчина и сыр', 'photo': 'https://cdn.dodostatic.net/site-static/dist/611f501db3a3369fac31.svg', 'price': 399}}
d2 = {'3': {'description': 'sf, моцарелла, фирменный соус альфредо', 'name': 'Ветчина и сыр', 'photo': 'https://cdn.dodostatic.net/site-static/dist/611f501db3a3369fac31.svg', 'price': 399}}

res = dict(list(d1.items())+list(d2.items()))
print(res['2']['name'])