# Tugas Individu 6 PBP
**Hugo Sulaiman Setiawan (2106707315)**

## URL aplikasi pada Heroku
https://pbp-tugas-hugo.herokuapp.com/todolist/

## Jelaskan perbedaan antara *asynchronous programming* dengan *synchronous programming*
*Asynchronous programming* memungkinkan agar saat suatu operasi sedang berjalan, operasi-operasi lain dapat tetap berjalan dan tidak terganggu (*non-blocking*). Misal, saat suatu aplikasi yang menerapkan prinsip *async* sedang mengirimkan data ke server, maka pengguna aplikasi tersebut dapat melakukan aksi lain pada aplikasi, walaupun pengiriman data ke server masih berlangsung di *background*. 

Hal ini berbeda dengan *synchronous programming*, di mana hanya satu operasi yang dapat berjalan pada suatu waktu, sehingga jika suatu operasi sedang berjalan, maka operasi-operasi lain harus menunggu operasi tersebut selesai sebelum mereka dapat berjalan (*blocking*). Sehingga, berdasarkan contoh di atas, ketika aplikasi yang menerapkan prinsip *sync* sedang mengirimkan data ke server, pengguna tidak dapat melakukan apapun selain menunggu hal tersebut selesai.

## Penjelasan paradigma *event-driven programming* dan contoh penerapannya
*Event-driven programming* adalah suatu paradigma pemrograman yang berbasis pada *event*-*event* yang dapat terjadi, baik karena pengguna secara langsung ataupun karena hal lain. Misal, terdapat event `onclick` yang akan terjadi ketika suatu elemen di-klik oleh pengguna. Jika terjadi suatu event, suatu fungsi akan menghandle *event* tersebut sesuai dengan. 

Salah satu penerapan paradigma *event-driven programming* adalah pada aplikasi todolist ini, yang menerapkan beberapa fungsi untuk menghandle event tertentu. Misalnya, untuk menghandle event `onclick` pada tombol untuk menghapus task, didefinisikan *handler function* sebagai berikut:
```html
<!-- note: 12 pada parameter fungsi diinput oleh script menggunakan task.pk pada saat pembuatan cards, BUKAN hardcoded -->
<button ... onclick="task_change_status(12)">
```  
Sehingga, jika terjadi event `onclick` pada button tersebut, fungsi `task_change_status(12)` akan dipanggil.

