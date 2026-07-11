import simulationSummaryJson from "./simulation-summary.json";

export type DailyNetLoss = {
  date: string;
  net_loss: number;
};

export type SimulationSummary = {
  start_date: string;
  end_date: string;
  days: number;
  total_events: number;
  event_counts: Record<string, number>;
  total_spoilage_loss: number;
  total_stockout_lost_margin: number;
  total_markdown_margin_loss: number;
  total_transfer_cost: number;
  total_holding_cost: number;
  total_inference_cost: number;
  total_net_loss: number;
  daily_net_loss: DailyNetLoss[];
};

export const simulationSummary =
  simulationSummaryJson as unknown as SimulationSummary;

export const topSimulationEventCounts = Object.entries(
  simulationSummary.event_counts,
)
  .sort(([, leftCount], [, rightCount]) => rightCount - leftCount)
  .slice(0, 3);
