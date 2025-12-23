import Signup from "../components/Signup";

export default function SignUpPage({ onSignupSuccess, onBackToLogin }) {
  return (
    <div className="min-h-screen flex flex-col items-center justify-center gap-4 bg-gray-100">
      
      {/* Signup form */}
      <Signup onSuccess={onSignupSuccess} />

      {/* Back to login */}
      <button
        onClick={onBackToLogin}
        className="text-[#111] text-sm hover:underline"
      >
        Already have an account? Login
      </button>

    </div>
  );
}