Selain itu, juga terdapat fungsi yang menghandle event `submit` pada suatu form seperti berikut:
```js
$(`#form-create-task`).submit(function (e) {
    e.preventDefault();

    // url action dari form
    var actionurl = e.currentTarget.action;

    $.ajax({
        url: actionurl,
        type: "POST",
        data: $(this).serialize(),
        // EDP: handler success
        success: function(response) {
            console.log("create-task POST OK!");
            
            // tutup modal
            $("#modal-create-task").modal('toggle');
            
            // kosongkan isi form
            $("#form-create-task > div > .form-control").each(function (i) {
                $(this).val("");
            })

            // refresh task
            load_tasks();
        },

        // EDP: handler error
        error: function(xhr, resp, text) {
            console.log("create-task POST ERROR")
            console.log(xhr, resp, text);
        }
    })

})
```
Saat event `submit` terjadi pada suatu form, maka akan dihandle oleh fungsi yang didefinisikan di atas. Bahkan, dalam *handler* untuk event `submit` tersebut juga memanfaatkan *event-driven programming*, yaitu jika saat AJAX telah selesai dan mendapatkan *response* dari server, ia akan memanggil fungsi pada success. Sebaliknya, jika terjadi error, maka ia akan memanggil fungsi pada error.

## Jelaskan penerapan *asynchronous programming* pada AJAX
*Asynchronous programming* diterapkan pada AJAX dengan `XMLHTTPRequest` yang dapat berjalan secara asinkron dengan halaman aplikasi web. Hal ini sesuai dengan huruf **A** dari **A**JAX yang merupakan singkatan dari ***A**synchronous*. Saat AJAX mengirimkan `XMLHTTPRequest` ke server, pengguna masih dapat melakukan aksi pada aplikasi web. Pengiriman, serta pemrosesan `XMLHTTPRequest` dilakukan di latar belakang, sehingga tidak mengganggu pengguna.

## Penjelasan implementasi
### Membuat view untuk membantu implementasi AJAX
Terdapat beberapa view yang perlu dibuat untuk membantu dalam implementasi AJAX pada tugas ini. View-view tersebut antara lain
- `get_todolist_json()`

    ```py
    @login_required(login_url='/todolist/login/')
    def get_todolist_json(request):
        todolist = Task.objects.filter(user = request.user)
        return HttpResponse(serializers.serialize("json", todolist), content_type="application/json")
    ```

- `create_task_ajax()`

    ```py
    @login_required(login_url='/todolist/login/')
    def create_task_ajax(request):
        if request.method == "POST":
            new_task = Task(
                date = datetime.datetime.now(),
                title = request.POST.get("title"),
                description = request.POST.get("description"),
                user = request.user
            )
            new_task.save()
            return HttpResponse(status=200)

        return redirect("todolist:show_todolist")
    ```

- `delete_task_ajax()`

    ```py
    @login_required(login_url='/todolist/login/')
    def delete_task_ajax(request: HttpRequest, id):
        if request.method == "DELETE":
            task = Task.objects.get(pk = id)

            if request.user == task.user:
                task.delete()
                response = HttpResponse(status=200)
            else:
                response = HttpResponse("Task owner not the same as requesting user!", status=403)

            return response

        return HttpResponseRedirect(reverse('todolist:show_todolist'))
    ```

Selain itu, terdapat beberapa modifikasi yang dilakukan pada view `modify_task` untuk memudahkan dalam implementasi AJAX.

### Routing view baru untuk AJAX
Setelah membuat view untuk membantu implementasi AJAX, dilakukan routing agar view tersebut dapat diakses pada path tertentu. Routing dilakukan sehingga `urlpatterns` pada `urls.py` berisi seperti berikut:
```py
urlpatterns = [
    path('', show_todolist, name='show_todolist'),
    path('json/', get_todolist_json, name='get_todolist_json'),
    path('create-task/', create_task, name='create_task'),
    path('add/', create_task_ajax, name='create_task_ajax'),
    path('modify-task/', modify_task, name='modify_task'),
    path('register/', register_user, name='register_user'),
    path('login/', login_user, name='login_user'),
    path('logout/', logout_user, name='logout_user'),
    path('delete/<int:id>/', delete_task_ajax, name='delete_task_ajax'),
]
```

### Implementasi AJAX GET untuk menampilkan Task
Untuk mengimplementasikan penampilan serta *refresh* task menggunakan AJAX GET, dibuat suatu fungsi js sebagai berikut:
```js
function load_tasks() {
        console.log('loading tasks');
        $.getJSON("{%url 'todolist:get_todolist_json'%}", function(data) {
            $("#cards-parent").empty();
            $(data).each(function(i, entry) {
                $("#cards-parent").append(
                    $(`<div class="col card card-hover border border-${entry.fields.is_finished ? "success" : "danger"} px-0">`).append(
                        $('<div class="card-body">').append(
                            $(`<h4 class="card-title">`).append(
                                $(`<strong>`).append(
                                    entry.fields.title
                                )
                            )
                        ).append(
                            $(`<h5 class="card-subtitle mb-2 text-muted">`).append(
                                entry.fields.date
                            )
                        ).append(
                            $(`<h6 class="card-subtitle mb-2 text-${entry.fields.is_finished ? "success" : "danger"}">`).append(
                                entry.fields.is_finished ? "Done" : "Not Done"
                            )
                        ).append(
                            $(`<p class="card-text">`).append(
                                entry.fields.description
                            )
                        )
                    ).append(
                        $(`<div class="card-footer">`).append(
                            $(`<div class="btn-group" role="group">`).append(
                                $(`<button class="btn btn-secondary" onclick="task_change_status(${entry.pk})">`).append(
                                    "Ubah Status"
                                )
                            ).append(
                                $(`<button class="btn btn-danger" onclick="task_delete(${entry.pk})">`).append(
                                    "Hapus Task"
                                )
                            )
                        )
                    ))
            })
        })
    }
