export default function Home() {
  return (
    <main className="min-h-screen bg-slate-950 px-8 py-10 text-white">
      <section className="mx-auto max-w-6xl">
        <p className="text-sm font-semibold uppercase tracking-[0.3em] text-emerald-400">
          Itara Fresh Intelligence
        </p>

        <h1 className="mt-6 text-5xl font-bold tracking-tight">
          Fresh Grocery Network Visualizer
        </h1>

        <p className="mt-5 max-w-3xl text-lg leading-8 text-slate-300">
          A visual operating layer for stores, suppliers, warehouse inventory,
          policy-grounded replenishment, and future agentic decision traces.
        </p>

        <div className="mt-10 grid gap-4 md:grid-cols-3 lg:grid-cols-6">
          <MetricCard label="Stores" value="15" />
          <MetricCard label="Suppliers" value="10" />
          <MetricCard label="Warehouse" value="1" />
          <MetricCard label="SKUs" value="500" />
          <MetricCard label="Policies" value="5" />
          <MetricCard label="Distance Rows" value="650" />
        </div>

        <div className="mt-10 rounded-3xl border border-slate-800 bg-slate-900 p-8">
          <h2 className="text-2xl font-bold">Network map placeholder</h2>
          <p className="mt-3 text-slate-400">
            This confirms the frontend skeleton is working. Next, we will connect
            this page to real backend-generated network data.
          </p>

          <div className="mt-8 h-[420px] rounded-2xl border border-slate-800 bg-slate-950 p-6">
            <div className="relative h-full">
              <MapPin label="Warehouse" className="left-[45%] top-[42%]" />
              <MapPin label="King West" className="left-[52%] top-[58%]" />
              <MapPin label="North York" className="left-[56%] top-[30%]" />
              <MapPin label="Scarborough" className="left-[73%] top-[35%]" />
              <MapPin label="Mississauga" className="left-[28%] top-[70%]" />
              <MapPin label="Produce Supplier" className="left-[8%] top-[82%]" />
            </div>
          </div>
        </div>
      </section>
    </main>
  );
}

function MetricCard({ label, value }: { label: string; value: string }) {
  return (
    <div className="rounded-2xl border border-slate-800 bg-slate-900 p-5">
      <p className="text-sm text-slate-400">{label}</p>
      <p className="mt-2 text-3xl font-bold">{value}</p>
    </div>
  );
}

function MapPin({
  label,
  className,
}: {
  label: string;
  className: string;
}) {
  return (
    <div className={`absolute ${className}`}>
      <div className="flex items-center gap-2">
        <span className="h-4 w-4 rounded-full bg-emerald-400 shadow-lg shadow-black" />
        <span className="rounded-full bg-slate-900/90 px-3 py-1 text-xs font-semibold text-white ring-1 ring-white/10">
          {label}
        </span>
      </div>
    </div>
  );
}
