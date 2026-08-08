// defines a function using an anonymous function expression
const calculateSubtotal = function (price,quantity) {
	return price * quantity;
};

// invokes the function
let result = calculateSubtotal(10,2);

console.log(calculateSubtotal);

// define another function
const warn = function(msg) {alert(msg); };

// now invoke that function
warn("This doesn't return anything");
