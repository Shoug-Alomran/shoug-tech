
const paintings = [
  {title: "Girl with a pearl earring", artist: "Vermeer", value: 10},
  {title: "Artists Holding a Thristle", artist: "Durer", value: 7},
  {title: "Wheat field with Crows", artist: "Van Gogh", value: 16},
  {title: "Burial at Ornans", artist: "Courbet", value: 18},
  {title: "Wheat field with Crows", artist: "Van Gogh", value: 9}
];


// FOR EACH
paintings.forEach( (p) => console.log(p) );


//  find 
console.log("Van Gogh only paintings:");
const vg = paintings.filter( (p) => p.artist == 'Van Gogh');
vg.forEach( (p) => console.log(p) );

// FOR filter
console.log("Van Gogh only paintings:");
const vg_fil = paintings.find( (p) => p.artist == 'Van Gogh');
console.log(vg_fil);

// map
console.log("All paintings in uppercase:")
const mapped = paintings.map( p => `${p.title.toUpperCase()} : ${p.artist.toUpperCase()}`);
console.log(mapped);



// // Reduce
console.log("Total value of paintings is:");
let initial = 0;
const total = paintings.reduce( (prev, p) => prev + p.value, initial);
console.log( total );

// sort by value
console.log("All paintings sorted by value:")
const compareFn = (a, b) => a.value - b.value;
const sorted = paintings.sort(compareFn);
sorted.forEach(e =>  console.log(e) );



// sort by string
console.log("All paintings sorted by artist:")
function compareFnstr (a, b)
{  if (a.artist < b.artist) return -1;
  else if (a.artist > b.artist) return 1;
  else return 0;
}
const sorted_str = paintings.sort(compareFnstr);
console.log(sorted_str)

