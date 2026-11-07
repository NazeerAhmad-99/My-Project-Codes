import picture from "./imresizer-resize-MA.jpg";

function Card() {
  return (
    <div className="card">
      <img className="card-image" src={picture} alt="Profile Picture"></img>
      <h2 className="card-title"> Nazeer Ahmad</h2>
      <p className="card-description">
        This is the placeholder for the paragraph.
      </p>
    </div>
  );
}

export default Card;
