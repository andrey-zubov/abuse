export default class StickyHeader {
  constructor() {
    this.stick();
    this.bindActions();
  }

  stick() {
    const isDesktop = window.innerWidth > 992;
    if (isDesktop) {
      $(".header__content").sticky({ topSpacing: 0, zIndex: 1 });
    } else {
      $(".header__content").unstick();
    }
  }

  bindActions() {
    window.addEventListener("resize", this.stick, false);
  }
}
