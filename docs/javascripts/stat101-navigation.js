(function () {
  'use strict';

  function normalizeCourseNavigation() {
    var sectionList = document.querySelector('.academic-sidebar .section-children');
    if (!sectionList) return;

    var courseMatch = window.location.pathname.match(/^\/academics\/other-courses\/([^/]+)\//i);
    if (!courseMatch) return;
    var base = '/academics/other-courses/' + courseMatch[1].toLowerCase() + '/';
    var order = [
      base,
      base + 'slide-breakdowns/',
      base + 'slides/',
      base + 'extra-resources/',
      base + 'quizzes/',
      base + 'exams/'
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

    if (base === '/academics/other-courses/math221/') {
      nestedLists.forEach(function (list) {
        var items = Array.from(list.children).filter(function (node) {
          return node.matches('li.tree-viewer');
        });
        items.sort(function (left, right) {
          var leftText = left.textContent.trim();
          var rightText = right.textContent.trim();
          var leftNumbers = (leftText.match(/\d+/g) || ['999']).map(Number);
          var rightNumbers = (rightText.match(/\d+/g) || ['999']).map(Number);
          for (var index = 0; index < Math.max(leftNumbers.length, rightNumbers.length); index += 1) {
            var difference = (leftNumbers[index] == null ? -1 : leftNumbers[index]) - (rightNumbers[index] == null ? -1 : rightNumbers[index]);
            if (difference) return difference;
          }
          return leftText.localeCompare(rightText, undefined, { numeric: true });
        });
        items.forEach(function (item) { list.appendChild(item); });
      });
    }

    if (base !== '/academics/other-courses/com201/') return;
    var studyList = nestedByRoute[base + 'extra-resources/'];
    if (!studyList) return;

    var worksheetSlugs = [
      '04-2-sc-chapter-2-perception-self-and-communication',
      '05-3-sc-chapter3-language-and-meaning',
      '06-4-sc-chapter-4-nonverbal-communication',
      '07-5-sc-chapter-5-listening-critical-thinking',
      '08-midterm-exam-full-slides'
    ];
    var worksheetItems = Array.from(studyList.children).filter(function (item) {
      var link = item.querySelector(':scope > a.tree-file');
      if (!link) return false;
      var slug = worksheetSlugs.find(function (candidate) {
        return link.getAttribute('href').indexOf(candidate) !== -1;
      });
      if (!slug) return false;
      link.setAttribute('href', base + 'extra-resources/worksheets/' + slug + '/');
      return true;
    });
    if (!worksheetItems.length) return;

    var inWorksheets = window.location.pathname.indexOf(base + 'extra-resources/worksheets/') === 0;
    var folderItem = document.createElement('li');
    folderItem.className = 'tree-item tree-viewer' + (inWorksheets ? ' file-active' : '');
    folderItem.innerHTML = '<a class="tree-file" href="' + base + 'extra-resources/worksheets/">' +
      (inWorksheets ? '<span class="status-dot"></span>' : '') + 'WORKSHEETS/</a>';
    studyList.insertBefore(folderItem, worksheetItems[0]);

    var worksheetList = document.createElement('ul');
    worksheetList.className = 'tree-children item-children folder-children' + (inWorksheets ? ' is-open' : '');
    worksheetItems.forEach(function (item) {
      worksheetList.appendChild(item);
    });
    studyList.insertBefore(worksheetList, folderItem.nextSibling);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', normalizeCourseNavigation);
  } else {
    normalizeCourseNavigation();
  }
})();
