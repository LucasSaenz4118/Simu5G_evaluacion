import pandas as pd
import sys

def clean_sheet_name(name):
    invalid_chars = ['\\', '/', '*', '[', ']', ':', '?']
    for char in invalid_chars:
        name = name.replace(char, '_')
    return name[:31]  # Los nombres de hoja en Excel tienen un límite de 31 caracteres

def segment_file(file_path):
    # Leer solo la fila del encabezado
    header_df = pd.read_csv(file_path, nrows=0)
    
    # Leer las filas de datos saltando las primeras 127 filas
    data_df = pd.read_csv(file_path, skiprows=128)
    
    # Eliminar las dos últimas filas
    data_df = data_df.iloc[:-2]
    
    # Combinar encabezado con los datos
    data_df.columns = header_df.columns
    
    print("Columnas del DataFrame:", data_df.columns)  # Verificar nombres de columnas

    if 'name' not in data_df.columns:
        print("Error: La columna 'name' no existe en el archivo CSV.")
        return

    unique_titles = data_df['name'].unique()
    output_file_path = f'{file_path.split(".")[0]}_util.xlsx'

    with pd.ExcelWriter(output_file_path, engine='openpyxl') as writer:
        for name in unique_titles:
            df_segment = data_df[data_df['name'] == name]
            sheet_name = clean_sheet_name(name)
            df_segment.to_excel(writer, sheet_name=sheet_name, index=False)
    print(f'Segmented file saved to {output_file_path}')

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python segmentar_vec.py <path_to_csv_file>")
    else:
        file_path = sys.argv[1]
        segment_file(file_path)

