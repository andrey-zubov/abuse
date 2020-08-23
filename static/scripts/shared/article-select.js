export default class SrticleSelect{
    constructor(){
        this.init();

    }

    showCity(e){
        const activeCity = e.params.originalSelect2Event.data.id;

        Array.from(document.querySelectorAll('.vacancy')).forEach(item=>{
            item.style.display = "none";
        })

        document.querySelector(`[data-city="${activeCity}"]`).style.display = "block";
    }

    init(){
        $('.select').select2({
            closeOnSelect: true,
            width: '190px',
            placeholder: 'Выберите город',
        });

        $('.select').on('select2:close', (e) =>{
            this.showCity(e);
          });
    }
}