// alert, confirm and prompt
let answer = prompt("Please enter your name:");

        
let bool=confirm('Please confirm that your name is ' + answer);
if (bool)
    {
        alert('your name is ' + answer);
        console.log('your name is ' + answer);
        document.write(`<h1> Hello ${answer} </h1>`)
    }
else 
    { alert('We dont know your name');}

     
navigator.geolocation.getCurrentPosition( (data) => { console.log(data); } );

