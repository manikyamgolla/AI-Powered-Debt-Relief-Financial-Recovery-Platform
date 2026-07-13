import { Link } from "react-router-dom";

const statusColors = {
  active: "bg-blue-100 text-blue-700",
  overdue: "bg-red-100 text-red-700",
  settled: "bg-green-100 text-green-700",
  closed: "bg-gray-100 text-gray-600",
};

export default function LoanCard({ loan }) {
  return (
    <div className="card flex flex-col gap-2">
      <div className="flex items-center justify-between">
        <h3 className="font-semibold">{loan.lender_name}</h3>
        <span className={`text-xs px-2 py-1 rounded-full ${statusColors[loan.status] || "bg-gray-100"}`}>
          {loan.status}
        </span>
      </div>
      <p className="text-sm text-gray-500 capitalize">{loan.loan_type.replace("_", " ")}</p>
      <div className="grid grid-cols-2 gap-2 text-sm mt-1">
        <div>
          <p className="text-gray-400">Outstanding</p>
          <p className="font-medium">${loan.outstanding_amount.toLocaleString()}</p>
        </div>
        <div>
          <p className="text-gray-400">EMI</p>
          <p className="font-medium">${loan.emi.toLocaleString()}</p>
        </div>
        <div>
          <p className="text-gray-400">Interest</p>
          <p className="font-medium">{loan.interest_rate}%</p>
        </div>
        <div>
          <p className="text-gray-400">Overdue</p>
          <p className="font-medium">{loan.overdue_days} days</p>
        </div>
      </div>
      <Link to={`/loans/${loan.id}`} className="btn-primary text-center text-sm mt-2">
        View Details
      </Link>
    </div>
  );
}
