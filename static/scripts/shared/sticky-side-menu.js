export default class StickySideMenu {
  constructor() {
    this.stick();
    this.bindActions();
  }

  stick() {
    const isDesktop = window.innerWidth > 992;
    const headerHeight = document
      .querySelector(".header--secondary")
      .getBoundingClientRect().height;
    const main = document.querySelector(".main");
    const mainMarginTop = +window
      .getComputedStyle(main, null)
      .getPropertyValue("margin-top")
      .replace("px", "");

    const sideMenuTopSPacing = headerHeight + mainMarginTop;

    const lastSection = document.querySelector('section:last-of-type');

    const lastSectionName = lastSection.classList.value;

    const footerHeight = document.querySelector('.footer').getBoundingClientRect().height;

    let bottomSpacing = null;

    if(lastSectionName == 'organizations' ){
      bottomSpacing +=  lastSection.querySelector('.organizations__map').getBoundingClientRect().height
    }else if(lastSectionName == 'feedback'){
      bottomSpacing +=  lastSection.getBoundingClientRect().height
    }

    bottomSpacing += footerHeight

    if (isDesktop) {
      $(".side-menu__content").sticky({ topSpacing: sideMenuTopSPacing, bottomSpacing: bottomSpacing + 30 });
    } else {
      $(".side-menu__content").unstick();
    }
  }

  bindActions() {
    window.addEventListener("resize", this.stick, false);
  }
}
