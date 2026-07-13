import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext.jsx";

export default function Header() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  return (
    <header className="border-b border-gray-100 dark:border-gray-800 bg-white/80 dark:bg-gray-900/80 backdrop-blur sticky top-0 z-10">
      <div className="max-w-6xl mx-auto px-4 py-3 flex items-center justify-between">
        <Link to="/" className="font-semibold text-brand-600 dark:text-brand-400 text-lg">
          DebtRelief AI
        </Link>
        {user && (
          <nav className="hidden md:flex gap-5 text-sm">
            <Link to="/dashboard" className="hover:text-brand-600">Dashboard</Link>
            <Link to="/loans" className="hover:text-brand-600">Loans</Link>
            <Link to="/analytics" className="hover:text-brand-600">Analytics</Link>
            <Link to="/history" className="hover:text-brand-600">History</Link>
          </nav>
        )}
        <div className="flex items-center gap-3">
          {user ? (
            <>
              <span className="text-sm text-gray-500 hidden sm:inline">{user.name}</span>
              <button
                className="btn-secondary text-sm"
                onClick={() => {
                  logout();
                  navigate("/login");
                }}
              >
                Log out
              </button>
            </>
          ) : (
            <>
              <Link to="/login" className="btn-secondary text-sm">Log in</Link>
              <Link to="/register" className="btn-primary text-sm">Sign up</Link>
            </>
          )}
        </div>
      </div>
    </header>
  );
}
