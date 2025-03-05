import { Burger, Container, Group } from "@mantine/core";
import { useDisclosure } from "@mantine/hooks";
import classes from "~/styles/HeaderMenu.module.css";

const links = [
  { link: "/dashboard", label: "Dashboard" },
  { link: "/settings", label: "Settings" },
  { link: "/profile", label: "Profile" },
];

export function HeaderMenu() {
  const [opened, { toggle }] = useDisclosure(false);

  const items = links.map((link) => (
    <a
      key={link.label}
      href={link.link}
      className={classes.link}
      onClick={(event) => event.preventDefault()}
    >
      {link.label}
    </a>
  ));

  return (
    <header className={classes.header}>
      <Container size="md">
        <div className={classes.inner}>
          <div>Lifehub</div>
          <Group gap={5} visibleFrom="sm">
            {items}
          </Group>
          <Burger opened={opened} onClick={toggle} size="sm" hiddenFrom="sm" />
        </div>
      </Container>
    </header>
  );
}
