export default class Organizations{
    constructor(){
        this.organizations = document.querySelector('.organizations__content');
        this.init()
    }

    showOrganization(){
        const isCityData = this.organizations.getAttribute('data-active-city');
        const isSpecData = this.organizations.getAttribute('data-active-spec');

        $('.organization-item').slideUp();
        $('.organization-item').removeClass( "organization-item--passed" )

        if(!isCityData){
            let passedCity = Array.from(document.querySelectorAll(".organization-item"));

            passedCity.forEach(item => {
                let specifications = item.getAttribute('data-spec').split(', ');

                let specFind = specifications.find(item =>{
                    return item === isSpecData;
                })

                if(specFind){
                    item.classList.add('organization-item--passed')
                }
            })

            $(`.organization-item--passed`).slideDown();

        }else if(!isSpecData){
            $(`.organization-item[data-city="${isCityData}"]`).slideDown();
        }else{
            let passedCity = Array.from(document.querySelectorAll(`.organization-item[data-city="${isCityData}"]`));

            passedCity.forEach(item => {
                let specifications = item.getAttribute('data-spec').split(', ');

                let specFind = specifications.find(item =>{
                    return item === isSpecData;
                })

                if(specFind){
                    item.classList.add('organization-item--passed')
                }
            })

            $(`.organization-item--passed`).slideDown();
        }
    }

    init(){
        $('.organizations__select__specifications').select2({
            closeOnSelect: true,
            placeholder: 'Выберите деятельность',
        });

        $('.organizations__select__cities').select2({
            closeOnSelect: true,
            placeholder: 'Выберите город',
        });

        $('.organizations__select__cities').on('select2:close', (e) =>{
            const activeCity = e.params.originalSelect2Event.data?.id;
            this.organizations.dataset.activeCity = activeCity;
            this.showOrganization()
        });

        $('.organizations__select__specifications').on('select2:close', (e) =>{
            const activeSpec = e.params.originalSelect2Event.data?.id;
            this.organizations.dataset.activeSpec = activeSpec;
            this.showOrganization()
        });
    }
}