import { createFileRoute } from "@tanstack/react-router";

export const Route = createFileRoute("/(app)/admin/")({
  component: AdminDashboard,
});

function AdminDashboard() {
  return (
    <div>
      <h1>Admin Dashboard</h1>
      <p>Welcome to the admin dashboard.</p>
    </div>
  );
}

export default AdminDashboard;
