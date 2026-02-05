import { useEffect, useState } from "react";
import { fetchJobs, fetchStats, fetchWorkers } from "../api/jobs";
import StatCard from "../components/StatCard";
import JobTable from "../components/JobTable";
import WorkerList from "../components/WorkerList";

export default function Dashboard() {
  const [jobs, setJobs] = useState([]);
  const [stats, setStats] = useState({});
  const [workers, setWorkers] = useState([]);
  const [filter, setFilter] = useState("");
  const [error, setError] = useState(null);

  useEffect(() => {
    let isMounted = true;

    const loadData = async () => {
      try {
        const [jobsRes, statsRes, workersRes] = await Promise.all([
          fetchJobs(filter),
          fetchStats(),
          fetchWorkers(),
        ]);

        if (!isMounted) return;

        setJobs(jobsRes.data);
        setStats(statsRes.data);
        setWorkers(workersRes.data);
        setError(null);
      } catch (err) {
        setError("Backend not reachable");
      }
    };

    loadData();

    const interval = setInterval(loadData, 3000); // 🔥 auto refresh

    return () => {
      isMounted = false;
      clearInterval(interval);
    };
  }, [filter]);

  return (
   <div className="min-h-screen bg-gray-100 p-6">
      <h1 className="text-2xl font-bold">Job Queue Dashboard</h1>

      {error && (
        <div className="p-3 bg-red-100 text-red-700 rounded">{error}</div>
      )}

      <div className="grid grid-cols-4 gap-4">
        <StatCard title="Queued" value={stats.queued} />
        <StatCard title="Running" value={stats.running} />
        <StatCard title="Success" value={stats.success} />
        <StatCard title="Failed" value={stats.failed} />
      </div>

      <div className="flex gap-2">
        {["", "QUEUED", "RUNNING", "SUCCESS", "FAILED"].map((s) => (
          <button
            key={s || "ALL"}
            onClick={() => setFilter(s)}
            className={`px-3 py-1 border rounded ${
              filter === s ? "bg-black text-white" : ""
            }`}
          >
            {s || "ALL"}
          </button>
        ))}
      </div>

      <JobTable jobs={jobs} />
      <WorkerList workers={workers} />
    </div>
  );
}
// export default function Dashboard() {
//   return (
//     <div className="min-h-screen bg-red-600 flex items-center justify-center">
//       <h1 className="text-5xl font-bold text-white">
//         Tailwind Works 🚀
//       </h1>
//     </div>
//   );
// }
