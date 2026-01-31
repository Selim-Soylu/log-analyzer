# Teknik Detaylar ve Çalışma Mantığı

Bu araç, sistem loglarını ham metin olmaktan çıkararak anlamlı ve analiz edilebilir verilere dönüştürmek amacıyla geliştirilmiştir. Performans, iz bırakmama ve modülerlik temel alınarak tasarlanmıştır.

## Backend ve Log İşleme

Sunucu tarafında **Python (Flask)** kullanılmaktadır.  
Uygulama, log dosyalarını satır satır okuyarak `config/rules.json` dosyasında tanımlı olan **regex ve anahtar kelime kalıpları** ile eşleştirir.

Bu yapı sayesinde aşağıdaki olaylar otomatik olarak tespit edilir:

- Şüpheli aktiviteler  
- Hata kayıtları  
- Güvenlik açısından kritik olaylar  

## Canlı Veri Akışı (SSE)

Canlı takip modunda, sayfa yenilemeye gerek kalmadan anlık veri akışı sağlanır.  
Bu amaçla **Server-Sent Events (SSE)** teknolojisi ve Python **generator** yapısı kullanılmıştır.

Sunucu tarafında üretilen log çıktıları, tarayıcıya sürekli ve düşük gecikmeli şekilde aktarılır.

## Statik Log Analizi

Geçmişe dönük tarama yapıldığında elde edilen tüm bulgular **bellek (RAM)** üzerinde işlenir.  
Analiz tamamlandıktan sonra sonuçlar:

- Diskte iz bırakmadan  
- Tek seferlik  
- İndirilebilir **CSV raporu**  

haline getirilir.

## Docker ve İzolasyon

Uygulama tamamen **Docker** ortamında çalışacak şekilde yapılandırılmıştır.

Host makinedeki log dizini, konteyner içindeki `/app/logs` dizinine **Volume Mapping** yöntemiyle bağlanır.  
Bu sayede:

- Host sistem izole edilir  
- Bağıl yol kullanılarak güvenli dosya erişimi sağlanır  
- Ortam bağımsız çalıştırma mümkün olur  

---

# Nasıl Çalıştırılır

Terminal üzerinden proje dizinine girerek aşağıdaki komutları sırasıyla çalıştırmanız yeterlidir:

```bash
docker build -t log-web-app .
docker run -p 5000:5000 --name altay-panel -v "${PWD}/logs:/app/logs" log-web-app
```

Uygulama başarıyla başlatıldıktan sonra, yönetim paneline aşağıdaki adres üzerinden erişilebilir:

[http://localhost:5000](http://localhost:5000)

