import { Center, Title, Button } from "@mantine/core";
import { useNavigate } from "react-router";

export default function Home() {
  const navigate = useNavigate();

  return (
    <Center style={{ height: "100vh", flexDirection: "column" }}>
      <Title order={1} style={{ fontSize: "8rem" }}>Lifehub</Title>
      <Button style={{ marginTop: "2rem" }} onClick={() => navigate("/login")}>
        Login
      </Button>
    </Center>
  );
}