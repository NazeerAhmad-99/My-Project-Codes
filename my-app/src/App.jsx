import Card from "./Card.jsx";
import Button from "./Button.jsx";
import Student from "./Student.jsx";
import UserGreeting from "./UserGreeting.jsx";
import List from "./List.jsx";
import ProfilePicture from "./ProfilePicture.jsx";
import MyComponent from "./MyComponenent.jsx";
import Counter from "./Counter.jsx";

function App() {
  return (
    <>
      <Button />
      <Counter />
      <MyComponent />
      <UserGreeting isLoggedIn={true} username="Nazeer" />
      <Student name="Mallika" age={22} isStudent={false} />
      <Student name="Nazeer" age={23} isStudent={true} />
      <Student name="Sandy" age={30} isStudent={false} />
      <List />
      <ProfilePicture />
      <Student name="Supa" age={28} isStudent={true} />
      <Card />
    </>
  );
}

export default App;
