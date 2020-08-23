export default class ArticleCalendar{
    constructor(){
        this.data= null;
        this.init();

    }

    showCity(e){
        const activeCity = e.params.originalSelect2Event.data?.id;

        document.querySelector('.article-calendar .activities').dataset.activeCity = activeCity;

        const allActivities = $('.activities .vacancy').slideUp();

        const activeData = document.querySelector('.article-calendar .activities[data-active-day]');

        let activities = null;

        const empty = document.querySelector('.activities .vacancy--empty')

        const emptyState = '<div class="vacancy--empty"><p class="headline-3">НА ВЫБРАННУЮ ДАТУ НЕТ МЕРОПРИЯТИЙ</p></div>'

        if(activeData){
            const calendarValue = document.querySelector('.calendar').value;
            if(!calendarValue ){
                activities =  $(`.activities .vacancy[data-city="${activeCity}"]`).slideDown();
            }else{
                activities =  $(`.activities .vacancy[data-city="${activeCity}"][data-active-day="${calendarValue}"]`).slideDown();
            }
        }else{   
            activities = $(`.activities .vacancy[data-city="${activeCity}"]`).slideDown();
        }

        if(activities.length === 0){
            if(!empty) document.querySelector('.activities').insertAdjacentHTML('afterbegin', emptyState)
        }else{
            empty?.remove();
        }
    }

    init(){
        $('.select__activity').select2({
            closeOnSelect: true,
            placeholder: 'Выберите город',
        });

        $('.select__activity').on('select2:close', (e) =>{
            this.showCity(e);
          });

        const options = {
            autoClose: true,
            offset: 7,
            dateFormat: "dd-mm-yyyy",
            onHide: function(dp, animationCompleted){
                if (animationCompleted) {
                    const calendarValue = document.querySelector('.calendar').value;

                    document.querySelector('.article-calendar .activities').dataset.activeDay = calendarValue;

                    const allActivities = $('.activities .vacancy').slideUp();

                    const activeCity = document.querySelector('.article-calendar .activities[data-active-city]');

                    const empty = document.querySelector('.activities .vacancy--empty')

                    let activities = null;

                    const emptyState = '<div class="vacancy--empty"><p class="headline-3">НА ВЫБРАННУЮ ДАТУ НЕТ МЕРОПРИЯТИЙ</p></div>'

                    if(activeCity){
                        const city = activeCity.getAttribute('data-active-city');
                        if(!calendarValue){
                            activities =  $(`.activities .vacancy[data-city="${city}"]`).slideDown();
                        }else{
                            activities =  $(`.activities .vacancy[data-city="${city}"][data-active-day="${calendarValue}"]`).slideDown();
                        }
                    }else{
                        if(!calendarValue){
                            $('.activities .vacancy').slideDown();
                        }else{
                        activities =  $(`.activities .vacancy[data-active-day="${calendarValue}"]`).slideDown();
                        }   
                    }
                    if(activities?.length === 0){
                        if(!empty) document.querySelector('.activities').insertAdjacentHTML('afterbegin', emptyState)
                    }else{
                        empty?.remove();
                    }

                }
            }
        }


       $('.calendar').datepicker(options);
    }
}