      document.onDOMContentLoaded = fw("document");

      window.onload = fw("window");

      function fw(sender) {
        alert(`The sender is ${sender}.`);
      }

      document.addEventListener("DOMContentLoaded", function (e) {
        const menu_li_items = document.querySelectorAll("#menu li");
        for (let item of menu_li_items) {
          item.addEventListener("click", function (e) {
            item.classList.toggle("shadow");
            alert(
              e.target + "; " + e.type + " ; " + e.clientX + ":" + e.clientY
            );
          });
        }
        const heading = document.querySelector("h2");
        heading.addEventListener("click", function (e) {
          heading.classList.toggle("shadow");
          alert(e.target + "; " + e.type + " ; " + e.clientX + ":" + e.clientY);
        });
      });