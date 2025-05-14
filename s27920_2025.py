import random
import os

"""
Generator losowych sekwencji DNA w formacie FASTA

CEL PROGRAMU:
Program generuje losowe sekwencje nukleotydowe (DNA), wraz z metadanymi i statystykami,
a następnie zapisuje je w standardowym formacie FASTA.

KONTEKST ZASTOSOWANIA:
1. Informatyka - tworzenie testowych sekwencji DNA do walidacji algorytmów
2. Symulacje - generowanie danych testowych do eksperymentów obliczeniowych

"""

def generate_dna_sequence(length, name):
    """Generuje sekwencję DNA o podanej długości z wstawionym imieniem w losowym miejscu"""
    nucleotides = ['A', 'C', 'G', 'T']
    # losowe wygenerowanie sekwencji nukleotydów
    seq = [random.choice(nucleotides) for _ in range(length)]

    # Wstawienie imienia w losowym miejscu (nie zastępując istniejących nukleotydów)
    if len(name) > 0:
        insert_pos = random.randint(0, length)
        seq = seq[:insert_pos] + list(name) + seq[insert_pos:]

    return ''.join(seq)


def calculate_statistics(seq, name):
    """Oblicza statystyki sekwencji, ignorując znaki imienia"""
    # Filtrujemy sekwencję usuwając znaki imienia
    filtered_seq = [n for n in seq if n in ['A', 'C', 'G', 'T']]
    total = len(filtered_seq)

    # jeśli sekwencja ma długość 0 nie podejmujemy dalszych kroków
    if total == 0:
        return {'A': 0, 'C': 0, 'G': 0, 'T': 0, 'CG_ratio': 0}

    # zliczenie liczby wystąpień każdego z nukleotydów w pełnej sekwencji
    counts = {
        'A': filtered_seq.count('A'),
        'C': filtered_seq.count('C'),
        'G': filtered_seq.count('G'),
        'T': filtered_seq.count('T')
    }

    # zliczenie procentowego udziału każdego z nukleotydów w pełnej sekwencji
    percentages = {
        'A': (counts['A'] / total) * 100,
        'C': (counts['C'] / total) * 100,
        'G': (counts['G'] / total) * 100,
        'T': (counts['T'] / total) * 100
    }

    cg = counts['C'] + counts['G']

    # ORIGINAL:
    # at = counts['A'] + counts['T']
    # cg_ratio = (cg / (cg + at)) * 100 if (cg + at) > 0 else 0
    # MODIFIED (liczba total jest jednoznaczna z całkowitą liczba wystąpień nukleotydów c, g, a oraz t. Zbędnym zatem jest wykonywanie działań arytmetycznych jak cg + at skoro ich wynik mamy już dostępny pod zmienną total)
    cg_ratio = (cg / total) * 100 if total > 0 else 0
    # MODIFIED END
    percentages['CG_ratio'] = cg_ratio
    return percentages


def save_fasta_file(seq_id, description, sequence, filename):
    """Zapisuje sekwencję do pliku w formacie FASTA"""
    # ORIGINAL:
    # with open(filename, 'w') as f:
    #     f.write(f">{seq_id} {description}\n")
    #     f.write(f"{sequence}\n")
    # MODIFIED (w przypadku wystąpienia 2 sekwencji o takim samym id stary plik byłby nadpisywany, zważywszy na potencjalne różnice, np. opis sekwencji, jakie mogą wystąpić warto byłoby zachować obie wersje):

    # wytłumaczenie dokonanych zmian:
    # sprawdzamy czy istnieje już plik o nazwie takiej samej jak ta przekazana do funkcji.
    # Jeśli warunek jest spełniony, zgodnie z konwencją windows znajdujemy najniższą wartość n która spełnia warunek unikatowej kombinacji nazwa pliku + n.
    # Nazwa konstruowana jest zgodnie z formatem <filename (n)>.
    # Po znalezeniu odpowiedniej wartości n zawartość jest zapisywana do nowo utworzonego pliku
    if os.path.exists(filename):
        filename_append = 1
        while os.path.exists(f"{filename} ({filename_append})"):
            filename_append += 1
        filename = f"{filename} ({filename_append})"
        # otwarcie strumienia do pliku wraz z automatycznym czyszczeniem zasobów po zakończeniu działanie
        with open(filename, 'w') as f:
            write_fasta_file_contents(seq_id, description, sequence, f)
    else:
        with open(filename, 'w') as f:
            write_fasta_file_contents(seq_id, description, sequence, f)
    # nazwa pliku zwrócona informacyjnie jako że wywołanie metody może zmieniać jej stan
    return filename
def write_fasta_file_contents(seq_id, description, sequence, file):
    """ dokonuje faktycznego zapisu do pliku """
    file.write(f">{seq_id} {description}\n")
    file.write(f"{sequence}\n")
# MODIFIED END

def main():
    print("Generator sekwencji DNA w formacie FASTA")

    # Pobieranie danych od użytkownika
    try:
        # weryfikujemy czy wartość podana jest nieujemna i całkowita
        length = int(input("Podaj długość sekwencji: "))
        if length <= 0:
            print("Długość sekwencji musi być większa od 0.")
            return
    except ValueError:
        print("Nieprawidłowa długość sekwencji. Podaj liczbę całkowitą.")
        return

    seq_id = input("Podaj ID sekwencji: ").strip()
    # weryfikujemy czy użytkownik faktycznie podał wartość
    if not seq_id:
        print("ID sekwencji nie może być puste.")
        return

    # pobieramy opis sekwencji i imie użytkownika w formacie pozbawionym wiodących i kończących białych znaków
    description = input("Podaj opis sekwencji: ").strip()
    name = input("Podaj imię: ").strip()

    # Generowanie sekwencji
    sequence = generate_dna_sequence(length, name)

    # Obliczanie statystyk
    stats = calculate_statistics(sequence, name)

    # Zapisywanie do pliku
    filename = save_fasta_file(seq_id, description, sequence, f"{seq_id}.fasta")

    # ORIGINAL:

    print(f"\nSekwencja została zapisana do pliku {filename}")
    print("Statystyki sekwencji:")
    # Wyświetlanie wyników
    # print(f"A: {stats['A']:.1f}%")
    # print(f"C: {stats['C']:.1f}%")
    # print(f"G: {stats['G']:.1f}%")
    # print(f"T: {stats['T']:.1f}%")
    # print(f"%CG: {stats['CG_ratio']:.1f}")

    # MODIFIED
    # (w wersji wygenerowanej przez LLM mieliśmy twardo zakodowane wypisanie statystyk sekwencji. Jeśli zawartość statysyk zmieniłaby się (np. zechcielibyśmy żeby zawierały one częstotliwość występowanie amino kwasu leu) należałoby manualnie dopisywać wypisanie kolejnych danych)
    for (key, value) in zip(stats.keys(), stats.values()):
        print(f"\t{key}: {value:.2f}%")
    # MODIFIED END

if __name__ == "__main__":
    main()