import random
import os


def generate_dna_sequence(length, name):
    """Generuje sekwencję DNA o podanej długości z wstawionym imieniem w losowym miejscu"""
    nucleotides = ['A', 'C', 'G', 'T']
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

    if total == 0:
        return {'A': 0, 'C': 0, 'G': 0, 'T': 0, 'CG_ratio': 0}

    counts = {
        'A': filtered_seq.count('A'),
        'C': filtered_seq.count('C'),
        'G': filtered_seq.count('G'),
        'T': filtered_seq.count('T')
    }

    percentages = {
        'A': (counts['A'] / total) * 100,
        'C': (counts['C'] / total) * 100,
        'G': (counts['G'] / total) * 100,
        'T': (counts['T'] / total) * 100
    }

    cg = counts['C'] + counts['G']
    at = counts['A'] + counts['T']
    cg_ratio = (cg / (cg + at)) * 100 if (cg + at) > 0 else 0

    percentages['CG_ratio'] = cg_ratio
    return percentages


def save_fasta_file(seq_id, description, sequence, filename):
    """Zapisuje sekwencję do pliku w formacie FASTA"""
    with open(filename, 'w') as f:
        f.write(f">{seq_id} {description}\n")
        f.write(f"{sequence}\n")


def main():
    print("Generator sekwencji DNA w formacie FASTA")

    # Pobieranie danych od użytkownika
    try:
        length = int(input("Podaj długość sekwencji: "))
        if length <= 0:
            print("Długość sekwencji musi być większa od 0.")
            return
    except ValueError:
        print("Nieprawidłowa długość sekwencji. Podaj liczbę całkowitą.")
        return

    seq_id = input("Podaj ID sekwencji: ").strip()
    if not seq_id:
        print("ID sekwencji nie może być puste.")
        return

    description = input("Podaj opis sekwencji: ").strip()
    name = input("Podaj imię: ").strip()

    # Generowanie sekwencji
    sequence = generate_dna_sequence(length, name)

    # Obliczanie statystyk
    stats = calculate_statistics(sequence, name)

    # Zapisywanie do pliku
    filename = f"{seq_id}.fasta"
    save_fasta_file(seq_id, description, sequence, filename)

    # Wyświetlanie wyników
    print(f"\nSekwencja została zapisana do pliku {filename}")
    print("Statystyki sekwencji:")
    print(f"A: {stats['A']:.1f}%")
    print(f"C: {stats['C']:.1f}%")
    print(f"G: {stats['G']:.1f}%")
    print(f"T: {stats['T']:.1f}%")
    print(f"%CG: {stats['CG_ratio']:.1f}")


if __name__ == "__main__":
    main()