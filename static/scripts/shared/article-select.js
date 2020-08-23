export default class SrticleSelect{
    constructor(){
        this.init();

    }

    showCity(e){
        const activeCity = e.params.originalSelect2Event.data.id;

        Array.from(document.querySelectorAll('.vacancy')).forEach(item=>{
            item.style.display = "none";
        })

        Array.from(document.querySelectorAll(`[data-city="${activeCity}"]`)).forEach(item=>{
            item.style.display = "block";
        })
    }

    init(){
        $('.article__select-item').select2({
            closeOnSelect: true,
            placeholder: 'Выберите город',
        });

        $('.article__select-item').on('select2:close', (e) =>{
            this.showCity(e);
          });
    }
}