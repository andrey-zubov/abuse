export default class StickyHeader {
  constructor() {
    this.init();
  }

  init() {
    $(".header__content").sticky({ topSpacing: 0, zIndex: 1 });
  }
}
