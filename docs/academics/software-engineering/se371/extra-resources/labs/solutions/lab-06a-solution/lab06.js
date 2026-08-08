var cities_set = new Set();
var employees_displayed = [];


for(let emp of data) {
  // create a second copy with all employees
  employees_displayed.push(emp);
  // create a set will all cities (sets only add unique cities -> no duplicates)
  cities_set.add(emp.address.city);
}

const createTRfromEmployee = (employee) => {
  let tr = document.createElement("tr");
  
  let td1 = document.createElement("td");
  td1.appendChild(document.createTextNode(employee.id));

  let td2 = document.createElement("td");
  td2.appendChild(document.createTextNode(`${employee.name} ${employee.lastname}`));

  let td3 = document.createElement("td");
  td3.appendChild(document.createTextNode(`${employee.address.nb}, 
      ${employee.address.street}, ${employee.address.city}`));

  tr.append(td1, td2, td3);
  
  return tr;
}

document.addEventListener("DOMContentLoaded", () => {
  // Create the table
  createTable(employees_displayed);

  // Refill the selector with cities
  const cities_selector = document.getElementById("cities_selector");
  cities_selector.innerHTML = "";
  let opt_all = document.createElement("option");
  opt_all.value = "all";
  opt_all.appendChild(document.createTextNode("all"));
  cities_selector.appendChild(opt_all);
  for(let c of cities_set){
    let opt = document.createElement("option");
    opt.value = c;
    opt.appendChild(document.createTextNode(c));
    cities_selector.appendChild(opt);
  }


})

const applycssClassNamesToElementsBySelector = (selectorString, ...classes) => {
  const elems = document.querySelectorAll(selectorString);
  for(let e of elems){
    for(let c of classes){
      e.classList.add(c);
    }
  }
}


const run = () => {
  // get the value of the selected city
  const city = document.getElementById("cities_selector").selectedOptions[0].value;

  // reconstruct the list of employees to display
  employees_displayed = [];
  for(let e of data){
    if((e.address.city === city) || (city === "all")){
      employees_displayed.push(e);
    }
  }

  // recreate the table
  createTable(employees_displayed);
};


const createTable = (listOfEmployeesToBeDisplayed) => {
  const table_body = document.getElementById("employee_table_body");
  table_body.innerHTML = "";

  for(let emp of listOfEmployeesToBeDisplayed) {
    table_body.appendChild(createTRfromEmployee(emp));
  }
  // Style the rows
  applycssClassNamesToElementsBySelector("tr:nth-child(even)", "grey");

  // Style the table
  applycssClassNamesToElementsBySelector("table, td", "border");
}

