document.addEventListener("DOMContentLoaded", 
    ()=>{
        let redirect;
        let timer;
        let button = document.querySelector('.main-button');

        $(".select").select2({
            closeOnSelect: true,
            placeholder: "Adminka",
            minimumResultsForSearch: -1,
        });

        $(".select").on("select2:close", (e) => {
                redirect = e.params.originalSelect2Event?.data.id;
            }
        )

        button.addEventListener('click', (e) => {
            clearTimeout(timer);
            e.preventDefault();
            e.stopPropagation();

            if(redirect){
                window.location.replace(redirect);
            }else{
                button.classList.add('main-button--red')
                timer = setTimeout(()=>{
                    button.classList.remove('main-button--red')
                }, 1000)
            }
        })
    }
);