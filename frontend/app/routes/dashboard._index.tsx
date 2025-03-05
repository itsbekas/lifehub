import { redirect } from "react-router";

export async function loader() {
  // redirect to /dashboard/finance until we have a dashboard
  return redirect("/dashboard/finance");
}

const Dashboard = () => {
  return (
    <div>
      <h1>Dashboard</h1>
      <p>This is the dashboard.</p>
    </div>
  );
};

export default Dashboard;
