export default class StickySideMenu {
  constructor() {
    this.init();
  }

  init() {
    const headerHeight = document
      .querySelector(".header")
      .getBoundingClientRect().height;
    const main = document.querySelector(".main");
    const mainMarginTop = window
      .getComputedStyle(main, null)
      .getPropertyValue("margin-top")
      .replace("px", "");
    console.log(mainMarginTop);

    const sideMenuTopSPacing = headerHeight + +mainMarginTop;

    $(".side-menu__content").sticky({ topSpacing: sideMenuTopSPacing });
  }
}
