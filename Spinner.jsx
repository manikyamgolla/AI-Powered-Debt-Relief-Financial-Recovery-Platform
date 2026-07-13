export default function Spinner({ label = "Loading..." }) {
  return (
    <div className="flex items-center justify-center gap-2 py-10 text-gray-400 text-sm">
      <div className="w-4 h-4 border-2 border-brand-400 border-t-transparent rounded-full animate-spin" />
      {label}
    </div>
  );
}
