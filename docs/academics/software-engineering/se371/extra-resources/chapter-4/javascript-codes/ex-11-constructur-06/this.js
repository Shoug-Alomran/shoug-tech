const employee = {
  id: "0023",
  name: "asma",
  address: {
    nb: 12,
    street: "faycaliyya street",
    city: "riyadh",
    country: "KSA",
    output: function() { return employee.id + " "+ this.nb + " " + this.street + ", " 
                        + this.city + ", " + this.country; },
  },

};

console.log( employee.address.output() );