import { Link } from "react-router-dom";
import { useAuth } from "../context/AuthContext.jsx";

export default function Landing() {
  const { user } = useAuth();

  return (
    <div className="max-w-3xl mx-auto px-4 py-20 text-center">
      <h1 className="text-4xl font-bold tracking-tight mb-4">
        Take control of your debt, <span className="text-brand-600">with AI on your side</span>
      </h1>
      <p className="text-gray-500 mb-8">
        Track your loans, understand your financial health, and get AI-generated settlement
        offers and negotiation letters — all in one place.
      </p>
      <div className="flex justify-center gap-4">
        {user ? (
          <Link to="/dashboard" className="btn-primary">Go to Dashboard</Link>
        ) : (
          <>
            <Link to="/register" className="btn-primary">Get Started</Link>
            <Link to="/login" className="btn-secondary">Log in</Link>
          </>
        )}
      </div>
    </div>
  );
}
