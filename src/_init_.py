import os
from PIL import Image, ImageOps
import numpy as np

script_path = os.path.abspath(__file__)
script_dir = os.path.dirname(script_path)
input_image_path = f"{script_dir}/input_image.jpeg"


def resize_and_prepare_for_print(image_path, output_path, hoop_width_cm, hoop_height_cm, padding_cm, dpi):
    # Converter dimensões de centímetros para pixels usando DPI
    dpi_scale = dpi / 2.54  # 1 polegada = 2.54 centímetros
    hoop_width_px = int(hoop_width_cm * dpi_scale)
    hoop_height_px = int(hoop_height_cm * dpi_scale)
    padding_px = int(padding_cm * dpi_scale)
    
    # Abrir a imagem
    image = Image.open(image_path)
    
    # Calcular as dimensões internas efetivas do bastidor, subtraindo o padding
    inner_width_px = hoop_width_px - 2 * padding_px
    inner_height_px = hoop_height_px - 2 * padding_px
    
    # Redimensionar a imagem para caber dentro das dimensões do bastidor com padding
    aspect_ratio = min(inner_width_px / image.width, inner_height_px / image.height)
    new_width = int(image.width * aspect_ratio)
    new_height = int(image.height * aspect_ratio)
    resized_image = image.resize((new_width, new_height), Image.LANCZOS)
    
    # Criar uma imagem com fundo branco para folha A4
    a4_width_cm = 21.0  # Largura da folha A4 em centímetros
    a4_height_cm = 29.7  # Altura da folha A4 em centímetros
    a4_width_px = int(a4_width_cm * dpi_scale)
    a4_height_px = int(a4_height_cm * dpi_scale)
    background = Image.new('RGB', (a4_width_px, a4_height_px), (255, 255, 255))
    
    # Centralizar a imagem redimensionada no fundo A4
    x_offset = (a4_width_px - new_width) // 2
    y_offset = (a4_height_px - new_height) // 2
    background.paste(resized_image, (x_offset, y_offset))
    
    # Converter a imagem para escala de cinza
    gray_image = ImageOps.grayscale(background)
    
    # Converter a imagem para um array NumPy
    np_image = np.array(gray_image)
    
    # Binarizar a imagem para manter apenas a cor preta
    threshold = 128  # Limiar para binarização
    binary_image = np.where(np_image > threshold, 255, 0).astype(np.uint8)
    
    # Converter de volta para uma imagem Pillow
    final_image = Image.fromarray(binary_image)
    
    # Salvar a imagem final
    final_image.save(output_path)
    print(f'Imagem redimensionada, com padding e apenas preto salva em: {output_path}')

# Exemplo de uso
resize_and_prepare_for_print(
    input_image_path,
    'prepared_image_for_print.jpg',
    hoop_width_cm=10.0,
    hoop_height_cm=10.0,
    padding_cm=0,
    dpi=300
)
