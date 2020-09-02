import "./vendor/jquery.js";
import "./vendor/jquery.sticky.js";
import "./vendor/select2.js";
import "./vendor/datepicker.js";

import MobileMenu from "./shared/mobile-menu.js";
import StickyHeader from "./shared/sticky-header.js";
import StickySideMenu from "./shared/sticky-side-menu.js";
import ArticleAccordeon from "./shared/article-accordeon.js";
import ArticleSelect from "./shared/article-select.js";
import ArticleCalendar from "./shared/article-calendar.js";
import Organizations from "./shared/organizations.js";

$(document).ready(async () => {
  window.refs = {
    mobileMenu: {
      init: () => new MobileMenu(),
      selectors: [".header--main"],
    },
    stickyHeader: {
      init: () => new StickyHeader(),
      selectors: [".header--secondary"],
    },
    stickySideMenu: {
      init: () => new StickySideMenu(),
      selectors: [".side-menu"],
    },
    articleAccordeon: {
      init: () => new ArticleAccordeon(),
      selectors: [".article-accordeon"],
    },
    articleSelect: {
      init: () => new ArticleSelect(),
      selectors: [".article-select"],
    },
    articleCalendar: {
      init: () => new ArticleCalendar(),
      selectors: [".article-calendar"],
    },
    organizations: {
      init: () => new Organizations(),
      selectors: [".organizations"],
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
