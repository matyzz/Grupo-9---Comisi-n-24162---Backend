const btnBorrar = document.querySelectorAll('.borrar')

if (btnBorrar) {
    const btnArray = Array.from(btnBorrar);
    btnArray.forEach((btn) => {
        btn.addEventListener('click', (e) => {
            if(!confirm('Estas seguro de querer eliminarlo?')){
                e.preventDefault();
            }
        })
    })
}