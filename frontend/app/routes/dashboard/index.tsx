import { Outlet } from "react-router";
import { HeaderMenu } from "~/components/HeaderMenu";
import { Container } from "@mantine/core";

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
