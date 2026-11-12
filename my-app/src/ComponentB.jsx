import ComponentC from "./ComponentC";
import React, { useContext } from "react";
import { UserContext } from "./ComponentA.jsx";

function ComponentB() {
  const user = useContext(UserContext);
  return (
    <div className="box">
      <h1>ComponentB</h1>
      <h2>{`Hello from ${user}`}</h2>
      <ComponentC />
    </div>
  );
}

export default ComponentB;
