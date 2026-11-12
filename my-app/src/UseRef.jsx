import { useRef } from "react";

function UseRefExample() {
  const ref = useRef(0);

  function handleClick() {
    ref.current = ref.current + 1;
    console.log("Current value of ref:", ref.current);
  }

  return (
    <>
      <h1>UseRef Example</h1>
      <button onClick={handleClick}>Increment</button>
    </>
  );
}

export default UseRefExample;
