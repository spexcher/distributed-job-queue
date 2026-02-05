export default function StatCard({ title, value }) {
  return (
    <div className="p-4 border rounded shadow-sm">
      <p className="text-gray-500">{title}</p>
      <p className="text-2xl font-bold">{value ?? 0}</p>
    </div>
  );
}
