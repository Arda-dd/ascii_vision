import cv2
import sys
import PIL.Image
from main import process_frame # Az önce yaptığımız main.py'den o fonksiyonu çağır

def baslat():
    # 1. Bilgisayarın kamerasını aç
    kamera = cv2.VideoCapture(0)
    
    if not kamera.isOpened():
        print("Hata: Kamera bulunamadı!")
        return

    print("Kamera açılıyor... Kapatmak için klavyeden 'q' tuşuna basın.")
    
    try:
        while True:
            # 2. Kameradan anlık bir kare (fotoğraf) çek
            kontrol, kare = kamera.read()
            if not kontrol:
                break

            # 3. Kameradan gelen görüntüyü Python'ın anlayacağı dile çevir
            kare_rgb = cv2.cvtColor(kare, cv2.COLOR_BGR2RGB)
            pil_resim = PIL.Image.fromarray(kare_rgb)

            # 4. Bu kareyi ASCII karakterlerine dönüştür (Genişlik 100 karakter olsun)
            sonuc = process_frame(pil_resim, new_width=100)

            # 5. Ekrana bas (Terminalin titrememesi için özel bir kod)
            # \033[H kodu imleci temizlemeden en başa çeker, böylece görüntü akar.
            sys.stdout.write("\033[H" + sonuc)
            sys.stdout.flush()

            # Eğer klavyeden 'q' tuşuna basılırsa döngüyü kır (Kapat)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        # 6. İş bitince kamerayı serbest bırak
        kamera.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    baslat()