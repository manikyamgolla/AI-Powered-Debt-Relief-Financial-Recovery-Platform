import { useEffect, useState } from "react";
import { Link, useNavigate, useParams } from "react-router-dom";
import { deleteLoan, getLoan } from "../services/api.js";
import Spinner from "../components/Spinner.jsx";
import Toast from "../components/Toast.jsx";

export default function LoanDetails() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [loan, setLoan] = useState(null);
  const [loading, setLoading] = useState(true);
  const [toast, setToast] = useState("");

  useEffect(() => {
    getLoan(id)
      .then((res) => setLoan(res.data))
      .finally(() => setLoading(false));
  }, [id]);

  async function handleDelete() {
    if (!confirm("Delete this loan? This cannot be undone.")) return;
    await deleteLoan(id);
    navigate("/loans");
  }

  if (loading) return <Spinner label="Loading loan details..." />;
  if (!loan) return <p className="text-center py-10 text-gray-500">Loan not found.</p>;

  return (
    <div className="max-w-2xl mx-auto px-4 py-8 space-y-6">
      <div className="card space-y-4">
        <div className="flex items-center justify-between">
          <h1 className="text-xl font-semibold">{loan.lender_name}</h1>
          <span className="text-xs px-2 py-1 rounded-full bg-gray-100 dark:bg-gray-700 capitalize">
            {loan.status}
          </span>
        </div>

        <div className="grid grid-cols-2 gap-4 text-sm">
          <div><p className="text-gray-400">Type</p><p className="font-medium capitalize">{loan.loan_type.replace("_", " ")}</p></div>
          <div><p className="text-gray-400">Outstanding</p><p className="font-medium">${loan.outstanding_amount.toLocaleString()}</p></div>
          <div><p className="text-gray-400">EMI</p><p className="font-medium">${loan.emi.toLocaleString()}</p></div>
          <div><p className="text-gray-400">Interest rate</p><p className="font-medium">{loan.interest_rate}%</p></div>
          <div><p className="text-gray-400">Overdue days</p><p className="font-medium">{loan.overdue_days}</p></div>
          <div><p className="text-gray-400">Tenure</p><p className="font-medium">{loan.tenure_months} months</p></div>
        </div>

        <div className="flex flex-wrap gap-3 pt-2">
          <Link to={`/loans/${id}/edit`} className="btn-secondary">Edit</Link>
          <button onClick={handleDelete} className="btn-secondary text-red-600">Delete</button>
        </div>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
        <Link to={`/settlement/${id}`} className="card hover:shadow-md transition text-center">
          <p className="font-semibold text-brand-600">Get Settlement Recommendation</p>
          <p className="text-xs text-gray-400 mt-1">AI-generated settlement % and payment plan</p>
        </Link>
        <Link to={`/letter/${id}`} className="card hover:shadow-md transition text-center">
          <p className="font-semibold text-brand-600">Generate Negotiation Letter</p>
          <p className="text-xs text-gray-400 mt-1">Draft a hardship / settlement request email</p>
        </Link>
      </div>

      <Toast message={toast} onClose={() => setToast("")} />
    </div>
  );
}
