import rawSite from '../../content/site.json';

export type NavigationItem = {
  label: string;
  href: string;
};

export type TreatCategory = {
  name: string;
  description: string;
  availability: string;
};

export type RareTreatsSite = typeof rawSite;

export const site = rawSite satisfies RareTreatsSite;

export const publicNavigation: NavigationItem[] = site.navigation.filter((item) => {
  const normalized = item.label.toLowerCase();
  if (!site.features.catering && normalized.includes('cater')) return false;
  if (!site.features.savoryFood && normalized.includes('food')) return false;
  return true;
});

export const treatCategories: TreatCategory[] = site.treatCategories;
