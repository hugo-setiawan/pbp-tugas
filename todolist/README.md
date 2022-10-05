# Tugas Individu 4 PBP
**Hugo Sulaiman Setiawan (2106707315)**
### [Readme untuk Tugas Individu 5 PBP](#tugas-individu-5-pbp)

## URL aplikasi pada Heroku
https://pbp-tugas-hugo.herokuapp.com/todolist/

## Apa kegunaan `{% csrf_token %}` pada elemen `<form>`? Apa yang terjadi apabila tidak ada potongan kode tersebut pada elemen `<form>`?
`csrf_token` adalah salah satu mitigasi yang dilakukan untuk menghindari *Cross-Site Request Forgery* (CSRF). CSRF sendiri merupakan sejenis serangan yang dapat terjadi pada suatu aplikasi web dimana sebuah *user* yang sudah diotentikasi serta dipercaya oleh suatu website mengirimkan *request* tertentu tanpa dilakukan ataupun diketahui oleh *user*. Dalam kata lain, terjadi *spoofing* atas *user* tersebut dimana sebuah request dikirimkan mengatasnamakan user tersebut namun sebenarnya user tersebut tidak melakukan request tersebut. Misal, seorang penjahat dapat melakukan CSRF dimana ia mengirimkan request yang seakan-akan berasal dari nasabah untuk melakukan transfer uang, padahal request tersebut bukan kehendak dari serta tidak diketahui oleh user. 

Untuk memitigasi kemungkinannya terjadi CSRF, diperlukan cara untuk memeriksa dan memvalidasi bahwa request yang diterima oleh web merupakan request yang dibuat oleh user melalui halaman web yang sesuai. Untuk melakukan hal tersebut, digunakanlah sebuah CSRF token. Implementasi CSRF token dalam django menggunakan konsep *synchronizer token pattern* dimana server mengenerate suatu string yang acak, untuk kemudian dimasukkan ke dalam form sebagai hidden field. Saat form sudah diisi oleh user dan dikembalikan ke server melalui request, server akan memeriksa CSRF token yang ada pada request tersebut dan membandingkannya dengan CSRF token yang sudah dibuat sebelumnya. Jika kedua token sama, maka dapat dipastikan bahwa request berasal dari user yang melakukan submit pada form dari server. Jika kedua token tidak sama, maka terdapat kemungkinan bahwa request tidak benar-benar berasal dari user. `{% csrf_token %}` merupakan sebuah *template tag* yang berfungsi untuk mengenerate dan menghasilkan hidden field untuk melakukan implementasi *synchronizer token pattern* pada suatu aplikasi web berbasis Django.

## Apakah kita dapat membuat elemen `<form>` secara manual (tanpa menggunakan generator seperti `{{ form.as_table }}`? Jelaskan secara gambaran besar bagaimana cara membuat `<form>` secara manual.
Ya, elemen form dapat dibuat secara manual tanpa menggunakan generator. Salah satu contoh dari pembuatan `<form>` secara manual dapat dilihat pada tugas saya sebagai berikut:
```html
<form method="post" action="modify-task/">
    {% csrf_token %}
    <input type="hidden" name="task_pk" value={{task.pk}}>
    <button name="action" value="delete"> Hapus Task
</form>
```
Secara garis besar, pembuatan `<form>` secara manual dapat dilakukan sebagai berikut:
1. Membuat elemen `<form>` serta menentukan action dan method yang akan digunakan untuk men-submit.
2. Menambahkan elemen-elemen interaktif seperti `<input>` dan `<button>` yang dapat digunakan untuk men-submit data.

## Jelaskan proses alur data dari submisi yang dilakukan oleh pengguna melalui HTML form, penyimpanan data pada database, hingga munculnya data yang telah disimpan pada template HTML.
Proses alur data dari submisi melalui `<form>` hingga munculnya data pada template HTML adalah sebagai berikut:
1. Saat pengguna melakukan submisi melalui HTML form, maka sebuah request (sesuai tipe request yang didefinisikan pada attribute dari tag `<form>`) akan dibuat kepada endpoint yang sesuai dengan attribute action.
2. Endpoint yang didefinisikan pada attribute action dari form akan menerima request dari client
3. Fungsi pada endpoint dapat melakukan validasi form menggunakan `is_valid()`.
4. Fungsi akan melakukan pemrosesan pada data, kemudian dapat menyimpan data pada database melalui models yang ada
5. Setelah data disimpan pada database, data tersebut dapat diambil oleh fungsi-fungsi lain, sehingga dapat dirender pada template HTML 

## Penjelasan implementasi
### Pembuatan app `todolist`
Pertama-tama, app `todolist` dibuat dengan perintah `startapp todolist` pada `manage.py`.
### Model `Task` pada ```models.py```
Untuk tugas ini, saya menambahkan model `Task` sesuai dengan ketentuan yang telah diberikan pada dokumen soal melalui implementasi pada `models.py` sebagai berikut:
```python
class Task(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    date = models.DateField()
    title = models.TextField()
    description = models.TextField()
    is_finished = models.BooleanField(default=False)
```
Setelah menambahkan model tersebut, saya melakukan `makemigrations` dan `migrate` agar model tersebut dapat tercermin pada *database*.

