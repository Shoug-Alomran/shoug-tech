(function () {
  'use strict';

  function normalizeStat101Navigation() {
    var sectionList = document.querySelector('.academic-sidebar .section-children');
    if (!sectionList) return;

    var order = [
      '/academics/other-courses/stat101/',
      '/academics/other-courses/stat101/slide-breakdowns/',
      '/academics/other-courses/stat101/slides/',
      '/academics/other-courses/stat101/extra-resources/',
      '/academics/other-courses/stat101/quizzes/'
    ];

    var sectionItems = Array.from(sectionList.children).filter(function (node) {
      return node.matches('li.tree-section');
    });
    var nestedLists = Array.from(sectionList.children).filter(function (node) {
      return node.matches('ul.item-children');
    });
    var nestedByRoute = {};

    nestedLists.forEach(function (list) {
      var previous = list.previousElementSibling;
      var link = previous && previous.querySelector(':scope > a.tree-file');
      if (link) nestedByRoute[link.getAttribute('href')] = list;
    });

    order.forEach(function (route) {
      var item = sectionItems.find(function (candidate) {
        var link = candidate.querySelector(':scope > a.tree-file');
        return link && link.getAttribute('href') === route;
      });
      if (!item) return;
      sectionList.appendChild(item);
      if (nestedByRoute[route]) sectionList.appendChild(nestedByRoute[route]);
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', normalizeStat101Navigation);
  } else {
    normalizeStat101Navigation();
  }
})();