```
Fungsi ini pertama-tama menghapus keseluruhan *cards* yang ada, kemudian mengambil data dari endpoint JSON yang sudah dibuat dengan `$.getJSON()`. Saat data sudah tersedia, fungsi yang didefinisikan di dalamnya akan dipanggil dan akan menyusun kembali *cards* sesuai dengan format yang sudah ada dan data yang tersedia.

### Implementasi AJAX POST untuk membuat task
Untuk mengimplementasikan pembuaan task baru dengan modal dan AJAX, pertama-tama sebuah modal yang mengandung suatu form dibuat. Setelah itu, *handler* dari event `submit` pada form tersebut diarahkan pada fungsi sebagai berikut:
```js
$(`#form-create-task`).submit(function (e) {
    e.preventDefault();

    /* url action dari form */
    var actionurl = e.currentTarget.action;

    $.ajax({
        url: actionurl,
        type: "POST",
        data: $(this).serialize(),
        success: function(response) {
            console.log("create-task POST OK!");
            $("#modal-create-task").modal('toggle');
            $("#form-create-task > div > .form-control").each(function (i) {
                $(this).val("");
            })
            load_tasks();
        },

        error: function(xhr, resp, text) {
            console.log("create-task POST ERROR")
            console.log(xhr, resp, text);
        }
    })

})
```
*Handler* ini mengirimkan data dengan request `POST` ke endpoint yang sudah dibuat sebelumnya. Data diambil dari form yang di-*serialize* ke dalam bentuk *url-encoded*. Jika request mereturn `200 OK`, maka *handler* pada success akan dipanggil, menutup modal, serta merefresh *cards*.  

### Implementasi AJAX DELETE untuk menghapus task
Untuk mengimplementasikan penghapusan task dengan request `DELETE`, pertama-tama didefinisikan fungsi *handler* sebagai berikut:
```js
function task_delete(pk) {
    $.ajax({
        url: `delete/${pk}/`,
        type: "DELETE",
        headers: {"X-CSRFToken": $('[name=csrfmiddlewaretoken]').val()},
        data: {
            csrfmiddlewaretoken: "{{csrf_token}}"
        },
        success: function(response) {
            console.log("DELETE OK!");
            load_tasks();
        },

        error: function(xhr, resp, text) {
            console.log("DELETE ERROR");
            console.log(xhr, resp, text);
        }
    })
}
```
Fungsi tersebut menerima satu parameter, yakni `pk` dari task yang hendak dihapus. Fungsi tersebut kemudian akan melakukan AJAX dengan request `DELETE` ke server, yang akan kemudian dihandle oleh view yang sesuai. Jika request mereturn `200 OK`, maka *handler* pada success akan dipanggil, untuk merefresh *cards*.  

Setelah membuat fungsi untuk melakukan penghapusan task, diperlukan cara untuk memanggil fungsi ini ketika tombol `Hapus Task` ditekan. Saya mengimplementasikan hal tersebut dengan menambahkan *handler* `onclick` ke button seperti berikut:
```html
<button ... onclick="task_delete(${entry.pk})">
```
`pk` untuk suatu entri akan dimasukkan oleh Javascript ke dalam parameter task_delete.

### Melakukan *deployment* ke Heroku
Setelah melakukan langkah-langkah di atas, saya membuat app pada Heroku, kemudian memasukkan nama app tersebut (```HEROKU_APP_NAME```) serta API key saya (```HEROKU_API_KEY```) ke dalam *actions secrets* pada repositori GitHub saya. Setelah itu, saya melakukan *commit* dan *push* sehingga perubahan pada repositori lokal akan tercermin pada GitHub, serta *actions* akan berjalan untuk mendeploy aplikasi ke Heroku.