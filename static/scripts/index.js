import "./vendor/jquery.js";
import "./vendor/jquery.sticky.js";

import MobileMenu from "./shared/mobile-menu.js";
import StickyHeader from "./shared/sticky-header.js";
import StickySideMenu from "./shared/sticky-side-menu.js";

$(document).ready(async () => {
  window.refs = {
    mobileMenu: {
      init: () => new MobileMenu(),
      selectors: [".header"],
    },
    stickyHeader: {
      init: () => new StickyHeader(),
      selectors: [".header"],
    },
    stickySideMenu: {
      init: () => new StickySideMenu(),
      selectors: [".side-menu"],
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
