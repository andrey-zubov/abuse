export default class MobileMenu{
    constructor(){
        this.headerButton = document.querySelector('.header__button');
        this.headerMenu = document.querySelector('.header__content');
        this.init();

    }

    showMenu(){
        this.headerButton.classList.toggle('header__button--active');
        this.headerMenu.classList.toggle('header__content--visible');
    }

    init(){
        if(!this.headerButton) return;

        this.headerButton.addEventListener('click', this.showMenu.bind(this));
        
    }
}