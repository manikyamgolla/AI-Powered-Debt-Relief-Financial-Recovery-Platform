import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { getDashboard } from "../services/api.js";
import StatCard from "../components/StatCard.jsx";
import Spinner from "../components/Spinner.jsx";

const stressTone = {
  low: "good",
  moderate: "default",
  high: "warn",
  critical: "bad",
};

export default function Dashboard() {
  const [summary, setSummary] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    getDashboard()
      .then((res) => setSummary(res.data))
      .catch(() => setError("Could not load dashboard. Try adding a loan and running financial analysis first."))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <Spinner label="Loading dashboard..." />;

  return (
    <div className="max-w-6xl mx-auto px-4 py-8 space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-semibold">Dashboard</h1>
        <Link to="/loans/new" className="btn-primary">+ Add Loan</Link>
      </div>

      {error && <div className="card text-sm text-amber-600">{error}</div>}

      {summary && (
        <>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <StatCard label="Total Loans" value={summary.total_loans} />
            <StatCard label="Total Outstanding" value={`$${summary.total_outstanding.toLocaleString()}`} />
            <StatCard label="Total EMI / month" value={`$${summary.total_emi.toLocaleString()}`} />
            <StatCard
              label="Monthly Surplus"
              value={`$${summary.monthly_surplus.toLocaleString()}`}
              tone={summary.monthly_surplus >= 0 ? "good" : "bad"}
            />
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <StatCard
              label="Financial Health Score"
              value={`${summary.health_score} / 100`}
              tone={stressTone[summary.stress_level]}
            />
            <StatCard
              label="Debt Stress Level"
              value={summary.stress_level}
              tone={stressTone[summary.stress_level]}
            />
          </div>

          <div className="card">
            <h2 className="font-semibold mb-3">Loans by Status</h2>
            <div className="flex gap-4 flex-wrap">
              {Object.entries(summary.loans_by_status).length === 0 && (
                <p className="text-sm text-gray-400">No loans yet.</p>
              )}
              {Object.entries(summary.loans_by_status).map(([status, count]) => (
                <div key={status} className="px-3 py-2 rounded-xl bg-gray-100 dark:bg-gray-700 text-sm">
                  <span className="capitalize">{status}</span>: <span className="font-medium">{count}</span>
                </div>
              ))}
            </div>
          </div>
        </>
      )}
    </div>
  );
}
