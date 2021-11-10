
function image_type_checks(event){
    var fl = $(event).val();
    var ext = fl.split('.').pop().toLowerCase();
    var size = event.files[0].size;
    if ($.inArray(ext, ['png', 'jpg', 'jpeg', 'pdf']) == 1) {
        let img = new Image()
        img.src = window.URL.createObjectURL(event.files[0])
        img.onload = () => {

        }
    }
}

