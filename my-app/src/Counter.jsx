import React, { useState } from "react";

function Counter() {
  const [count, setCount] = useState(0);

  const increment = () => {
    setCount(count + 1);
  };

  const decrement = () => {
    setCount(count - 1);
  };

  const reset = () => {
    setCount(0);
  };

  return (
    <div className="counterContainer">
      <p className="countDisplay"> {count} </p>
      <button className="counterButton" onClick={increment}>
        Increment
      </button>

      <button className="counterButton" onClick={reset}>
        Reset
      </button>

      <button className="counterButton" onClick={decrement}>
        Decrement
      </button>
    </div>
  );
}

export default Counter;
