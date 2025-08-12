import os
import re
from bs4 import BeautifulSoup, NavigableString

# --- CONFIGURACIÓN ---

TAGS_TO_PROCESS = [
    'button', 'a', 'label', 'small', 'select', 'input', 'div', 
    'span', 'p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'option'
]
CONNECTORS = ['de', 'en', 'un', 'una', 'con', 'para', 'a', 'el', 'la', 'los', 'las']

# --- FUNCIONES DE AYUDA PARA EL TEXTO ---

def clean_and_format_tooltip(text):
    if not text:
        return ""
    text = re.sub(r'[:()%\[\]{}]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    words = text.split()
    words = words[:6]
    if words and words[-1].lower() in CONNECTORS:
        words.pop()
    if not words:
        return ""
    final_text = ' '.join(words)
    return final_text.capitalize()

def get_tooltip_text(tag, soup, placeholders):
    """Aplica una serie de heurísticas para encontrar el mejor texto para el tooltip."""
    
    # Prioridad 1: Contenido de Texto Directo (con lógica mejorada)
    text_content = tag.get_text(separator=' ', strip=True)
    
    # --- INICIO DE LA MODIFICACIÓN CLAVE ---
    # Reemplazamos los placeholders para ver si queda texto estático real.
    text_without_placeholders = text_content
    for key in placeholders:
        if key in text_without_placeholders:
            text_without_placeholders = text_without_placeholders.replace(key, '')
    
    # Verificamos si queda algún carácter alfabético. Si no, el contenido es puramente
    # dinámico o son solo íconos/símbolos. En ese caso, no usamos este texto.
    if re.search(r'[a-zA-Z]', text_without_placeholders):
        return text_without_placeholders  # Usamos el texto estático que encontramos.
    # --- FIN DE LA MODIFICACIÓN CLAVE ---

    # Si la Prioridad 1 falla (porque el contenido era dinámico), continuamos con las otras.
    
    # Prioridad 2: Atributos Relevantes
    for attr in ['placeholder', 'name', 'id']:
        if tag.has_attr(attr) and tag[attr]:
            value = tag[attr].replace('_', ' ').replace('-', ' ')
            return value

    # Prioridad 3: Contexto de la URL (para <a>)
    if tag.name == 'a' and tag.has_attr('href'):
        href_value = tag['href']
        # Restauramos el contenido original de href si era un placeholder
        if href_value in placeholders:
            href_value = placeholders[href_value]
        
        match = re.search(r"\{%\s*url\s*['\"]([^'\"]+)['\"].*?%\}", href_value)
        if match:
            return match.group(1).replace('_', ' ')

    # Prioridad 4: Contenido de Variables de Plantilla (Heurística de respaldo)
    # Buscamos el nombre de la variable dentro del placeholder original
    tag_content_str = ''.join(str(c) for c in tag.contents)
    if tag_content_str in placeholders:
        original_django_tag = placeholders[tag_content_str]
        match = re.search(r'\{\{\s*(.*?)\s*\}\}', original_django_tag)
        if match:
            var_name = match.group(1).split('|')[0].strip()
            return var_name.split('.')[ -1].replace('_', ' ')

    # Prioridad 5: Contexto Jerárquico (para <div>)
    if tag.name == 'div':
        header = tag.find(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
        if header and header.get_text(strip=True):
            # Re-evaluamos el texto del header para asegurarnos de que no sea dinámico
            header_text = get_tooltip_text(header, soup, placeholders)
            if header_text:
                return header_text

    return None

# --- LÓGICA PRINCIPAL DE PROCESAMIENTO ---

def add_tooltips_to_content(html_content):
    placeholders = {}
    
    def replace_django_tag(match):
        key = f"__DJANGO_PLACEHOLDER_{len(placeholders)}__"
        placeholders[key] = match.group(0)
        return key

    protected_content = re.sub(r'(\{\{.*?\}\}|\{%.*?%\}|\{#.*?#\})', replace_django_tag, html_content, flags=re.DOTALL)
    soup = BeautifulSoup(protected_content, 'html.parser')
    
    tags = soup.find_all(TAGS_TO_PROCESS)
    
    for tag in tags:
        if tag.has_attr('title'):
            continue
            
        # Pasamos el diccionario de placeholders para que la función pueda analizar el contexto original
        tooltip_text = get_tooltip_text(tag, soup, placeholders)
        
        if tooltip_text:
            formatted_tooltip = clean_and_format_tooltip(tooltip_text)
            if formatted_tooltip:
                tag['title'] = formatted_tooltip
    
    modified_html = str(soup)
    
    # Restauramos usando el diccionario inverso para manejar anidamiento
    # Primero reemplazamos los placeholders más largos (que contienen a otros)
    for key, value in sorted(placeholders.items(), key=lambda item: len(item[1]), reverse=True):
        modified_html = modified_html.replace(key, value, 1)
        
    return modified_html

def process_html_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            original_content = f.read()

        modified_content = add_tooltips_to_content(original_content)

        if original_content != modified_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(modified_content)
            print(f"✅ Tooltips añadidos/actualizados en: {filepath}")
        else:
            print(f"⚪ No se necesitaron cambios en: {filepath}")

    except Exception as e:
        print(f"❌ Error procesando el archivo {filepath}: {e}")

# --- PUNTO DE ENTRADA DEL SCRIPT ---

def main():
    print("--- Script para Añadir Tooltips Automáticos a HTML con Django (Versión 2.0) ---")
    
    try:
        root_dir = input("Por favor, introduce la ruta completa al directorio de tus plantillas: ")
    except KeyboardInterrupt:
        print("\nProceso cancelado por el usuario.")
        return

    if not os.path.isdir(root_dir):
        print(f"Error: La ruta '{root_dir}' no es un directorio válido.")
        return

    html_files = []
    for subdir, _, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.html'):
                html_files.append(os.path.join(subdir, file))

    if not html_files:
        print("No se encontraron archivos .html en el directorio especificado.")
        return

    print(f"\nSe encontraron {len(html_files)} archivos .html. Iniciando proceso...")
    
    for filepath in html_files:
        process_html_file(filepath)
        
    print("\n--- Proceso completado. ---")


if __name__ == "__main__":
    main()