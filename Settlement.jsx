import { useState } from "react";
import { useParams } from "react-router-dom";
import { createSettlement } from "../services/api.js";
import Spinner from "../components/Spinner.jsx";

export default function Settlement() {
  const { loanId } = useParams();
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleGenerate() {
    setLoading(true);
    setError("");
    try {
      const res = await createSettlement(Number(loanId));
      setResult(res.data);
    } catch (err) {
      setError(err.response?.data?.detail || "Could not generate a recommendation.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="max-w-xl mx-auto px-4 py-8 space-y-6">
      <div className="card">
        <h1 className="text-xl font-semibold mb-2">Settlement Recommendation</h1>
        <p className="text-sm text-gray-500 mb-4">
          Our AI reviews your loan and financial profile to suggest a fair settlement offer.
        </p>
        <button onClick={handleGenerate} disabled={loading} className="btn-primary w-full">
          {loading ? "Generating..." : "Generate Recommendation"}
        </button>
        {error && <p className="text-sm text-red-500 mt-3">{error}</p>}
      </div>

      {loading && <Spinner label="Analyzing your loan..." />}

      {result && (
        <div className="card space-y-3">
          <div className="grid grid-cols-3 gap-3 text-center">
            <div>
              <p className="text-2xl font-semibold text-brand-600">{result.recommended_percentage}%</p>
              <p className="text-xs text-gray-400">Settlement %</p>
            </div>
            <div>
              <p className="text-2xl font-semibold">${result.suggested_amount.toLocaleString()}</p>
              <p className="text-xs text-gray-400">Suggested amount</p>
            </div>
            <div>
              <p className="text-2xl font-semibold">${result.monthly_payment_plan.toLocaleString()}</p>
              <p className="text-xs text-gray-400">Monthly plan</p>
            </div>
          </div>
          <div className="pt-2 border-t border-gray-100 dark:border-gray-700">
            <p className="text-sm font-medium mb-1">Reasoning</p>
            <pre className="text-sm text-gray-600 dark:text-gray-300 whitespace-pre-wrap font-sans">
              {result.ai_summary}
            </pre>
          </div>
        </div>
      )}
    </div>
  );
}
