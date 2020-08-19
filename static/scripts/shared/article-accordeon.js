export default class ArticleAccordeon{
    constructor(){
        this.accordeonItems = document.querySelectorAll('.accordeon-item__title');
        this.accordeonItemsLinks = document.querySelectorAll('.accordeon-item__link__title');
        this.init();
    }

    delActiveClass(item){
        item.parentElement.classList.remove("accordeon-item__link--active");
    }

    addActiveClassToLink(e){
        this.accordeonItemsLinks.forEach(item=>{
            if(item != e.currentTarget){
                this.delActiveClass(item)
            }
        });

        e.currentTarget.parentElement.classList.toggle("accordeon-item__link--active")

    }

    addActiveClass(e){
        this.accordeonItems.forEach(item=>{
            if(item != e.currentTarget){
                item.parentElement.classList.remove("accordeon-item--active")
            }
        });

        this.accordeonItemsLinks.forEach(item=>{    
            this.delActiveClass(item)
        });

        e.currentTarget.parentElement.classList.toggle("accordeon-item--active")

    }

    init(){
        this.accordeonItems.forEach(item=>{
            item.addEventListener('click', (e)=>{this.addActiveClass(e)}
        )});

        this.accordeonItemsLinks.forEach(item=>{
            item.addEventListener('click', (e)=>{this.addActiveClassToLink(e)}
        )});

    }
}
