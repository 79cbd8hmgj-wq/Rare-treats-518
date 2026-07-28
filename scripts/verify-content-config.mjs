import fs from 'node:fs';
import path from 'node:path';

const launchMode = process.argv.includes('--launch');
const contentPath = path.resolve('content/site.json');
const site = JSON.parse(fs.readFileSync(contentPath, 'utf8'));
const errors = [];
const warnings = [];

if (!site.business?.name) errors.push('business.name is required');
if (!site.business?.ownerName) errors.push('business.ownerName is required');
if (!site.business?.instagramUrl) errors.push('business.instagramUrl is required');
if (!Array.isArray(site.navigation) || site.navigation.length === 0) errors.push('navigation must contain public routes');
if (!Array.isArray(site.treatCategories) || site.treatCategories.length < 3) errors.push('at least three treat categories are required');

if (site.features?.catering !== false) errors.push('catering must remain disabled for the current website direction');
if (site.features?.savoryFood !== false) errors.push('savoryFood must remain disabled for the current website direction');
if (site.navigation.some((item) => /cater|savory|food/i.test(`${item.label} ${item.href}`))) {
  errors.push('public navigation must not expose catering or savory food while those features are disabled');
}

if (!site.features?.onlineOrdering) warnings.push('online ordering is disabled');
if (!site.business?.publicEmail) warnings.push('public business email is not confirmed');
if (!site.markets?.confirmedEvents?.length) warnings.push('no confirmed market dates are published');
if (site.policies?.status !== 'approved') warnings.push('policies remain in draft status');

if (launchMode) {
  const launchChecks = site.launch ?? {};
  for (const [key, value] of Object.entries(launchChecks)) {
    if (value !== true) errors.push(`launch requirement not complete: ${key}`);
  }
  if (!site.business.publicEmail && !site.business.publicPhone) errors.push('at least one official public contact method is required for launch');
  if (site.policies?.status !== 'approved') errors.push('policies.status must be approved for launch');
}

for (const warning of warnings) console.warn(`WARNING: ${warning}`);
if (errors.length) {
  for (const error of errors) console.error(`ERROR: ${error}`);
  process.exit(1);
}
console.log(launchMode ? 'Launch content validation passed.' : 'Foundation content validation passed.');
