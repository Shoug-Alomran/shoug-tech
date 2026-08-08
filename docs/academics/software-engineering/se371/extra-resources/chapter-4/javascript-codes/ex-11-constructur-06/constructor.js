
let employee = function (name, lastname) {
  this.name = name,
  this.lastname = lastname,
  this.myfunc = function () {
    return this.name + " " + this.lastname; }
};

let s = new employee("Asma", "Sattar");
console.log(s.myfunc());
