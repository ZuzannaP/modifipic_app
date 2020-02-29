// $(function() {
// function addBook(book) {
// console.log('Dodaje ksiazke');
// $.ajax({
//   method: 'POST',
//   url: 'http://localhost:8000/book/',
//   data: book,
//   dataType: "JSON",
// }).done(function(response) {
//   getBooks();
// }).fail(function(error) {
//   console.log(error);
// })
// }
// })

$('#id_ajax_upload_form').submit(function (e) {
    e.preventDefault();
    $form = $(this);
    var formData = new FormData(this);
    formData.append("category",0);
    $.ajax({
        url: 'http://localhost:8000/api/raw_images/',
        type: 'POST',
        data: formData,
        contentType: false,
        processData: false,
        cache: false
    }).done(
        function (response) {
            $('.error').remove();
            console.log(response);
            if (response.error) {
                $.each(response.errors, function (name, error) {
                    error = '<small class="text-muted error">' + error + '</small>';
                    $form.find('[name=' + name + ']').after(error);
                })
            } else {
                alert(response.message);
                window.location = ""
            }
    });
    });



