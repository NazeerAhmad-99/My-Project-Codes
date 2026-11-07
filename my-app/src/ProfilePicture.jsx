import imageUrl from "./assets/imresizer-resize-MA.jpg";

function ProfilePicture() {
  const handleClick = (e) => (e.target.style.display = "none");

  return <img onClick={(e) => handleClick(e)} src={imageUrl} alt="Profile" />;
}
export default ProfilePicture;
