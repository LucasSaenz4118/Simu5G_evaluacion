import pandas as pd
import matplotlib.pyplot as plt
import os

# Cargar el archivo Excel segmentado
excel_file = 'RURAL_VEC_T_util.xlsx'

# Leer todas las hojas del archivo
xlsx = pd.ExcelFile(excel_file)
sheet_names = xlsx.sheet_names

# Crear un directorio para guardar los gráficos
output_dir = 'plots_RURAL_VALIDO'
os.makedirs(output_dir, exist_ok=True)

# Función para procesar y graficar los datos
def process_and_plot(df, sheet_name, max_series_per_plot=10):
    # Filtrar las columnas vectime y vecvalue y asegurarse de que no estén vacías
    if 'vectime' in df.columns and 'vecvalue' in df.columns:
        grouped = df.groupby(['module', 'name'])
        
        series_counter = 0
        plot_counter = 1
        
        plt.figure(figsize=(16, 10))  # Aumentar el tamaño de la figura
        
        for (module_name, group) in grouped:
            vectime = group['vectime'].dropna().astype(str)
            vecvalue = group['vecvalue'].dropna().astype(str)
            
            if not vectime.empty and not vecvalue.empty:
                # Procesar valores separados por espacios
                vectime_list = vectime.str.split().apply(pd.Series, 1).stack().astype(float).reset_index(drop=True)
                vecvalue_list = vecvalue.str.split().apply(pd.Series, 1).stack().astype(float).reset_index(drop=True)
                
                # Asegurarse de que las longitudes coincidan
                min_length = min(len(vectime_list), len(vecvalue_list))
                vectime_list = vectime_list[:min_length]
                vecvalue_list = vecvalue_list[:min_length]
                
                # Crear la gráfica con estilos mejorados
                plt.plot(vectime_list, vecvalue_list, label=f'{module_name}', marker='o', linestyle='-', markersize=4, alpha=0.7)
                series_counter += 1
                
                # Crear un nuevo gráfico si se alcanza el máximo de series por gráfico
                if series_counter >= max_series_per_plot:
                    plt.xlabel('vectime')
                    plt.ylabel('vecvalue')
                    plt.title(f'Gráfico de {sheet_name} - Parte {plot_counter}')
                    plt.legend(loc='best')
                    plt.grid(True)
                    
                    # Guardar la gráfica
                    plot_file = os.path.join(output_dir, f'{sheet_name}_part_{plot_counter}.png')
                    plt.savefig(plot_file)
                    plt.close()
                    
                    print(f'Gráfico guardado: {plot_file}')
                    
                    # Resetear el contador de series y crear una nueva figura
                    series_counter = 0
                    plot_counter += 1
                    plt.figure(figsize=(16, 10))
        
        # Guardar el último gráfico si tiene series restantes
        if series_counter > 0:
            plt.xlabel('vectime')
            plt.ylabel('vecvalue')
            plt.title(f'Gráfico de {sheet_name} - Parte {plot_counter}')
            plt.legend(loc='best')
            plt.grid(True)
            
            plot_file = os.path.join(output_dir, f'{sheet_name}_part_{plot_counter}.png')
            plt.savefig(plot_file)
            plt.close()
            
            print(f'Gráfico guardado: {plot_file}')
        
    else:
        print(f'Hoja {sheet_name} no contiene columnas vectime y vecvalue')

# Procesar y graficar cada hoja
for sheet_name in sheet_names:
    df = pd.read_excel(excel_file, sheet_name=sheet_name)
    process_and_plot(df, sheet_name)

print('Gráficos generados para todas las hojas.')
