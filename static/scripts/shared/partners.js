export default class Partners{
    constructor(){
        this.init()
    }

    setFirstActiveForm(selectForm){
        selectForm[0].classList.add('link--active');
        const form = document.querySelector(`.partners .partners__form[data-form='${+selectForm[0].getAttribute('data-form')}']`);
        form.style.display = "block";
        form.classList.add("partners__form--active");
    }

    init(){
        $('.form-item__select--type').select2({
            closeOnSelect: true,
            placeholder: 'Тип организации',
        });
        
        $('.form-item__select--form').select2({
            closeOnSelect: true,
            placeholder: 'Форма собственности организации',
        });

        $('.form-item__select--work').select2({
            closeOnSelect: true,
            placeholder: 'Тип занятости',
        });

        $('.form-item__select--organization').select2({
            closeOnSelect: true,
            placeholder: 'Деятельность организации',
        }); 

        $(".form-item__phone input").mask("+375 (99) 999 - 99 - 99", {
            completed: function(){console.log(this.val()) }
        });


        const selectForm = Array.from(document.querySelectorAll('.partners .main-menu__navigation .link'));
        const forms = Array.from(document.querySelectorAll('.partners .partners__form'));

        this.setFirstActiveForm(selectForm);

        selectForm.forEach(link=>{
            link.addEventListener('click', (e)=>{
                let timer;
                selectForm.forEach(i=>{
                    i.classList.remove('link--active')
                })

                e.currentTarget.classList.add('link--active')
                const idActiveForm = e.currentTarget.getAttribute('data-form');
                
                forms.forEach((f)=>{
                    f.classList.remove("partners__form--active")
                    f.style.display = "none"
                })

                const activeForm = document.querySelector(`.partners .partners__form[data-form='${+idActiveForm}']`);
                activeForm.style.display = "block";
                
                timer = setTimeout(()=>{
                    activeForm.classList.add("partners__form--active");
                }, 300)
            })
        })
    }
}