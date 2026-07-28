export function normalizeCopy(value) {
  return value
    .replace(/[’‘]/g, "'")
    .replace(/\s+/g, " ")
    .trim()
    .toLowerCase();
}

export function findVoiceViolations(content, forbiddenPhrases) {
  const normalizedContent = normalizeCopy(content);

  return forbiddenPhrases.filter((phrase) =>
    normalizedContent.includes(normalizeCopy(phrase))
  );
}
