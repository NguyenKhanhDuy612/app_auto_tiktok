"use client";

import { useRouter } from "next/navigation";
import { routes } from "./index";

export const useNavigate = () => {
  const router = useRouter();

  const navigate = (path: keyof typeof routes) => {
    router.push(routes[path]);
  };
  return { navigate };
};