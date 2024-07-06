import os
from transformers import pipeline, set_seed

# Definir el generador GPT-2
generator = pipeline("text-generation", model="gpt2")

def main_menu():
    # ASCII art del título
    ascii_art = """
      _____                 _                                               _                         
     |  __ \               | |                                             | |                        
     | |  | | __ _  ___  __| |_ __ __ _  __ _  ___  _ __    _ __ ___  _   _| |_ __ _  __ _  ___ _ __  
     | |  | |/ _` |/ _ \/ _` | '__/ _` |/ _` |/ _ \| '_ \  | '_ ` _ \| | | | __/ _` |/ _` |/ _ \ '_ \ 
     | |__| | (_| |  __/ (_| | | | (_| | (_| | (_) | | | | | | | | | | |_| | || (_| | (_| |  __/ | | |
     |_____/ \__,_|\___|\__,_|_|  \__,_|\__, |\___/|_| |_| |_| |_| |_|\__,_|\__\__,_|\__, |\___|_| |_|
                                         __/ |                                        __/ |           
                                        |___/                                        |___/            
        """

    while True:
        print(f"\n{ascii_art}")
        print("\n=== Menú Principal ===")
        print("1. Mutar (mejorar) código")
        print("2. Entrenar con experiencia acumulada")
        print("3. Salir")

        try:
            opcion = int(input("Seleccione una opción: "))
            if opcion == 1:
                mutate_code_menu()
            elif opcion == 2:
                # Verificar si ya se ha mejorado un código antes de llamar a entrenar con experiencia
                if 'improved_code' in globals():
                    train_with_experience(improved_code)
                else:
                    print("Primero debe mejorar un código antes de entrenar con experiencia.")
            elif opcion == 3:
                print("Saliendo...")
                break
            else:
                print("Opción no válida. Inténtalo de nuevo.")
        except ValueError:
            print("Por favor, ingrese un número válido.")

def mutate_code_menu():
    global improved_code  # Declarar improved_code como global al inicio de la función
    file_path = input("Ingrese la ruta al archivo de código: ")
    language = input("Ingrese el lenguaje de programación del código (por ejemplo, Python, Java, C++): ")

    if not os.path.exists(file_path):
        print(f"Error: El archivo {file_path} no existe.")
        return

    try:
        with open(file_path, "r") as file:
            code = file.read()

        improved_code, improvement = improve_code_in_sections(code, language)

        # Pedir al usuario que ingrese la ruta de salida para guardar el archivo mejorado
        output_path = input("Ingrese la ruta para guardar el archivo mejorado o deje en blanco para generar automáticamente: ").strip()

        if output_path == "":
            # Generar una nueva ruta automáticamente
            file_name, file_extension = os.path.splitext(os.path.basename(file_path))
            output_path = os.path.join(os.path.dirname(file_path), file_name + "_improved" + file_extension)

        # Guardar el código mejorado en el nuevo archivo
        with open(output_path, "w") as file:
            file.write(improved_code)

        print(f"El código ha sido mejorado y guardado exitosamente en: {output_path}")
        print(f"Mejora detectada: {improvement}")

        # Llamar a la función para entrenar con experiencia acumulada si es necesario
        if 'improved_code' in globals():
            train_with_experience(improved_code)

    except FileNotFoundError:
        print(f"Error: El archivo {file_path} no se pudo encontrar.")

    except Exception as e:
        print(f"Error al mejorar el código: {str(e)}")

def improve_code_in_sections(code, language):
    try:
        set_seed(42)  # Asegura reproducibilidad
        max_section_length = 500  # Longitud máxima de cada sección

        # Dividir el código en secciones manejables
        sections = [code[i:i + max_section_length] for i in range(0, len(code), max_section_length)]
        improved_sections = []

        for section in sections:
            prompt = f"Improve the following {language} code: {section}"
            max_length = len(prompt) + len(section) + 200  # Añadir margen adicional de tokens
            generated = generator(prompt, max_length=max_length, num_return_sequences=1, truncation=True, pad_token_id=50256)

            improved_section = generated[0]["generated_text"][len(prompt):].strip()
            improved_sections.append(improved_section)

        improved_code = "\n".join(improved_sections)
        return improved_code, "Auto-generated improvement"

    except IndexError as e:
        print(f"Error al mejorar el código: {e}")
        return code, "No improvement (index error)"

    except Exception as e:
        print(f"Error al mejorar el código: {e}")
        return code, "No improvement (error)"

def train_with_experience(improved_code):
    experience_folder = "experience"
    os.makedirs(experience_folder, exist_ok=True)
    experience_file = os.path.join(experience_folder, "experience.txt")

    try:
        with open(experience_file, "a") as f:
            f.write("\n=== Nueva Experiencia ===\n")
            f.write(improved_code)
            f.write("\n=========================\n")
        print("El código mejorado se ha guardado como experiencia acumulada.")
    except Exception as e:
        print(f"Error al guardar la experiencia acumulada: {str(e)}")

if __name__ == "__main__":
    main_menu()

