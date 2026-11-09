import React, { useState } from "react";

function MyComponent() {
  const [name, setName] = useState("Guest");

  const [age, setAge] = useState(0);

  const [isEmployed, setIsEmployed] = useState(false);

  const incrementAge = () => {
    setAge(age + 1);
  };

  const UpdateName = () => {
    setName("Nazeer");
  };
  const UpdateEmploymentStatus = () => {
    setIsEmployed(!isEmployed);
  };

  return (
    <div>
      <p>Name: {name}</p>
      <button onClick={UpdateName}>Set Name</button>

      <p>Age: {age}</p>
      <button onClick={incrementAge}>Set Age</button>

      <p>Employed: {isEmployed ? "Yes" : "No"}</p>
      <button onClick={UpdateEmploymentStatus}>Employment Status</button>
    </div>
  );
}

export default MyComponent;
