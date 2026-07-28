import siteData from "../../content/site.json";
import treatsData from "../../content/treats.json";
import eventsData from "../../content/events.json";
import policiesData from "../../content/policies.json";
import galleryData from "../../content/gallery.json";

export type TreatIcon = "cookie" | "brownie" | "tray" | "gift" | "jar" | "sparkle";

export interface TreatCategory {
  slug: string;
  name: string;
  shortDescription: string;
  longDescription: string;
  icon: TreatIcon;
  availability: "rotating" | "custom-order" | "limited" | "seasonal";
}

export const site = siteData;
export const treats = treatsData as unknown as Omit<typeof treatsData, "categories"> & { categories: TreatCategory[] };
export const events = eventsData;
export const policies = policiesData;
export const gallery = galleryData;

export const navigation = [
  { href: "/treats", label: "Treats" },
  { href: "/custom-orders", label: "Custom orders" },
  { href: "/markets", label: "Markets" },
  { href: "/about", label: "About" },
  { href: "/faq", label: "FAQ" }
];
