import React, { useState } from "react";

function OnChangeComponent() {
  const [name, setName] = useState("");
  const [quantity, setQuantity] = useState(1);
  const [comment, setComment] = useState("");
  const [payment, setPayment] = useState("select");
  const [shipping, setShipping] = useState("");

  function handleShippingChange(event) {
    setShipping(event.target.value);
  }

  function handlePaymentChange(event) {
    setPayment(event.target.value);
  }

  function handleCommentChange(event) {
    setComment(event.target.value);
  }

  function handleQuantityChange(event) {
    setQuantity(event.target.value);
  }

  function handleNameChange(event) {
    setName(event.target.value);
  }

  return (
    <div className="on-change-component">
      <input value={name} onChange={handleNameChange} />
      <p>Name: {name}</p>
      <input value={quantity} onChange={handleQuantityChange} type="number" />
      <p>Quantity: {quantity}</p>
      <textarea
        value={comment}
        onChange={handleCommentChange}
        placeholder="Enter your comment here..."
      />
      <p>Comment: {comment}</p>
      <select value={payment} onChange={handlePaymentChange}>
        <option value="Select">Select Payment Method</option>
        <option value="Credit">Credit Card</option>
        <option value="Debit">Debit Card</option>
        <option value="PayPal">PayPal</option>
      </select>
      <p>Payment Method: {payment}</p>
      <label>
        <input
          type="radio"
          value="Pickup"
          checked={shipping === "Pickup"}
          onChange={handleShippingChange}
        />
        Pickup
      </label>
      <label>
        <input
          type="radio"
          value="Delivery"
          checked={shipping === "Delivery"}
          onChange={handleShippingChange}
        />
        Delivery
      </label>
      <p>Shipping Method: {shipping}</p>
    </div>
  );
}
export default OnChangeComponent;
