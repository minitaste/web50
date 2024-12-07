// function hello() {
//   const heading = document.querySelector("h1");

//   if (heading.innerHTML === "Hiii!") {
//     heading.innerHTML = "Goodbye!";
//   } else {
//     heading.innerHTML = "Hiii";
//   }
//   alert("Hello, world!");
// }

if (!localStorage.getItem('counter')) {
    localStorage.setItem('counter', 0);

}

function count() {
    let counter = localStorage.getItem('counter')
    counter++;
    document.querySelector("h1").innerHTML = counter;
    localStorage.setItem('counter', counter);
}

document.addEventListener("DOMContentLoaded", function () {
    document.querySelector("h1").innerHTML = localStorage.getItem('counter');
    document.querySelector("button").onclick = count;


    // setInterval(count , 100);
});

// document.addEventListener('DOMContentLoaded', function () {
//     document.querySelector('form').onsubmit = function () {
//         const name = document.querySelector('#name').value;
//         alert(`Hello ${name}!`)
//     };
// });