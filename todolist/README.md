# Tugas Individu 4 PBP
**Hugo Sulaiman Setiawan (2106707315)**

## URL aplikasi pada Heroku
https://pbp-tugas-hugo.herokuapp.com/todolist/

## Apa kegunaan `{% csrf_token %}` pada elemen `<form>`? Apa yang terjadi apabila tidak ada potongan kode tersebut pada elemen `<form>`?
*TODO*

## Apakah kita dapat membuat elemen `<form>` secara manual (tanpa menggunakan generator seperti `{{ form.as_table }}`? Jelaskan secara gambaran besar bagaimana cara membuat `<form>` secara manual.
*TODO*

## Jelaskan proses alur data dari submisi yang dilakukan oleh pengguna melalui HTML form, penyimpanan data pada database, hingga munculnya data yang telah disimpan pada template HTML.
*TODO&

## Penjelasan implementasi
### Pembuatan app `todolist`
Pertama-tama, app `todolist` dibuat dengan perintah `startapp todolist` pada `manage.py`.
### Model `Task` pada ```models.py```
Untuk tugas ini, saya menambahkan model `Task` sesuai dengan ketentuan yang telah diberikan pada dokumen soal melalui implementasi pada `models.py` sebagai berikut:
```py
class Task(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    date = models.DateField()
    title = models.TextField()
    description = models.TextField()
    is_finished = models.BooleanField(default=False)
```
Setelah menambahkan model tersebut, saya melakukan `makemigrations` dan `migrate` agar model tersebut dapat tercermin pada *database*.

### Pembuatan halaman (*form*) registrasi, login, dan logout
*TODO*

### Membuat halaman utama todolist
*TODO*

### Membuat halaman form untuk pembuatan task
*TODO*

### Membuat endpoint untuk melakukan CRUD *(Bonus)*
*TODO*

### *Routing* pada ```urls.py``` untuk memetakan fungsi
Pada file `urls.py`, baik pada *root directory* maupun pada direktori untuk app, saya menambahkan ```urlpatterns``` yang bertujuan untuk memetakan *request* pada path tertentu (```/mywatchlist/*```) ke fungsi yang sesuai pada ```views.py```. Misal, jika *path* yang diminta adalah *todo blablabla*

### Melakukan *deployment* ke Heroku
Setelah melakukan langkah-langkah di atas, saya membuat app pada Heroku, kemudian memasukkan nama app tersebut (```HEROKU_APP_NAME```) serta API key saya (```HEROKU_API_KEY```) ke dalam *actions secrets* pada repositori GitHub saya. Setelah itu, saya melakukan *commit* dan *push* sehingga perubahan pada repositori lokal akan tercermin pada GitHub, serta *actions* akan berjalan untuk mendeploy aplikasi ke Heroku.