import Login from "../components/Login";

export default function LoginPage({ onLogin, onShowSignup }) {
  return (
    <div className="min-h-screen flex flex-col items-center justify-center gap-4 bg-gray-100">
      <Login onSuccess={onLogin} />

      <button
        onClick={onShowSignup}
        className="text-[#111] text-sm hover:underline"
      >
        Don&apos;t have an account? Sign up
      </button>
    </div>
  );
}
