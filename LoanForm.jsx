import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { useForm } from "react-hook-form";
import { createLoan, getLoan, updateLoan } from "../services/api.js";
import Spinner from "../components/Spinner.jsx";

const LOAN_TYPES = ["personal", "credit_card", "auto", "home", "education", "other"];
const STATUSES = ["active", "overdue", "settled", "closed"];

export default function LoanForm() {
  const { id } = useParams();
  const isEdit = Boolean(id);
  const navigate = useNavigate();
  const { register, handleSubmit, reset, formState: { errors, isSubmitting } } = useForm();
  const [loading, setLoading] = useState(isEdit);
  const [error, setError] = useState("");

  useEffect(() => {
    if (!isEdit) return;
    getLoan(id)
      .then((res) => reset(res.data))
      .finally(() => setLoading(false));
  }, [id, isEdit, reset]);

  async function onSubmit(data) {
    setError("");
    const payload = {
      ...data,
      outstanding_amount: Number(data.outstanding_amount),
      emi: Number(data.emi),
      interest_rate: Number(data.interest_rate),
      overdue_days: Number(data.overdue_days),
      tenure_months: Number(data.tenure_months),
    };
    try {
      if (isEdit) {
        await updateLoan(id, payload);
      } else {
        await createLoan(payload);
      }
      navigate("/loans");
    } catch (err) {
      setError(err.response?.data?.detail || "Could not save loan.");
    }
  }

  if (loading) return <Spinner label="Loading loan..." />;

  return (
    <div className="max-w-xl mx-auto px-4 py-8">
      <div className="card">
        <h1 className="text-xl font-semibold mb-6">{isEdit ? "Edit Loan" : "Add Loan"}</h1>
        <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
          <div>
            <label className="text-sm font-medium">Lender name</label>
            <input className="input mt-1" {...register("lender_name", { required: true })} />
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="text-sm font-medium">Loan type</label>
              <select className="input mt-1" {...register("loan_type")}>
                {LOAN_TYPES.map((t) => (
                  <option key={t} value={t}>{t.replace("_", " ")}</option>
                ))}
              </select>
            </div>
            <div>
              <label className="text-sm font-medium">Status</label>
              <select className="input mt-1" {...register("status")}>
                {STATUSES.map((s) => (
                  <option key={s} value={s}>{s}</option>
                ))}
              </select>
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="text-sm font-medium">Outstanding amount ($)</label>
              <input type="number" step="0.01" className="input mt-1" {...register("outstanding_amount", { required: true })} />
            </div>
            <div>
              <label className="text-sm font-medium">Monthly EMI ($)</label>
              <input type="number" step="0.01" className="input mt-1" {...register("emi", { required: true })} />
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="text-sm font-medium">Interest rate (%)</label>
              <input type="number" step="0.01" className="input mt-1" {...register("interest_rate", { required: true })} />
            </div>
            <div>
              <label className="text-sm font-medium">Overdue days</label>
              <input type="number" className="input mt-1" defaultValue={0} {...register("overdue_days")} />
            </div>
          </div>

          <div>
            <label className="text-sm font-medium">Tenure (months)</label>
            <input type="number" className="input mt-1" {...register("tenure_months", { required: true })} />
          </div>

          {error && <p className="text-sm text-red-500">{error}</p>}

          <div className="flex gap-3 pt-2">
            <button type="submit" disabled={isSubmitting} className="btn-primary flex-1">
              {isSubmitting ? "Saving..." : isEdit ? "Save changes" : "Add loan"}
            </button>
            <button type="button" onClick={() => navigate(-1)} className="btn-secondary">
              Cancel
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
