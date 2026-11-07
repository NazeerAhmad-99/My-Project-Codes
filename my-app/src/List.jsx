function List() {
  const fruits = [
    { name: "Apple", calories: 95 },
    { name: "Banana", calories: 105 },
    { name: "Cherry", calories: 50 },
    { name: "Date", calories: 282 },
    { name: "Elderberry", calories: 100 },
  ];

  fruits.sort((a, b) => a.name.localeCompare(b.name)); //sort the fruits array alphabetically by name

  const listItems = fruits.map((fruit) => (
    <li className="list-item" key={fruit.name}>
      {fruit.name}: {fruit.calories} calories
    </li>
  ));
  return <ol>{listItems}</ol>;
}

export default List;