### Pembuatan halaman (*form*) registrasi, login, dan logout
Untuk mengimplementasi *requirement* ini, terdapat dua langkah utama:
1. Implementasi pada view <br> 
Saya mengimplementasi registrasi user pada view menggunakan `UserCreationForm`, dan untuk login serta logout diimplementasikan dengan memanfaatkan fungsi yang tersedia pada `django.auth`. 

2. Implementasi pada template <br>
Saya membuat dua template, `register.html` dan `login.html`. Template tersebut mengandung sebuah `<form>` yang akan mengirimkan data melalui POST request kepada endpoint serta fungsi yang sesuai agar fungsi registrasi, login, dan logout dapat berjalan dengan baik.

### Membuat halaman utama todolist
Untuk mengimplementasi *requirement* ini, saya membuat view `show_todolist(request)` yang akan mengambil `Task` yang dibuat oleh user yang sedang log in. Untuk memastikan halaman ini hanya bisa diakses ketika user sudah terlogin, ditambahkan decorator `@login_required(login_url='/todolist/login/')`. Setelah itu, saya membuat template `todolist.html` yang berfungsi menampilkan data todolist, serta mengandung button-button yang memiliki fungsi tertentu.

### Membuat halaman form untuk pembuatan task
Pertama, saya membuat forms dalam Django sebagai berikut:
```python
class CreateTaskForm(forms.Form):
    title = forms.CharField(label="Judul Task")
    description = forms.CharField(label="Deskripsi Task")
```
Kemudian, form tersebut dipakai dalam view `def create_task(request)`. Fungsi ini memiliki dua kegunaan. Pertama, jika request bukan bertipe POST maka fungsi ini akan mengembalikan halaman yang berisi form untuk diisi oleh user. Kedua, jika request bertipe POST maka fungsi ini akan melakukan validasi dan menambahkan object `Task` baru ke database sesuai ketentuan.

### Membuat endpoint untuk melakukan CRUD *(Bonus)*
Untuk melakukan implementasi bonus berupa CRUD, saya membuat fungsi baru pada `views.py` yaitu `modify_task(request)`. Endpoint ini berfungsi untuk menerima POST request dari `<button>` pada `<form>` yang ada pada halaman `todolist/`. Endpoint ini dapat melakukan tiga action, yakni `finish`, `unfinish`, dan `delete`. Implementasi `modify_task` sebagai berikut:
```python
@login_required(login_url='/todolist/login/')
def modify_task(request):
    if request.method == "POST":
        pk = request.POST.get("task_pk")
        task = Task.objects.get(pk = pk)
        action = request.POST.get("action")

        # Validasi requesting user == pemilik task untuk menghindari modifikasi oleh user lain
        if request.user == task.user:
            if action == "finish":
                task.is_finished = True
                task.save()
            elif action == "unfinish":
                task.is_finished = False
                task.save()
            elif action == "delete":
                task.delete()
    return HttpResponseRedirect(reverse('todolist:show_todolist'))
``` 

### *Routing* pada ```urls.py``` untuk memetakan fungsi
Pada file `urls.py`, baik pada *root directory* maupun pada direktori untuk app, saya menambahkan ```urlpatterns``` yang bertujuan untuk memetakan *request* pada path tertentu (```/todolist/*```) ke fungsi yang sesuai pada ```views.py```. Misal, jika *path* yang diminta adalah *todo blablabla*

### Melakukan *deployment* ke Heroku
Setelah melakukan langkah-langkah di atas, saya membuat app pada Heroku, kemudian memasukkan nama app tersebut (```HEROKU_APP_NAME```) serta API key saya (```HEROKU_API_KEY```) ke dalam *actions secrets* pada repositori GitHub saya. Setelah itu, saya melakukan *commit* dan *push* sehingga perubahan pada repositori lokal akan tercermin pada GitHub, serta *actions* akan berjalan untuk mendeploy aplikasi ke Heroku.

# Tugas Individu 5 PBP
**Hugo Sulaiman Setiawan (2106707315)**

## URL aplikasi pada Heroku
https://pbp-tugas-hugo.herokuapp.com/todolist/

## Apa perbedaan dari Inline, Internal, dan External CSS? Apa saja kelebihan dan kekurangan dari masing-masing style?
**TODO**

## Jelaskan tag HTML5 yang kamu ketahui.
**TODO**

## Jelaskan tipe-tipe CSS selector yang kamu ketahui.
**TODO**

## Penjelasan implementasi
### Kustomisasi halaman register dan login
### Kustomisasi halaman create task
### Kustomisasi halaman utama todolist
### Membuat halaman menjadi *responsive*
### Menambahkan efek *hover* pada *cards* di todolist
### Melakukan *deployment* ke Heroku
Setelah melakukan langkah-langkah di atas, saya membuat app pada Heroku, kemudian memasukkan nama app tersebut (```HEROKU_APP_NAME```) serta API key saya (```HEROKU_API_KEY```) ke dalam *actions secrets* pada repositori GitHub saya. Setelah itu, saya melakukan *commit* dan *push* sehingga perubahan pada repositori lokal akan tercermin pada GitHub, serta *actions* akan berjalan untuk mendeploy aplikasi ke Heroku.