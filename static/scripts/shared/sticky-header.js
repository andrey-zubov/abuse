export default class StickyHeader {
  constructor() {
    this.init();
  }

  stick() {
    const isDesktop = window.innerWidth > 992;
    if (isDesktop) {
      $(".header__content").sticky({ topSpacing: 0, zIndex: 1 });
    } else {
      $(".header__content").unstick();
    }
  }

  init() {
    window.addEventListener("resize", this.stick, false);
  }
}
