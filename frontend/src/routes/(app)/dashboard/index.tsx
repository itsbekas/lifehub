import { createFileRoute, redirect } from "@tanstack/react-router";

export const Route = createFileRoute("/(app)/dashboard/")({
  beforeLoad: () => {
    throw redirect({ to: "/dashboard/finance" });
  },
});

const Dashboard = () => {
  return (
    <div>
      <h1>Dashboard</h1>
      <p>This is the dashboard.</p>
    </div>
  );
};

export default Dashboard;
