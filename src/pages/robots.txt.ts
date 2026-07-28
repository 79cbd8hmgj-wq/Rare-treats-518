import type { APIRoute } from "astro";
import { site } from "../data/content";

export const GET: APIRoute = ({ site: astroSite }) => {
  const base = astroSite?.toString().replace(/\/$/, "") ?? "https://rare-treats-518.pages.dev";
  const body = site.previewMode
    ? "User-agent: *\nDisallow: /\n"
    : `User-agent: *\nAllow: /\nSitemap: ${base}/sitemap.xml\n`;

  return new Response(body, {
    headers: { "Content-Type": "text/plain; charset=utf-8" }
  });
};
