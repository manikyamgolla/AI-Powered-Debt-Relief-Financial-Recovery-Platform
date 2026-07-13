import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { listLoans } from "../services/api.js";
import LoanCard from "../components/LoanCard.jsx";
import Spinner from "../components/Spinner.jsx";

export default function Loans() {
  const [loans, setLoans] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    listLoans()
      .then((res) => setLoans(res.data))
      .finally(() => setLoading(false));
  }, []);

  return (
    <div className="max-w-6xl mx-auto px-4 py-8 space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-semibold">Your Loans</h1>
        <Link to="/loans/new" className="btn-primary">+ Add Loan</Link>
      </div>

      {loading ? (
        <Spinner label="Loading loans..." />
      ) : loans.length === 0 ? (
        <div className="card text-center text-gray-500">
          No loans yet. <Link to="/loans/new" className="text-brand-600 font-medium">Add your first loan</Link>.
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {loans.map((loan) => (
            <LoanCard key={loan.id} loan={loan} />
          ))}
        </div>
      )}
    </div>
  );
}
