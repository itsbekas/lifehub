import { Outlet } from "react-router";
import { HeaderMenu } from "~/components/HeaderMenu";
import { Container } from "@mantine/core";
import { redirect } from "react-router";
import { getSession } from "~/utils/session";
import type { Route } from "./+types/dashboard";

export async function loader({ request }: Route.LoaderArgs) {
  const session = await getSession(request.headers.get("Cookie"));
  if (!session.has("access_token")) {
    return redirect("/login");
  }
  return null;
}

const DashboardLayout = () => {
  return (
    <div>
      {/* Header */}
      <HeaderMenu />

      {/* Main Content */}
      <Container size="lg" style={{ paddingTop: "1rem" }}>
        <Outlet />
      </Container>
    </div>
  );
};

export default DashboardLayout;
