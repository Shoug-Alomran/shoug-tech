// Set of unique cities
const cities_set = new Set();

// fill set of cities
for (let d of data) {
  cities_set.add(d.address.city);
}

// Create and return a TD DOM element for some given text
const makeTDForText = (text) => {
  const td = document.createElement("td");
  td.appendChild(document.createTextNode(text));
  return td;
}

// Create and return a TR DOM element for some given employee object
const makeTRFromEmployee = (emp) => {
  const tr = document.createElement("tr");
  tr.appendChild(makeTDForText(emp.id));
  tr.appendChild(makeTDForText(`${emp.name} ${emp.lastname}`));
  tr.appendChild(makeTDForText(`${emp.address.nb} ${emp.address.street}, ${emp.address.city}`));
  return tr;
}

// Create and append to the HTML tbody a TR DOM element for every employee Object
// taking into account the city that is selected
const createTable = (option, employees) => {
  const tbody = document.querySelector("#employee_table_body");
  // remove old children
  while(tbody.firstChild) {
    tbody.removeChild(tbody.lastChild);
  }
  employees.forEach((emp) => {
    if(option === "All" || option === emp.address.city) {
      const tr = makeTRFromEmployee(emp);
      tbody.appendChild(tr);
    }

  })

  applycssClassForSelectedElements("grey", "tbody tr:nth-child(2n + 1)");
  applycssClassForSelectedElements("border", "td, th");
}

// Fills the cities selector with all cities in the given cities set
const fillSelector = (cities) => {
  const selector = document.querySelector("#cities_selector");
  selector.appendChild(makeOptionForText("All"));

  cities.forEach((city) => {
    selector.appendChild(makeOptionForText(city));
  });
}

// Create and return an OPTION DOM element for some given text
const makeOptionForText = (text) => {
  const option = document.createElement("option");
  if(text) {
    option.appendChild(document.createTextNode(text));
    option.value = text;
  }
  return option;
}

// Applies the given css class to every element selected by the given css selector
const applycssClassForSelectedElements = (css_class, selector) => {
  const nodes = document.querySelectorAll(selector);
  nodes.forEach( (node) => {
    node.classList.add(css_class);
  });
}

const sortData = (criteria) => {
  if(criteria === "none") {
    return data;
  } else if(criteria === "by_id") {
    return data.toSorted((empA, empB) => {
      if (empA.id > empB.id) { 
        return 1;
      } else if(empA.id - empB.id) {
        return -1;
      } else {
        return 0;
      }
    });
  } else if(criteria === "by_name") {
    return data.toSorted((empA, empB) => {
      if (empA.name > empB.name) { 
        return 1;
      } else if(empA.name < empB.name) {
        return -1;
      } else {
        return 0;
      }
    });
  } else if(criteria === "by_city") {
    return data.toSorted((empA, empB) => {
      if (empA.address.city > empB.address.city) { 
        return 1;
      } else if(empA.address.city < empB.address.city) {
        return -1;
      } else {
        return 0;
      }
    });
  }
};

// When the page is loaded, create the table, fill the selecotr then declare event handlers
// for the selectors
document.addEventListener("DOMContentLoaded", () => {
  createTable("All", data);

  fillSelector(cities_set);

  const city_selector = document.querySelector("#cities_selector");
  city_selector.addEventListener("change", () => {
    createTable(city_selector.value, data);
  });

  const sort_selector = document.querySelector("#sortby_selector");
  sort_selector.addEventListener("change", () => {
    const sorted = sortData(sort_selector.value);
    createTable(city_selector.value, sorted);
  });

});

