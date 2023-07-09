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

// Para ver opciones de colaborador
function colab(){
    let colabs = document.getElementById("colabs");
    if(colabs.classList.contains("hidden")){
        colabs.classList.remove("hidden")
    } else {
        colabs.classList.add("hidden")
    }
}

// para el boton de agregar nuevo ingreso
function add_colab(){
    var addColab = document.getElementById("addColab");
    var closeColab = document.getElementById("closeColab");

    if(addColab.classList.contains("hidden")){
        addColab.classList.remove("hidden")
        closeColab.classList.add("hidden")
    } else {
        addColab.classList.add("hidden")
        closeColab.classList.remove("hidden")
    }
}