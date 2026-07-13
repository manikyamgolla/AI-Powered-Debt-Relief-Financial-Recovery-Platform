export default function StatCard({ label, value, sublabel, tone = "default" }) {
  const toneClasses = {
    default: "text-gray-800 dark:text-gray-100",
    good: "text-green-600",
    warn: "text-amber-600",
    bad: "text-red-600",
  };

  return (
    <div className="card">
      <p className="text-sm text-gray-400">{label}</p>
      <p className={`text-2xl font-semibold mt-1 ${toneClasses[tone] || toneClasses.default}`}>{value}</p>
      {sublabel && <p className="text-xs text-gray-400 mt-1">{sublabel}</p>}
    </div>
  );
}
