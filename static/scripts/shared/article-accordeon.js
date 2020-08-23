export default class ArticleAccordeon{
    constructor(){
        this.init();
    }

  

    init(){

  
        $('.accordeon-item__title').click(function(){
          $(this).parent().toggleClass('accordeon-item--active').siblings().removeClass('accordeon-item--active');
          $('.accordeon-item__links').slideUp(500);
          $('.accordeon-item__links').children().children('.accordeon-item__link__content').slideUp(500);
          
          if(!$(this).next().is(":visible")) {
                $(this).next().slideDown(500);
              }
        });

  
        $('.accordeon-item__link__title').click(function(){
          $('.accordeon-item__link__content').slideUp(500);
          
          if(!$(this).next().is(":visible")) {
                  $(this).next().slideDown(500);
              }
        });

    }
}
