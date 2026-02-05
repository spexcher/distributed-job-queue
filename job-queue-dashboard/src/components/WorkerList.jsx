export default function WorkerList({ workers }) {
  return (
    <div className="bg-white rounded-lg shadow p-5">
      <h2 className="text-lg font-semibold text-gray-800 mb-4">Workers</h2>

      <table className="w-full text-sm">
        <thead className="text-gray-500">
          <tr>
            <th className="text-left py-2">ID</th>
            <th className="text-left py-2">Status</th>
            <th className="text-left py-2">Last Seen</th>
          </tr>
        </thead>

        <tbody>
          {workers.map((w) => (
            <tr key={w.workerId} className="border-t">
              <td className="py-2 font-mono text-xs">
                {w.workerId.slice(0, 8)}
              </td>

              <td className="py-2">
                <span
                  className={`px-2 py-0.5 rounded-full text-xs font-medium
                    ${
                      w.status === "ALIVE"
                        ? "bg-green-100 text-green-700"
                        : "bg-red-100 text-red-700"
                    }`}
                >
                  {w.status}
                </span>
              </td>

              <td className="py-2 text-gray-600">
                {Math.floor(Date.now() / 1000 - w.lastSeen)}s ago
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
