function Button() {
  const handleClick = (e) =>
    (e.target.textContent = "Ouch!! You clicked me !!");

  return (
    <button className="btn" onClick={(e) => handleClick(e)}>
      Click Me
    </button>
  );
}
export default Button;
