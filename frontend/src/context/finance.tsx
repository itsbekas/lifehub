import { createContext } from "react";

export const TimeRangeContext = createContext<{
  timeRange: {
    startDate: string;
    endDate: string;
  };
  setTimeRange: (range: { startDate: string; endDate: string }) => void;
}>({
  timeRange: {
    startDate: new Date(new Date().getFullYear(), new Date().getMonth(), 1)
      .toISOString()
      .split("T")[0],
    endDate: new Date().toISOString().split("T")[0],
  },
  setTimeRange: () => {},
});
