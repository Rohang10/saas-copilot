import { useState } from "react";
import LoginPage from "./pages/LoginPage";
import SignupPage from "./pages/SignupPage";
import ChatPage from "./pages/ChatPage";
import { getToken, logout } from "./services/api";

export default function App() {
  const [loggedIn, setLoggedIn] = useState(() => Boolean(getToken()));
  const [showSignUp, setShowSignUp] = useState(false);

  //  Logout
  const handleLogout = () => {
    logout();
    setLoggedIn(false);
  };


  // 1️⃣ User is logged in → Chat
  if (loggedIn) {
    return <ChatPage onLogout={handleLogout} />;
  }

  // 2️⃣ Signup page
  if (showSignUp) {
    return (
      <SignupPage
        onSignupSuccess={() => {
          setLoggedIn(true);
          setShowSignUp(false);
        }}
        onBackToLogin={() => setShowSignUp(false)}
      />
    );
  }

  // 3️⃣ Login page (default)
  return (
    <LoginPage
      onLogin={() => setLoggedIn(true)}      // login → chat
      onShowSignup={() => setShowSignUp(true)} // login → signup
    />
  );
}
