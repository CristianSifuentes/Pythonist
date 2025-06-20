# Python Features
# Object-Oriented Language
# Interpreted Language
# Dynamic Typing
x = 5
y = 3
c = x + y
print(c)


# Create a code that receives a letter and responds
# if it is a vowel or a consonant
def es_vocal(letra):
  vocales = ['A', 'E', 'I', 'O', 'U']
  if letra in vocales:
    print('La letra introducida es una vocal')
  else:
    print('La letra introducida es una consonante')

n = True
while(n):
  es_vocal(letra= input('Ingrese una letra del español').upper())
  respuesta = input('¿Desea continuar? S/N: ').lower()
  n = (respuesta == 's')


  # Realizar un código que genere una salida como
# la siguiente:
niveles = int(input("Ingrese el número de niveles: "))
for i in range(1, niveles + 1):
  print("*" * i)



c = 1
for i in range(5,0,-1):
  print(("-" * i)+("*")*c)
  c = c + 1


data = [10, 20, 30, 40, 50]
data.remove(30)
print(data)

data.insert(2,30)
print(data)

data = [x for x in data if x != 20]
print(data)

value_to_remove = 50
while value_to_remove in data:
  data.remove(value_to_remove)

print(data)

# Remove an item from the list by position
del data[1] #delete second element
print(data)
data.append(60)
data.append(70)
print(data)
del data[1:2]   # delete slice
print(data)

# Add items to a list
data.extend([80,90])
print(data)


# while loop
number = 612
guess = number / 2
epsilon = 1e-9

while abs(guess * guess - number) > epsilon:
  guess = (guess + number / guess) / 2

print(f"Square root of {number} ≈ {guess} ")


# Create a function that tells you whether a number is positive, negative, or zero
# TIP: You may need to use conditionals within your function

def validation(value: int):
  if value > 0:
    print("Es positivo")
  elif value < 0:
    print("Es negativo")
  else:
    print("Es cero")

validation(0)


# Using map and lambda functions
# Returns an object from the results
# after applying a given function
# Syntax = map(T, V);
# T = transformation function,
# V = vector of data to be transformed
# Single expression to execute a block of actions
numeros = [1,2,3,4,5]
cuadrados = map(lambda x: x**2, numeros)

print(list(cuadrados))

a = [1, 2, 3]
b = [10, 20, 30]


resultado = list(map(lambda x, y: x + y,a, b))