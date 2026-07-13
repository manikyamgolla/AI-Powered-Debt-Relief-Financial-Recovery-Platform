import { useEffect } from "react";

export default function Toast({ message, type = "info", onClose }) {
  useEffect(() => {
    if (!message) return;
    const timer = setTimeout(onClose, 4000);
    return () => clearTimeout(timer);
  }, [message, onClose]);

  if (!message) return null;

  const colors = {
    info: "bg-gray-800",
    success: "bg-green-600",
    error: "bg-red-600",
  };

  return (
    <div
      className={`fixed bottom-5 right-5 ${colors[type] || colors.info} text-white text-sm px-4 py-3 rounded-xl shadow-lg z-50`}
    >
      {message}
    </div>
  );
}
