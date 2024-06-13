import sys

filepath = sys.argv[1]
with open(filepath, 'r') as f:
    lines = f.readlines()

print(lines)

lista_initiala = ['siruri', 'clasa', 'cana', 'lungimea', 'controale', 'pisica', 'catel']

lista_finala = [val.upper() for val in lista_initiala if len(val) % 2 !=0]
print(lista_finala)

sir = "abcd"
val = "0123"

lista_tupluri = []

for litera in sir:
    for cifra in val:
        lista_tupluri.append((litera, cifra))

lst_tpl = [(litera, cifra) for litera in sir for cifra in val]

print(lista_tupluri)
print(lst_tpl)