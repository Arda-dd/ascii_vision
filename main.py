import PIL.Image
import PIL.ImageEnhance

# Karakter setimiz: En soldaki en koyu ($), en sağdaki en açık (.) yerleri temsil eder.
CHAR_SET = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunfjt1{}[?-_+~<>i!lI;:,\"^`'. "

def process_frame(pil_image, new_width=100):
    """Bu fonksiyon bir fotoğrafı alır ve onu renkli karakterlere dönüştürür."""
    
    # 1. Resmin boyutunu terminale sığacak şekilde ayarla
    width, height = pil_image.size
    aspect_ratio = height / width
    # 0.52 çarpanı önemli: Karakterler uzun olduğu için görüntünün yayvan durmasını engeller.
    new_height = int(new_width * aspect_ratio * 0.52)
    img = pil_image.resize((new_width, new_height))

    # 2. Renkleri daha canlı yap (Terminale basınca güzel görünsün)
    img = PIL.ImageEnhance.Contrast(img).enhance(1.5)
    
    pixels = img.load()
    ascii_output = ""
    
    for y in range(new_height):
        for x in range(new_width):
            r, g, b = pixels[x, y][:3] # O noktanın Kırmızı, Yeşil, Mavi değerini al
            
            # Bu noktanın ne kadar parlak olduğunu hesapla (Gri tonlama mantığı)
            brightness = int(0.299*r + 0.587*g + 0.114*b)
            
            # Parlaklığa göre listeden bir karakter seç
            char_index = brightness * (len(CHAR_SET) - 1) // 255
            char = CHAR_SET[char_index]
            
            # Karakteri kendi rengiyle (ANSI koduyla) yan yana diz
            ascii_output += f"\033[38;2;{r};{g};{b}m{char}"
            
        ascii_output += "\033[0m\n" # Satır bitince rengi sıfırla ve alt satıra geç
    
    return ascii_output