import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useForm } from "react-hook-form";
import { runFinancialAnalysis } from "../services/api.js";

export default function FinancialProfileForm() {
  const { register, handleSubmit, formState: { isSubmitting } } = useForm();
  const navigate = useNavigate();
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");

  async function onSubmit(data) {
    setError("");
    try {
      const payload = {
        monthly_income: Number(data.monthly_income),
        monthly_expenses: Number(data.monthly_expenses),
        savings: Number(data.savings || 0),
      };
      const res = await runFinancialAnalysis(payload);
      setResult(res.data);
    } catch (err) {
      setError(err.response?.data?.detail || "Could not run analysis.");
    }
  }

  return (
    <div className="max-w-xl mx-auto px-4 py-8 space-y-6">
      <div className="card">
        <h1 className="text-xl font-semibold mb-1">Financial Profile</h1>
        <p className="text-sm text-gray-500 mb-6">
          Enter your income and expenses so we can compute your debt stress and surplus.
        </p>
        <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
          <div>
            <label className="text-sm font-medium">Monthly income ($)</label>
            <input type="number" step="0.01" className="input mt-1" {...register("monthly_income", { required: true })} />
          </div>
          <div>
            <label className="text-sm font-medium">Monthly expenses ($)</label>
            <input type="number" step="0.01" className="input mt-1" {...register("monthly_expenses", { required: true })} />
          </div>
          <div>
            <label className="text-sm font-medium">Savings ($)</label>
            <input type="number" step="0.01" className="input mt-1" defaultValue={0} {...register("savings")} />
          </div>
          {error && <p className="text-sm text-red-500">{error}</p>}
          <button type="submit" disabled={isSubmitting} className="btn-primary w-full">
            {isSubmitting ? "Analyzing..." : "Run Analysis"}
          </button>
        </form>
      </div>

      {result && (
        <div className="card space-y-3">
          <div className="grid grid-cols-2 gap-3 text-sm">
            <div><p className="text-gray-400">Monthly surplus</p><p className="font-medium">${result.monthly_surplus.toLocaleString()}</p></div>
            <div><p className="text-gray-400">EMI-to-income</p><p className="font-medium">{result.emi_to_income_ratio}%</p></div>
            <div><p className="text-gray-400">Debt-to-income</p><p className="font-medium">{result.debt_to_income_ratio}%</p></div>
            <div><p className="text-gray-400">Stress level</p><p className="font-medium capitalize">{result.stress_level}</p></div>
          </div>
          <button onClick={() => navigate("/dashboard")} className="btn-primary w-full">
            View Dashboard
          </button>
        </div>
      )}
    </div>
  );
}
