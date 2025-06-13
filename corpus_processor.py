# corpus_processor.py

import math
from collections import defaultdict, Counter
import matplotlib.pyplot as plt

# ---------- DATOS DE ENTRADA ----------
corpus = [
    "La inteligencia artificial es fascinante",
    "Python es poderoso y flexible",
    "Aprender ciencia de datos es útil",
    "La inteligencia artificial está transformando el mundo"
]

# ---------- FUNCIONES DE PROCESAMIENTO ----------

def limpiar_palabras(frase: str) -> list:
    """Convierte a minúsculas y separa en palabras sin signos."""
    return [palabra.strip(".,;:").lower() for palabra in frase.split()]

def construir_vocabulario(lista_frases: list) -> set:
    """Devuelve un conjunto con todas las palabras únicas."""
    vocabulario = set()
    for frase in lista_frases:
        vocabulario.update(limpiar_palabras(frase))
    return vocabulario

def contar_frecuencias(corpus: list) -> dict:
    """Devuelve un diccionario con la frecuencia de cada palabra."""
    contador = defaultdict(int)
    for frase in corpus:
        for palabra in limpiar_palabras(frase):
            contador[palabra] += 1
    return dict(contador)

def resumen_estadistico(frecuencias: dict) -> tuple:
    """Devuelve media, varianza y moda de las frecuencias."""
    valores = list(frecuencias.values())
    media = sum(valores) / len(valores)
    varianza = sum((x - media) ** 2 for x in valores) / len(valores)
    moda = max(frecuencias.items(), key=lambda x: x[1])
    return (media, varianza, moda)

# ---------- OBJETO CIENTÍFICO ----------

class CorpusAnalisis:
    def __init__(self, corpus):
        self.corpus = corpus
        self.vocabulario = construir_vocabulario(corpus)
        self.frecuencias = contar_frecuencias(corpus)
    
    def imprimir_resumen(self):
        print(f"Total de frases: {len(self.corpus)}")
        print(f"Vocabulario único ({len(self.vocabulario)}): {self.vocabulario}")
        media, varianza, moda = resumen_estadistico(self.frecuencias)
        print(f"Media de frecuencias: {media:.2f}")
        print(f"Varianza: {varianza:.2f}")
        print(f"Palabra más frecuente: '{moda[0]}' con {moda[1]} apariciones")
    
    def graficar(self):
        palabras = list(self.frecuencias.keys())
        conteos = list(self.frecuencias.values())
        plt.figure(figsize=(10, 5))
        plt.bar(palabras, conteos, color="skyblue")
        plt.title("Frecuencia de Palabras en el Corpus")
        plt.xlabel("Palabras")
        plt.ylabel("Frecuencia")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

# ---------- EJECUCIÓN PRINCIPAL ----------

if __name__ == "__main__":
    analisis = CorpusAnalisis(corpus)
    analisis.imprimir_resumen()
    analisis.graficar()
