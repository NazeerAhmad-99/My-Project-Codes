import ComponentD from "./ComponentD";
import React, { useContext } from "react";
import { UserContext } from "./ComponentA.jsx";

function ComponentC() {
  const user = useContext(UserContext);
  return (
    <div className="box">
      <h1>ComponentC</h1>
      <h2>{`Hello from ${user}`}</h2>
      <ComponentD />
    </div>
  );
}

export default ComponentC;
