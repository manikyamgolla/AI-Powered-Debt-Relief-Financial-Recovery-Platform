import { useEffect, useState } from "react";
import { listHistory } from "../services/api.js";
import Spinner from "../components/Spinner.jsx";

export default function History() {
  const [entries, setEntries] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    listHistory()
      .then((res) => setEntries(res.data))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <Spinner label="Loading history..." />;

  return (
    <div className="max-w-3xl mx-auto px-4 py-8 space-y-4">
      <h1 className="text-2xl font-semibold">AI History</h1>

      {entries.length === 0 && (
        <div className="card text-center text-gray-500">No AI interactions yet.</div>
      )}

      {entries.map((entry) => (
        <div key={entry.id} className="card">
          <div className="flex items-center justify-between mb-2">
            <span className="text-xs px-2 py-1 rounded-full bg-gray-100 dark:bg-gray-700 capitalize">
              {entry.module_type}
            </span>
            <span className="text-xs text-gray-400">
              {new Date(entry.created_at).toLocaleString()}
              {entry.used_fallback && " · fallback template"}
            </span>
          </div>
          <p className="text-sm font-medium text-gray-500 mb-1">Prompt</p>
          <p className="text-sm text-gray-700 dark:text-gray-300 mb-3 line-clamp-3">{entry.prompt_text}</p>
          <p className="text-sm font-medium text-gray-500 mb-1">Response</p>
          <p className="text-sm text-gray-700 dark:text-gray-300 whitespace-pre-wrap line-clamp-4">
            {entry.response_text}
          </p>
        </div>
      ))}
    </div>
  );
}
