import sys

ALLOWED_MODES = ('balance', 'sale', 'purchase', 'account', 'warehouse', 'overview') # dozwolone tryby programu
ALLOWED_COMMANDS = ('balance', 'purchase', 'sale', 'stop') # dozwolone komendy

mode = sys.argv[1] # tryb programu
balance = 1000.0 # poczatkowe saldo
store = {
    'chleb': {'count': 2, 'price': 10.0},
    'mleko': {'count': 12, 'price': 4.0}
} # magazyn
logs = [] # historia operacji

if mode not in ALLOWED_MODES:
    print("Niedozwolony tryb programu!")

while True:
    command = input("Wpisz komendę: ")

    if command not in ALLOWED_COMMANDS:
        print("Niedozwolona komenda!")
        continue
    if command == 'stop':
        print("Koniec programu!")
        break

    if command == 'balance':
        amount = float(input("Kwota salda: "))
        if (amount < 0) and (balance + amount < 0):
            print("Nie masz środków na koncie!")
            continue
        balance += amount
        log = f"Zmiana saldo o: {amount}"
        logs.append(log)
    elif command == 'purchase':
        product_name = input(("Nazwa produktu: "))
        product_count = int(input("Ilość sztuk: "))
        product_price = float(input("Cena za sztukę: "))
        product_total_price = product_count * product_price
        if product_total_price > balance:
            print(f"Cena za towary ({product_total_price}) przekracza wartość salda {balance}.")
            continue
        else:
            balance -= product_total_price
            if not store.get(product_name):
                store[product_name] = {'count': product_count, 'price': product_price}
            else:
                store_product_count = store[product_name]['count']
                store[product_name] = {
                    'count': store_product_count+product_count,
                    'price': product_price}
        log = f"Dokonano zakupu produktu: {product_name} w ilości {product_count} sztuk, o cenie jednostkowej {product_price}."
        logs.append(log)
    elif command == 'sale':
        product_name = input(("Nazwa produktu: "))
        product_count = int(input("Ilość sztuk: "))
        product_price = float(input("Cena za sztukę: "))
        if not store.get(product_name):
            print("Produktu nie ma w magazynie!")
            continue
        if store.get(product_name)['count'] < product_count:
            print("Brak wystarczającej ilości towaru!")
            continue
        store[product_name] = {
            'count': store.get(product_name)['count'] - product_count,
            'price': product_price
        }
        balance += product_count * product_price
        if not store.get(product_name)['count']:
            del store[product_name]
        log = f"Dokonano sprzedaży produktu: {product_name} w ilości {product_count} sztuk, o cenie jednostkowej {product_price}."
        logs.append(log)

if mode == 'balance':
    amount = float(sys.argv[2])
    if (amount < 0) and (balance + amount < 0):
        log = "Nie masz środków na koncie!"
    else:
        balance += amount
        log = f"Zmiana saldo o: {amount}. Komentarz: {sys.argv[3]}"
    logs.append(log)
    print(f'{sys.argv[2]} {sys.argv[3]}')
elif mode == 'sale':
    product_name = sys.argv[2]
    product_count = float(sys.argv[4])
    product_price = float(sys.argv[3])
    if not store.get(product_name):
        log = "Produktu nie ma w magazynie!"
    if store.get(product_name)['count'] < product_count:
        log = "Brak wystarczającej ilości towaru!"
    store[product_name] = {
        'count': store.get(product_name)['count'] - product_count,
        'price': product_price
    }
    balance += product_count * product_price
    if not store.get(product_name)['count']:
        del store[product_name]
    log = f"Dokonano sprzedaży produktu: {product_name} w ilości {product_count} sztuk, o cenie jednostkowej {product_price}."
    logs.append(log)
    print(f'{product_name} {product_price} {product_count}')
elif mode == 'purchase':
    product_name = sys.argv[2]
    product_count = float(sys.argv[4])
    product_price = float(sys.argv[3])
    product_total_price = product_count * product_price
    if product_total_price > balance:
        log = f"Cena za towary ({product_total_price}) przekracza wartość salda {balance}."
    else:
        balance -= product_total_price
        if not store.get(product_name):
            store[product_name] = {'count': product_count, 'price': product_price}
        else:
            store_product_count = store[product_name]['count']
            store[product_name] = {
                'count': store_product_count + product_count,
                'price': product_price}
    log = f"Dokonano zakupu produktu: {product_name} w ilości {product_count} sztuk, o cenie jednostkowej {product_price}."
    logs.append(log)
    print(f'{product_name} {product_price} {product_count}')
elif mode == 'account':
    print(f'SALDO: {balance}')
elif mode == 'warehouse':
    print(f'MAGAZYN: {store}')
    print(f"{sys.argv[2]}: {store[sys.argv[2]]['count']}")
    print(f"{sys.argv[3]}: {store[sys.argv[3]]['count']}")
    print(f"{sys.argv[4]}: {store[sys.argv[4]]['count']}")
elif mode == 'overview':
    for i in range(int(sys.argv[2]), int(sys.argv[3])):
        print(logs[i])

print(logs)