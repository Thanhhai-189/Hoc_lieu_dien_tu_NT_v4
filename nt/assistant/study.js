(function () {
  'use strict';

  const glossaryRequest = /^(?:thuat ngu|tu vung|tra tu|dich|phat am|doc tu)\s+|\s+(?:(?:(?:dich|goi) )?sang (?:tieng anh|tieng viet)|(?:tieng anh|tieng viet) la gi)$/g;
  const definitionRequest = /^(?:cong dung|chuc nang|vai tro|nhiem vu|khai niem) (?:cua )?|\s+(?:la gi|dung de lam gi|co tac dung gi)$/g;

  function normalize(value) {
    return value.toLowerCase().normalize('NFD')
      .replace(/[\u0300-\u036f]/g, '').replace(/đ/g, 'd').replace(/×/g, 'x')
      .replace(/[^a-z0-9]+/g, ' ').trim();
  }

  function termQuery(value) {
    const query = normalize(value);
    return query.replace(glossaryRequest, '').replace(/\s+la gi$/, '').trim();
  }

  function create(course, corpus, glossary) {
    const terms = new Map();
    const choices = [];
    const seen = new Set();

    function addChoice(label, question, matches, selection = {}) {
      const key = normalize(label);
      if (!key || seen.has(key)) return;
      seen.add(key);
      const keys = [...new Set([key, ...matches.map(normalize)].filter(Boolean))];
      choices.push({key, keys, item: {label, question, ...selection}});
    }

    for (const card of glossary) terms.set(normalize(card.term), card);
    for (const card of glossary) {
      for (const alias of card.aliases) {
        const key = normalize(alias);
        if (key && !terms.has(key)) terms.set(key, card);
      }
    }
    for (const record of corpus.records) {
      if (record.kind !== 'topic') continue;
      addChoice(record.title, record.title, record.keywords || [], {topic: record.key});
    }
    for (const card of glossary) {
      addChoice(card.term, 'Thuật ngữ: ' + card.term, card.aliases, {card});
    }
    for (const lesson of Object.values(course.lessons)) {
      const label = `Bài ${lesson.code} · ${lesson.title}`;
      addChoice(label, 'Mở bài ' + lesson.code, [lesson.title, lesson.code, lesson.chapterTitle]);
    }
    for (const record of corpus.records) {
      if (record.kind === 'part' && record.title.length <= 64) {
        addChoice(record.title, record.title + ' trong bài ' + record.lesson, record.keywords || []);
      }
      const figure = record.figure;
      if (record.kind === 'figure' && figure?.number && figure.image) {
        const label = 'Hình ' + figure.number;
        addChoice(label, label, [figure.caption]);
      }
    }

    function findTerm(value) {
      const plain = normalize(value);
      const query = termQuery(value);
      if (!query) return null;
      const explicit = plain.replace(glossaryRequest, '').trim() !== plain;
      const card = terms.get(query) || terms.get(query.replace(definitionRequest, '').trim());
      if (!explicit && card?.lesson) return null;
      return card || null;
    }

    function suggest(value) {
      const input = normalize(value);
      const filter = termQuery(value);
      if (filter.length < 2 || filter.length > 65) return [];
      const onlyTerms = input.replace(glossaryRequest, '').trim() !== input;
      const hits = [];
      for (const {key: labelKey, item, keys} of choices) {
        if (onlyTerms && !item.card) continue;
        const score = keys.reduce((best, key) => {
          if (key === filter) return Math.max(best, 4);
          if (key.startsWith(filter)) return Math.max(best, 3);
          if (key.includes(' ' + filter)) return Math.max(best, 2);
          return best;
        }, 0);
        const priority = item.label === 'Hình ' + value.trim() ? 1 : labelKey === input ? .25 : 0;
        if (score) hits.push({item, score: score + priority + (item.topic && !onlyTerms ? .4 : 0)});
      }
      return hits.sort((a, b) => b.score - a.score || a.item.label.length - b.item.label.length)
        .slice(0, 5).map(hit => hit.item);
    }

    return {findTerm, suggest};
  }

  window.NTStudyCatalog = {create};
})();
