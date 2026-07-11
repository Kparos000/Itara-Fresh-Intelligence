import type { SimulationSummary } from "@/data/simulation";

type BaselineSimulationSummaryProps = {
  summary: SimulationSummary;
  topEventCounts: [string, number][];
};

const currencyFormatter = new Intl.NumberFormat("en-CA", {
  currency: "CAD",
  maximumFractionDigits: 2,
  minimumFractionDigits: 2,
  style: "currency",
});

const numberFormatter = new Intl.NumberFormat("en-CA");

function formatEventLabel(eventType: string) {
  return eventType.replaceAll("_", " ");
}

export function BaselineSimulationSummary({
  summary,
  topEventCounts,
}: BaselineSimulationSummaryProps) {
  return (
    <section className="mt-10 border-y border-slate-800 py-6">
      <div className="flex flex-col gap-3 lg:flex-row lg:items-end lg:justify-between">
        <div>
          <p className="text-xs font-semibold uppercase tracking-[0.24em] text-emerald-300">
            Phase 2 simulator
          </p>
          <h2 className="mt-2 text-2xl font-semibold tracking-tight">
            Baseline simulation smoke summary
          </h2>
          <p className="mt-2 max-w-3xl text-sm leading-6 text-slate-300">
            Smoke simulation only. This is a deterministic wiring check for
            events, replay, and modeled loss totals; it is not a savings claim.
          </p>
        </div>
        <p className="text-sm text-slate-400">
          {summary.start_date} to {summary.end_date}
        </p>
      </div>

      <div className="mt-6 grid gap-4 md:grid-cols-3">
        <div className="border-l border-emerald-400/60 bg-slate-900/40 px-4 py-3">
          <p className="text-xs uppercase tracking-[0.18em] text-slate-400">
            Days
          </p>
          <p className="mt-2 text-2xl font-semibold">
            {numberFormatter.format(summary.days)}
          </p>
        </div>

        <div className="border-l border-emerald-400/60 bg-slate-900/40 px-4 py-3">
          <p className="text-xs uppercase tracking-[0.18em] text-slate-400">
            Total events
          </p>
          <p className="mt-2 text-2xl font-semibold">
            {numberFormatter.format(summary.total_events)}
          </p>
        </div>

        <div className="border-l border-emerald-400/60 bg-slate-900/40 px-4 py-3">
          <p className="text-xs uppercase tracking-[0.18em] text-slate-400">
            Modeled net loss
          </p>
          <p className="mt-2 text-2xl font-semibold">
            {currencyFormatter.format(summary.total_net_loss)}
          </p>
        </div>
      </div>

      <div className="mt-5 flex flex-wrap gap-3">
        {topEventCounts.map(([eventType, count]) => (
          <div
            className="border border-slate-800 bg-slate-900/30 px-3 py-2"
            key={eventType}
          >
            <p className="text-xs uppercase tracking-[0.16em] text-slate-400">
              {formatEventLabel(eventType)}
            </p>
            <p className="mt-1 text-lg font-semibold">
              {numberFormatter.format(count)}
            </p>
          </div>
        ))}
      </div>
    </section>
  );
}
