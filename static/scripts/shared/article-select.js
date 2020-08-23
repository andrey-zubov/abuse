export default class ArticleSelect{
    constructor(){
        this.init();

    }

    showCity(e){
        const activeCity = e.params.originalSelect2Event.data.id;

        $('.vacancy').slideUp();

        $(`[data-city="${activeCity}"]`).slideDown();
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