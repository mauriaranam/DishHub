// Opcion de confirmacion para eliminar
function check(){
    let opcion = confirm('Estas seguro que queres eliminar');
    if (opcion == false) {
        event.preventDefault();
    }
}


// Para ver el slidebar
function slide(){
    let slides = document.getElementById("slides");
    if(slides.classList.contains("hidden")){
        slides.classList.remove("hidden")
    } else {
        slides.classList.add("hidden")
    }
}