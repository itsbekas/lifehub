import { useMatches, useNavigate } from "@tanstack/react-router";
import { Stack, Center, Tooltip, UnstyledButton } from "@mantine/core";
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

interface NavbarLinkProps {
  icon: typeof IconChartPie;
  label: string;
  active?: boolean;
  onClick?: () => void;
}

function NavbarLink({ icon: Icon, label, active, onClick }: NavbarLinkProps) {
  return (
    <Tooltip label={label} position="right" transitionProps={{ duration: 0 }}>
      <UnstyledButton
        onClick={onClick}
        className={classes.link}
        data-active={active || undefined}
      >
        <Icon size={20} stroke={1.5} />
      </UnstyledButton>
    </Tooltip>
  );
}

const linkData = [
  {
    icon: IconWallet,
    color: "primary",
    label: "Dashboard",
    to: "/dashboard/finance",
    description: "Finance overview",
  },
  {
    icon: IconSettings,
    color: "primary",
    label: "Settings",
    to: "/settings",
    description: "App configuration",
  },
  {
    icon: IconUser,
    color: "primary",
    label: "Profile",
    to: "/profile",
    description: "Your account",
  },
];

export function Sidebar() {
  const matches = useMatches();
  const navigate = useNavigate();
  const currentPath = matches[matches.length - 1]?.pathname || "";
  const { data: user } = useCurrentUser();

  const isActive = (path: string) => {
    return currentPath.startsWith(path);
  };

  const handleLogout = () => {
    logoutUser();
    navigate({ to: "/" });
  };

  const links = linkData.map((link) => (
    <NavbarLink
      {...link}
      key={link.label}
      active={isActive(link.to)}
      onClick={() => navigate({ to: link.to })}
    />
  ));

  return (
    <nav className={classes.navbar}>
      <Center>
        <NavbarLink icon={IconChartPie} label="Lifehub" />
      </Center>

      <div className={classes.navbarMain}>
        <Stack justify="center" gap={0}>
          {links}
        </Stack>
      </div>

      <Stack justify="center" gap={0}>
        <NavbarLink icon={IconLogout} label="Logout" onClick={handleLogout} />
      </Stack>
    </nav>
  );
}
