export default class StickySideMenu {
  constructor() {
    this.stick();
    this.bindActions();
  }

  stick() {
    const isDesktop = window.innerWidth > 992;
    const headerHeight = document
      .querySelector(".header")
      .getBoundingClientRect().height;
    const main = document.querySelector(".main");
    const mainMarginTop = window
      .getComputedStyle(main, null)
      .getPropertyValue("margin-top")
      .replace("px", "");

    const sideMenuTopSPacing = headerHeight + +mainMarginTop;

    if (isDesktop) {
      $(".side-menu__content").sticky({ topSpacing: sideMenuTopSPacing });
    } else {
      $(".side-menu__content").unstick();
    }
  }

  bindActions() {
    window.addEventListener("resize", this.stick, false);
  }
}
