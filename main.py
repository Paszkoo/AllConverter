from PIL import Image
import cairosvg
import os

def convert_image(input_file, output_file):  # Tutaj jest poprawiona deklaracja funkcji
    input_ext = os.path.splitext(input_file)[1].lower()
    output_ext = os.path.splitext(output_file)[1].lower()

    if input_ext == ".svg" and output_ext in [".png", ".jpg", ".jpeg", ".ico"]:
        cairosvg.svg2png(url=input_file, write_to=output_file)
    elif input_ext in [".png", ".jpg", ".jpeg", ".ico"] and output_ext == ".svg":
        print("Konwersja z rastrowego do SVG nie jest wspierana w tym programie.")
    else:
        with Image.open(input_file) as img:
            img.save(output_file)
        print(f"Plik zapisano jako: {output_file}")

def menu():
    print("Konwerter obrazów")
    print("1. Konwertuj JPG na PNG")
    print("2. Konwertuj PNG na JPG")
    print("3. Konwertuj SVG na PNG")
    print("4. Konwertuj PNG na ICO")
    print("5. Konwertuj ICO na PNG")
    print("6. Konwertuj JPG na ICO")
    print("7. Inne konwersje")
    print("8. Wyjście")

    choice = input("Wybierz opcję (1-8): ")

    if choice == '1':
        input_file = input("Podaj ścieżkę do pliku JPG: ")
        output_file = input("Podaj ścieżkę do zapisu pliku PNG: ")
        convert_image(input_file, output_file)
    elif choice == '2':
        input_file = input("Podaj ścieżkę do pliku PNG: ")
        output_file = input("Podaj ścieżkę do zapisu pliku JPG: ")
        convert_image(input_file, output_file)
    elif choice == '3':
        input_file = input("Podaj ścieżkę do pliku SVG: ")
        output_file = input("Podaj ścieżkę do zapisu pliku PNG: ")
        convert_image(input_file, output_file)
    elif choice == '4':
        input_file = input("Podaj ścieżkę do pliku PNG: ")
        output_file = input("Podaj ścieżkę do zapisu pliku ICO: ")
        convert_image(input_file, output_file)
    elif choice == '5':
        input_file = input("Podaj ścieżkę do pliku ICO: ")
        output_file = input("Podaj ścieżkę do zapisu pliku PNG: ")
        convert_image(input_file, output_file)
    elif choice == '6':
        input_file = input("Podaj ścieżkę do pliku JPG: ")
        output_file = input("Podaj ścieżkę do zapisu pliku ICO: ")
        convert_image(input_file, output_file)
    elif choice == '7':
        input_file = input("Podaj ścieżkę do pliku wejściowego: ")
        output_file = input("Podaj ścieżkę do zapisu pliku wyjściowego: ")
        convert_image(input_file, output_file)
    elif choice == '8':
        print("Zamykanie programu.")
        exit()
    else:
        print("Nieprawidłowy wybór, spróbuj ponownie.")


if __name__ == "__main__":
    menu()

