const calcArea = (radius) => {
  return 3.14 * radius ** 2;
};

const area = calcArea(5);
console.log(`The area of the circle is: ${area}`);

function calcArea2(radius) {
  return 3.14 * radius ** 2;
}

const area2 = calcArea2(7);
console.log(`The area of the circle is: ${area2}`);
