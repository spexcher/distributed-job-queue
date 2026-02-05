export default function JobTable({ jobs }) {
  return (
    <div className="bg-white rounded-lg shadow overflow-x-auto">
      <table className="w-full text-sm">
        <thead className="bg-gray-50 text-gray-600">
          <tr>
            <th className="px-4 py-3 text-left">ID</th>
            <th className="px-4 py-3 text-left">Type</th>
            <th className="px-4 py-3 text-left">Status</th>
            <th className="px-4 py-3 text-left">Attempts</th>
            <th className="px-4 py-3 text-left">Worker</th>
          </tr>
        </thead>

        <tbody>
          {jobs.map((j) => (
            <tr key={j.jobId} className="border-t hover:bg-gray-50">
              <td className="px-4 py-2 font-mono text-xs">
                {j.jobId.slice(0, 8)}
              </td>

              <td className="px-4 py-2">{j.jobType}</td>

              <td className="px-4 py-2">
                <span
                  className={`px-2 py-0.5 rounded-full text-xs font-medium
                    ${
                      j.status === "SUCCESS"
                        ? "bg-green-100 text-green-700"
                        : j.status === "FAILED"
                        ? "bg-red-100 text-red-700"
                        : j.status === "RUNNING"
                        ? "bg-yellow-100 text-yellow-700"
                        : "bg-gray-100 text-gray-700"
                    }`}
                >
                  {j.status}
                </span>
              </td>

              <td className="px-4 py-2">{j.attempts}</td>

              <td className="px-4 py-2 font-mono text-xs">
                {j.lockedBy?.slice(0, 8) || "-"}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
