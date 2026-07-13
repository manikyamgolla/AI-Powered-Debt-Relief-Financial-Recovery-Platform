import { useState } from "react";
import { useParams } from "react-router-dom";
import { generateLetter } from "../services/api.js";
import Spinner from "../components/Spinner.jsx";
import Toast from "../components/Toast.jsx";

const LETTER_TYPES = [
  { value: "settlement_request", label: "Settlement Request" },
  { value: "hardship_explanation", label: "Hardship Explanation" },
  { value: "debt_restructuring", label: "Debt Restructuring Request" },
];

export default function NegotiationLetter() {
  const { loanId } = useParams();
  const [letterType, setLetterType] = useState("settlement_request");
  const [letterText, setLetterText] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [toast, setToast] = useState("");

  async function handleGenerate() {
    setLoading(true);
    setError("");
    try {
      const res = await generateLetter({ loan_id: Number(loanId), letter_type: letterType });
      setLetterText(res.data.letter_text);
    } catch (err) {
      setError(err.response?.data?.detail || "Could not generate a letter.");
    } finally {
      setLoading(false);
    }
  }

  function handleCopy() {
    navigator.clipboard.writeText(letterText);
    setToast("Letter copied to clipboard");
  }

  return (
    <div className="max-w-2xl mx-auto px-4 py-8 space-y-6">
      <div className="card space-y-4">
        <h1 className="text-xl font-semibold">Negotiation Letter</h1>

        <div>
          <label className="text-sm font-medium">Letter type</label>
          <select className="input mt-1" value={letterType} onChange={(e) => setLetterType(e.target.value)}>
            {LETTER_TYPES.map((t) => (
              <option key={t.value} value={t.value}>{t.label}</option>
            ))}
          </select>
        </div>

        <button onClick={handleGenerate} disabled={loading} className="btn-primary w-full">
          {loading ? "Drafting..." : "Generate Letter"}
        </button>
        {error && <p className="text-sm text-red-500">{error}</p>}
      </div>

      {loading && <Spinner label="Drafting your letter..." />}

      {letterText && (
        <div className="card space-y-3">
          <textarea
            className="input min-h-[280px] font-sans"
            value={letterText}
            onChange={(e) => setLetterText(e.target.value)}
          />
          <div className="flex gap-3">
            <button onClick={handleCopy} className="btn-secondary flex-1">Copy to clipboard</button>
          </div>
        </div>
      )}

      <Toast message={toast} onClose={() => setToast("")} />
    </div>
  );
}
