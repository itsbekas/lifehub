import { Link, useMatches, useNavigate } from "@tanstack/react-router";
import {
  Stack,
  Text,
  NavLink,
  Avatar,
  Group,
  Divider,
  Box,
  ThemeIcon,
} from "@mantine/core";
import {
  IconSettings,
  IconUser,
  IconLogout,
  IconWallet,
  IconChartPie,
} from "@tabler/icons-react";
import { useCurrentUser } from "~/hooks/useUserQueries";
import { logoutUser } from "~/lib/cookies";
import classes from "~/styles/Sidebar.module.css";

export function Sidebar() {
  const matches = useMatches();
  const navigate = useNavigate();
  const currentPath = matches[matches.length - 1]?.pathname || "";
  const { data: user } = useCurrentUser();

  const isActive = (path: string) => {
    return currentPath.startsWith(path);
  };

  const links = [
    {
      icon: <IconWallet size={18} stroke={1.5} />,
      color: "primary",
      label: "Dashboard",
      to: "/dashboard/finance",
      description: "Finance overview",
    },
    {
      icon: <IconSettings size={18} stroke={1.5} />,
      color: "primary",
      label: "Settings",
      to: "/settings",
      description: "App configuration",
    },
    {
      icon: <IconUser size={18} stroke={1.5} />,
      color: "primary",
      label: "Profile",
      to: "/profile",
      description: "Your account",
    },
  ];

  const handleLogout = () => {
    logoutUser();
    navigate({ to: "/login" });
  };

  const navLinks = links.map((link) => (
    <NavLink
      key={link.label}
      component={Link}
      to={link.to}
      label={
        <div>
          <Text size="sm" fw={500}>
            {link.label}
          </Text>
          <Text size="xs" c="dimmed" lineClamp={1}>
            {link.description}
          </Text>
        </div>
      }
      leftSection={
        <ThemeIcon variant="light" color={link.color} size="md">
          {link.icon}
        </ThemeIcon>
      }
      active={isActive(link.to)}
      variant={isActive(link.to) ? "light" : "subtle"}
      className={isActive(link.to) ? classes.activeLink : ""}
      py="xs"
      mb={5}
    />
  ));

  // Get initials from user name or username
  const getInitials = () => {
    if (!user) return "U";

    if (user.name) {
      return user.name
        .split(" ")
        .map((part) => part[0])
        .join("")
        .toUpperCase()
        .substring(0, 2);
    }

    return user.username.substring(0, 2).toUpperCase();
  };

  return (
    <Stack className={classes.sidebar} justify="space-between" h="100%">
      <Stack gap="md">
        <Box className={classes.header}>
          <Group gap="xs">
            <ThemeIcon size="lg" radius="xl" color="primary" variant="filled">
              <IconChartPie size={20} />
            </ThemeIcon>
            <Text size="xl" fw={700} c="primary">
              Lifehub
            </Text>
          </Group>
        </Box>
        <Divider />
        <Stack gap="xs">{navLinks}</Stack>
      </Stack>

      <Stack gap="xs">
        <Divider />
        <Group p="xs">
          <Avatar color="primary" radius="xl">
            {getInitials()}
          </Avatar>
          <Box style={{ flex: 1 }}>
            <Text size="sm" fw={500}>
              {user?.name || user?.username || "User"}
            </Text>
            <Text size="xs" c="dimmed" lineClamp={1}>
              {user?.email || ""}
            </Text>
          </Box>
        </Group>
        <NavLink
          onClick={handleLogout}
          label="Logout"
          leftSection={
            <ThemeIcon variant="light" color="red" size="sm">
              <IconLogout size={16} stroke={1.5} />
            </ThemeIcon>
          }
          variant="subtle"
          color="red"
        />
      </Stack>
    </Stack>
  );
}
