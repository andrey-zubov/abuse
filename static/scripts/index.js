import MobileMenu from "./shared/mobile-menu.js";

$(document).ready(async () => {
  window.refs = {
    mobileMenu: {
      init: () => new MobileMenu(),
      selectors: [".header"],
    },
  };

  Object.keys(window.refs).forEach((ref) => {
    if (
      window.refs[ref].hasOwnProperty("init") &&
      $(window.refs[ref].selectors.join(",")).length > 0
    ) {
      window.refs[ref].class = window.refs[ref].init();
    }
  });
});
