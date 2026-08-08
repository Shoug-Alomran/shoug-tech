function caltotal(price, quality)
{ {
    let subtotal=price * quality;
    return subtotal+calculatetax(subtotal);
    
}

function calculatetax(subtotal)
{
let taxrate=0.05;
let tax= subtotal*taxrate;
return tax;    
};
}

p=caltotal(3, 10);
console.log(p);

// function caltotal(price, quality)
// { {
//     let subtotal=price * quality;
//     return subtotal+calculatetax(subtotal);
    
// }

// const calculatetax=function (subtotal)
// {
// let taxrate=0.05;
// let tax= subtotal*taxrate;
// return tax;    
// };
// }
// p=caltotal(3, 10);
// console.log(p);