export default class StickyHeader {
  constructor() {
    this.stick();
    this.bindActions();
  }

  stick() {
    const isDesktop = window.innerWidth > 992;
    if (isDesktop) {
      $(".header--secondary").sticky({ topSpacing: 0, zIndex: 1 });
    } else {
      $(".header--secondary").unstick();
    }
  }

  bindActions() {
    window.addEventListener("resize", this.stick, false);
  }
}
