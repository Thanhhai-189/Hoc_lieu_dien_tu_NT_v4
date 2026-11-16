(function (global) {
  'use strict';

  const ALIASES = [
    [/\ba\s+b\s+s\b|\banti lock braking system\b|\bchong (?:bo|ham|khoa) cung (?:banh(?: xe)?|phanh)\b|\bchong khoa banh(?: xe)?\b/g, 'abs'],
    [/\bcardan\b|\bcac dang\b|\bcat dang\b/g, 'cac_dang'],
    [/\bli hop\b|\bly hop\b|\bbo con\b|\bcon xe\b|\bclutch\b/g, 'ly_hop'],
    [/\bhop so (?:vo cap|bien thien lien tuc)\b|\bc v t\b/g, 'cvt'],
    [/\bhop so (?:2|hai) truc\b/g, 'hop_so_hai_truc'],
    [/\bhop so (?:3|ba) truc\b/g, 'hop_so_ba_truc'],
    [/\bban truc\b|\bhalf shaft\b/g, 'ban_truc'],
    [/\bphanh hoi\b|\bphanh khi nen\b/g, 'phanh khi_nen'],
    [/\bphanh dau\b|\bphanh thuy luc\b/g, 'phanh thuy_luc'],
    [/\bkhi nen\b/g, 'khi_nen'],
    [/\bthuy luc\b/g, 'thuy_luc'],
    [/\bbo vi sai\b|\bvi sai\b|\bdifferential\b/g, 'vi_sai'],
    [/\bcam bien\b|\bsensor\b/g, 'cam_bien'],
    [/\btoc do banh xe\b|\bwheel speed\b/g, 'toc_do_banh'],
    [/\bxa ap\b|\bgiam ap\b/g, 'giam_ap'],
    [/\bgiu ap\b/g, 'giu_ap'],
    [/\btang ap\b/g, 'tang_ap'],
    [/\bhe so truot\b|\bdo truot\b/g, 'he_so_truot'],
    [/\bgiam xoc\b|\bgiam chan\b/g, 'giam_chan'],
    [/\bong don\b|\bmonotube\b/g, 'ong_don'],
    [/\bong kep\b|\bong doi\b|\b(?:2|hai) ong\b|\btwin tube\b/g, 'ong_kep'],
    [/\bsteer by wire\b|\blai khong truc lai\b/g, 'sbw'],
    [/\bcan bang dong\b|\bcan bang banh xe\b/g, 'can_bang_banh'],
    [/\bmo men\b|\bmomen\b|\bmomem\b/g, 'mo_men'],
    [/\bxi lanh\b|\bxy lanh\b|\bxylanh\b/g, 'xi_lanh'],
    [/\bpit tong\b|\bpiston\b/g, 'pit_tong'],
    [/\bmoay o\b|\bmoayo\b/g, 'moay_o'],
    [/\bpuly\b|\bpulley\b/g, 'puli'],
    [/\boto\b|\bo to\b/g, 'o_to'],
    [/\bti so\b|\bty so\b/g, 'ty_so'],
    [/\btua bin\b|\bturbine\b/g, 'tua_bin'],
    [/\bchu thap\b/g, 'chu_thap'],
    [/\bdong toc\b/g, 'dong_toc'],
    [/\bthung ben\b|\bnang ha thung xe\b/g, 'nang_ha_thung'],
  ];
  const STOP = new Set(('a ai ban bat bao bay ben bi bo cac cai cau cho co cung cua da dang day de den dieu do doc dong duoc dung em gia gi giua giai hai hay hien hoi hoc hieu khi khong kia lam la len loai luc ma minh mot moi nao nay neu nhu nhung noi o qua ra roi rang rat sau se su theo thi thao thanh the thich toi tro tren trong tu ung va vao ve vi voi vay xong yeu y xin xem chi tim gium giup sao ne nha noi chung co ban tai sao vi sao nhat thoi nhieu it so thieu thuoc xuat tat ca het them').split(' '));
  const INTENT_WORDS = new Set(('cong dung chuc nang nhiem vu cau tao thanh phan nguyen ly hoat dong nguyen tac bo phan chi tiet qua trinh tac dung khai niem giai thich hinh bang so sanh su khac nhau phan biet buoc muc dich tong quan tom tat noi dung de cap trinh bay mo ta che do').split(' '));
  const REFUSAL = 'Tôi chưa tìm được đoạn đủ căn cứ trong học liệu. Bạn có thể bổ sung tên hệ thống, tên chi tiết hoặc mã bài để tôi tra lại.';
  const WRONG_DOMAIN = /\b(?:thu do|(?:dia diem|di|tour|lich trinh) du lich|du lich o dau|tho tiet|thoi tiet|cong thuc nau|nau an|bai tho|bong da|co phieu|mat khau|system prompt|ignore previous|bo qua huong dan|bo qua chi dan|hack|viet code|viet ma python|o_to bay)\b/;
  const SERVICE_SPEC = /\b(?:mo_men siet|luc siet|siet bao nhieu|ma phu tung|ma linh kien|ma loi obd|ma loi dtc|luong dau can do|(?:khi nao|bao lau|dinh ky|chu ky) (?:can )?thay (?:dau|nhot))\b|\b(?:dau boi tron|dau hop so|dau cau|nhot hop so)\b.*\b(?:sae|gl ?[45]|chuan gi|loai nao)\b/;
  const SERVICE_ACTION = /\b(?:vo hieu hoa|cach sua|sua (?:the nao|lam sao|o dau|chua)|cach khac phuc|khac phuc (?:the nao|lam sao)|thay the (?:the nao|lam sao))\b/;
  const UNDERSPECIFIED = /^(?:(?:cho (?:toi|em|minh) biet|xin hoi|giai thich) )?(?:che do|loai|cai) nao (?:tot nhat|phu hop nhat|nen dung)$/;
  const LOCAL_REFERENCE = /\b(?:(?:trong )?bai (?:nay|(?:dang )?(?:mo|hoc|doc))|(?:noi dung|hinh) nay)\b/g;
  const PRESSURE_LABELS = {tang_ap: 'Tăng áp', giu_ap: 'Giữ áp', giam_ap: 'Giảm áp'};
  const SHORT_PRESSURE = {tang: 'tang_ap', giu: 'giu_ap', giam: 'giam_ap', xa: 'giam_ap'};
  const PHASE_CLAUSE = /\b(?:tang_ap|giu_ap|giam_ap)\b/g;
  const QUESTION_QUANTITY = /\b(?:bao nhieu|may vong|may lan|bao lau|bao xa)\b/;

  function folded(value) {
    return String(value || '').toLowerCase().normalize('NFD')
      .replace(/[\u0300-\u036f]/g, '').replace(/đ/g, 'd').replace(/×/g, 'x');
  }

  function normalize(value) {
    let text = folded(value).replace(/[^a-z0-9_]+/g, ' ').trim().replace(/\s+/g, ' ');
    for (const [pattern, replacement] of ALIASES) text = text.replace(pattern, replacement);
    return text;
  }

  function terms(normalized) {
    return normalized.split(' ').filter(word => word.length > 1 && !STOP.has(word) && !/^\d+$/.test(word));
  }

  function distinct(items) {
    return [...new Set(items)];
  }

  function phraseIn(text, phrase) {
    return Boolean(phrase) && ` ${text} `.includes(` ${phrase} `);
  }

  function headingFor(source) {
    if (source.title.length <= 120) return source.title;
    const prefix = source.title.match(/^Hình\s+\d+\.\d+[a-z]?/i);
    return prefix ? prefix[0] : source.title.slice(0, 116).replace(/\s+\S*$/, '') + '…';
  }

  function frequency(list) {
    const result = new Map();
    for (const word of list) result.set(word, (result.get(word) || 0) + 1);
    return result;
  }

  function pagesText(pages) {
    const groups = [];
    for (const page of distinct(pages || []).sort((a, b) => a - b)) {
      const group = groups.at(-1);
      if (group && group[1] + 1 === page) group[1] = page;
      else groups.push([page, page]);
    }
    return groups.map(([from, to]) => from === to ? String(from) : `${from}–${to}`).join(', ');
  }

  function create(course, corpus) {
    const lessons = course.lessons;
    const topics = new Map();
    const topicLabels = new Map();
    const knownFigures = new Map();
    const byLesson = new Map();
    const df = new Map();
    const index = [];
    const lessonVocabulary = new Map(Object.values(lessons).map(lesson =>
      [lesson.code, new Set(terms(normalize(`${lesson.chapterTitle} ${lesson.title}`)))]));
    for (const source of corpus.records) {
      if (!Object.hasOwn(lessons, source.lesson)) continue;
      const title = normalize(source.title);
      const keywords = (source.keywords || []).map(normalize).filter(Boolean);
      const titleTerms = new Set(terms([title, ...keywords].join(' ')));
      const bodyTerms = frequency(terms(normalize(source.text)));
      const lessonTerms = lessonVocabulary.get(source.lesson);
      const vocabulary = new Set([...titleTerms, ...bodyTerms.keys(), ...lessonTerms]);
      for (const term of vocabulary) df.set(term, (df.get(term) || 0) + 1);
      const labels = [title, ...keywords].map(value => [value, terms(value).length]);
      const entry = {source, title, labels, titleTerms, bodyTerms, lessonTerms, length: bodyTerms.size};
      index.push(entry);
      if (!byLesson.has(source.lesson)) byLesson.set(source.lesson, []);
      byLesson.get(source.lesson).push(entry);
      if (source.key) {
        topics.set(source.key, source);
        topicLabels.set(source.key, labels);
      }
      const figure = source.figure;
      if (figure?.number && figure.image) {
        const previous = knownFigures.get(figure.number);
        if (!previous || source.pages?.length) knownFigures.set(figure.number, figure);
      }
    }
    const averageLength = index.reduce((sum, entry) => sum + entry.length, 0) / index.length;
    const idf = word => Math.log(1 + (index.length + .5) / ((df.get(word) || 0) + .5));
    const technicalTerms = new Set(index.flatMap(entry => [...entry.titleTerms]).filter(word => !INTENT_WORDS.has(word)));

    function classify(query) {
      return {
        definition: /\b(?:la gi|cong dung|chuc nang|nhiem vu|dung de|vai tro|muc dich)\b/.test(query),
        operation: /\b(?:nguyen ly|lam viec|hoat dong|duong truyen|trinh tu|cac buoc|giam_ap|tang_ap|giu_ap)\b/.test(query),
        structure: /\b(?:cau tao|gom|thanh phan|bo phan|chi tiet|ket cau)\b/.test(query),
        comparison: /\b(?:so sanh|phan biet|khac nhau|giong nhau|khac gi|khac voi)\b/.test(query),
        figure: /\b(?:hinh|so do|anh minh hoa|vi tri)\b/.test(query),
        overview: /\b(?:tom tat|tong quan|noi ve|hoc gi|noi dung chinh)\b/.test(query),
      };
    }

    function findTopics(query) {
      return [...topics.values()].map(source => {
        const entry = topicLabels.get(source.key);
        const matches = entry.filter(([label]) => phraseIn(query, label));
        return {source, strength: Math.max(0, ...matches.map(([, length]) => length))};
      }).filter(hit => hit.strength > 0).sort((a, b) => b.strength - a.strength);
    }

    function sourceList(records) {
      const keys = new Set();
      return records.filter(record => {
        const key = `${record.lesson}|${(record.pages || []).join(',')}|${record.anchor || ''}`;
        if (keys.has(key)) return false;
        keys.add(key);
        return true;
      }).slice(0, 4);
    }

    function answerFrom(records, settings = {}) {
      const first = records[0];
      const citations = sourceList(records);
      const context = settings.context || {
        lesson: first.lesson,
        topic: first.key || '',
        label: first.title,
      };
      const related = (first.more || []).map(key => topics.get(key)).filter(Boolean);
      if (!first.more && citations.length) {
        related.push(...[...topics.values()].filter(source => source.id !== first.id && source.lesson === first.lesson).slice(0, 3));
      }
      const suggestions = related.map(source => ({
        label: source.title,
        question: source.title,
        topic: source.key,
      }));
      const figure = first.figure?.image ? first.figure : knownFigures.get(first.figureNumber || first.figure?.number);
      return {
        type: 'answer', title: settings.title || headingFor(first),
        paragraphs: settings.paragraphs || [first.text],
        sources: citations,
        context, suggestions: suggestions.slice(0, 3),
        figure: settings.figure ? figure : null,
        excerpt: first.kind === 'pdf' || first.kind === 'html',
      };
    }

    function rank(query, queryTerms, options) {
      const {lesson, chapter, current, intent} = options;
      const results = [];
      const weighted = queryTerms.map(word => [word, idf(word)]);
      const totalWeight = weighted.reduce((sum, [, weight]) => sum + weight, 0);
      for (const entry of lesson ? byLesson.get(lesson) || [] : index) {
        const source = entry.source;
        if (chapter && lessons[source.lesson].chapter !== chapter) continue;
        let score = 0;
        let covered = 0;
        let substantive = 0;
        for (const [term, weight] of weighted) {
          const count = entry.bodyTerms.get(term) || 0;
          const title = entry.titleTerms.has(term);
          const lessonTitle = entry.lessonTerms.has(term);
          if (!count && !title && !lessonTitle) continue;
          covered += weight;
          if (count || title) substantive += 1;
          if (title) score += 2.9 * weight;
          if (lessonTitle) score += .63 * weight;
          if (count) score += weight * count * 2.25 / (count + 1.25 * (.3 + .7 * entry.length / averageLength));
        }
        if (!substantive && !lesson && !entry.labels.some(([label]) => label === query)) continue;
        const coverage = totalWeight ? covered / totalWeight : 1;
        score *= .45 + .55 * coverage;
        let longest = 0;
        for (const [label, length] of entry.labels) {
          if (length > longest && phraseIn(query, label)) longest = length;
        }
        if (longest > 0) score += 6 + Math.min(6, longest * 1.8);
        if (longest && source.kind === 'part' && intent.definition && phraseIn(query, entry.title)) score += 15;
        if (source.kind === 'topic' && longest) score += 7;
        if (source.kind === 'note') score *= 1.14;
        if (source.kind === 'lesson') score *= .56;
        if (source.kind === 'figure' && !intent.figure && !intent.structure) score *= .70;
        if (intent.operation && source.kind === 'simulation') score *= 1.35;
        if (intent.structure && (source.kind === 'figure' || source.kind === 'part')) score *= 1.27;
        if (intent.definition && source.kind === 'topic') score *= 1.13;
        if (source.lesson === current) score += 1.25;
        results.push({source, score, coverage, substantive, longest});
      }
      return results.sort((a, b) => b.score - a.score);
    }

    function comparison(query, topicHits, chapter) {
      const byKey = key => topics.get(key);
      let pairs = topicHits.map(hit => hit.source);
      if (phraseIn(query, 'abs') && phraseIn(query, 'ebd')) pairs = [byKey('abs'), byKey('ebd')];
      if (phraseIn(query, 'eps') && phraseIn(query, 'sbw')) pairs = [byKey('eps'), byKey('sbw')];
      if (phraseIn(query, 'ong_don') && phraseIn(query, 'ong_kep')) pairs = [byKey('monotube'), byKey('twintube')];
      if (phraseIn(query, 'abs') && phraseIn(query, 'khi_nen') && phraseIn(query, 'thuy_luc')) {
        pairs = [byKey('abs-oil'), byKey('abs-air')];
      } else if (!phraseIn(query, 'abs') && phraseIn(query, 'phanh khi_nen') && phraseIn(query, 'phanh thuy_luc')) {
        pairs = [byKey('air-brake'), byKey('hydraulic-brake')];
      }
      pairs = pairs.filter(source => source && (!chapter || lessons[source.lesson].chapter === chapter)).slice(0, 2);
      if (pairs.length !== 2) return null;
      return answerFrom(pairs, {
        title: 'Đối chiếu hai nội dung',
        paragraphs: pairs.map(source => `${source.title}. ${source.text}`),
      });
    }

    function findFigure(number, current) {
      const hits = index.filter(({source}) => source.kind === 'figure' && source.figure?.number === number);
      hits.sort((a, b) => (Number(Boolean(b.source.figure.image)) - Number(Boolean(a.source.figure.image))) * 3
        + Number(Boolean(b.source.pages)) - Number(Boolean(a.source.pages))
        + Number(b.source.lesson === current) - Number(a.source.lesson === current));
      if (!hits.length) {
        return {type: 'missing', title: `Hình ${number}`, paragraphs: [REFUSAL]};
      }
      const best = hits[0].source;
      const detail = hits.find(entry => entry.source.pages?.length)?.source;
      return answerFrom(detail ? [best, detail] : [best], {figure: true});
    }

    function relatedFigure(source, current) {
      const number = source.figureNumber || source.figure?.number;
      if (number) {
        const result = findFigure(number, current || source.lesson);
        if (result.type === 'answer') return result;
      }
      if (source.figure?.image) return answerFrom([source], {figure: true});
      const figure = (byLesson.get(source.lesson) || []).find(entry => entry.source.kind === 'figure' && entry.source.figure?.image);
      return figure ? answerFrom([figure.source], {figure: true}) : answerFrom([source]);
    }

    function lessonOverview(code) {
      const lesson = lessons[code];
      const subjects = lesson.simulations.map(sim => sim.title);
      const paragraphs = lesson.objectives.filter(text => !text.startsWith('Nhận diện và gọi đúng'));
      if (subjects.length) paragraphs.push('Các mục nguyên lý trong bài gồm ' + subjects.join(' và ') + '.');
      return {
        type: 'answer',
        title: 'Nội dung chính · ' + lesson.title,
        paragraphs: paragraphs.length ? paragraphs : ['Mở bài để xem hình minh họa và các hoạt động.'],
        sources: [{lesson: code}],
        suggestions: [
          {label: 'Xem nguyên lý', question: 'Nguyên lý bài ' + code},
          {label: 'Xem hình trong bài', question: 'Hình trong bài ' + code},
        ],
      };
    }

    function pressureAnswer(key, phase, showFigure) {
      const source = topics.get(key);
      const detail = source.phases?.[phase];
      if (!detail) return answerFrom([source], {figure: showFigure});
      const system = key === 'abs-air' ? 'ABS khí nén' : 'ABS thủy lực';
      const result = answerFrom([source], {
        title: PRESSURE_LABELS[phase] + ' · ' + system,
        paragraphs: [detail], figure: showFigure,
      });
      result.suggestions = [{label: 'Xem đủ ba chế độ', question: source.title, topic: source.key}, ...result.suggestions].slice(0, 3);
      return result;
    }

    function answer(question, {currentLesson = '', context = null, topic = ''} = {}) {
      const raw = String(question || '').trim().slice(0, 600);
      const query = normalize(raw);
      const intent = classify(query);
      if (topic && topics.has(topic)) return answerFrom([topics.get(topic)]);
      if (/^(?:xin )?chao(?: ban| tro ly)?$|^(?:cam on|thanks|hello|hi)$/.test(query)) {
        return {type: 'info', title: 'Trợ lý tra cứu', paragraphs: ['Bạn có thể hỏi về một chi tiết, nguyên lý làm việc hoặc yêu cầu mở hình theo số hiệu.']};
      }
      if (!query || WRONG_DOMAIN.test(query)) return {type: 'missing', title: 'Tra cứu học liệu', paragraphs: [REFUSAL]};
      if (SERVICE_ACTION.test(query)) {
        return {type: 'missing', title: 'Tra cứu trong phạm vi học liệu',
          paragraphs: ['Học liệu trình bày cấu tạo và nguyên lý làm việc. Để chẩn đoán, sửa chữa hoặc thay đổi hệ thống trên xe, hãy dùng tài liệu bảo dưỡng đúng mẫu xe.']};
      }
      if (SERVICE_SPEC.test(query)) {
        return {type: 'missing', title: 'Thông số theo mẫu xe', paragraphs: ['Tôi chưa xác nhận được trị số theo mẫu xe từ nguồn học liệu. Cần tài liệu kỹ thuật đúng mẫu xe và cụm chi tiết để tra thông số này.']};
      }
      if (UNDERSPECIFIED.test(query)) {
        return {type: 'info', title: 'Bạn muốn so sánh nội dung nào?',
          paragraphs: ['Nêu tên hệ thống và các phương án cần so sánh, ví dụ giảm chấn ống đơn và ống kép.']};
      }
      const pdfNumber = query.match(/\b(?:trang|tr) (?:pdf )?(\d{1,4})\b/)?.[1];
      if (pdfNumber && /\b(?:tap (?:2|hai)|pdf)\b/.test(query)) {
        const page = Number(pdfNumber);
        if (page >= 1 && page <= corpus.pdfPages) {
          return {type: 'page', title: 'Tập 2 · Trang PDF ' + page, pdfPage: page, paragraphs: []};
        }
        return {type: 'missing', title: 'Trang PDF Tập 2',
          paragraphs: [`Tập 2 có ${corpus.pdfPages} trang PDF. Hãy nhập số trang trong khoảng đó.`]};
      }
      const numberText = folded(raw);
      const figureNumber = numberText.match(/\bhinh\s+(\d{1,2}\.\d{1,3}[a-z]?)\b(?!\.\d)|^(\d{1,2}\.\d{1,3}[a-z]?)$/);
      if (figureNumber) return findFigure(figureNumber[1] || figureNumber[2], currentLesson);

      const code = raw.match(/\b\d{1,2}\.\d{1,2}\.\d{1,2}\b/)?.[0];
      if (code && !Object.hasOwn(lessons, code)) {
        return {type: 'missing', title: `Bài ${code}`, paragraphs: ['Mục lục hiện có 102 bài. Tôi chưa tìm thấy mã bài này.']};
      }
      const chapterText = query.match(/\bchuong\s+(\d{1,2})\b/)?.[1];
      const chapter = chapterText ? Number(chapterText) : null;
      if (chapter && !Object.hasOwn(course.chapters, chapter)) {
        return {type: 'missing', title: 'Mục lục học liệu', paragraphs: ['Học liệu có 12 chương. Bạn có thể nhập số chương từ 1 đến 12.']};
      }
      if (code && /^(?:(?:mo|xem|den) )?(?:bai )?\d+ \d+ \d+$/.test(query)) {
        const lesson = lessons[code];
        return {type: 'answer', title: `Bài ${code} · ${lesson.title}`,
          paragraphs: ['Mở bài học để đọc nội dung, xem hình và làm các hoạt động.'],
          sources: [{lesson: code}]};
      }
      const scopedQuery = query.replace(LOCAL_REFERENCE, ' ').replace(/\s+/g, ' ').trim();
      const localReference = scopedQuery !== query;
      const queryTerms = distinct(terms(scopedQuery.replace(/\b(?:bai|chuong)\b/g, ' ')));
      const relevant = queryTerms.filter(word => !INTENT_WORDS.has(word));
      if (chapter && !code && relevant.every(word => ['mo', 'danh', 'sach', 'muc', 'luc'].includes(word))) {
        return {type: 'chapter', title: `Chương ${chapter} · ${course.chapters[chapter]}`,
          paragraphs: ['Mở chương để xem các bài học và nội dung tương tác.'], chapter};
      }
      const hits = findTopics(query).filter(hit => (!code || hit.source.lesson === code)
        && (!chapter || lessons[hit.source.lesson].chapter === chapter));
      if (intent.comparison && !code && !localReference) {
        const result = comparison(query, hits, chapter);
        if (result) return result;
      }
      if (!localReference && !code && (!chapter || chapter === 6) && phraseIn(query, 'chu_thap') && phraseIn(query, 'dong_toc')) {
        return answerFrom([topics.get('constant-velocity')], {figure: intent.figure});
      }
      if (!localReference && !code && (!chapter || chapter === 6) && /\b(?:cac_dang|nang)\b/.test(query) && /\bdung pha\b/.test(query)) {
        return answerFrom([topics.get('constant-velocity')], {figure: intent.figure});
      }
      if (!localReference && !code && (!chapter || chapter === 7) && /\b(?:quay vong|khi re|vao cua)\b/.test(query)
        && (/\bbanh trong\b/.test(query) && /\bbanh ngoai\b/.test(query)
          || /\bhai banh\b.*\b(?:khac toc do|chenh lech toc do)\b/.test(query))) {
        return answerFrom([topics.get('differential')], {figure: intent.figure});
      }
      const previousTopic = context?.topic ? topics.get(context.topic) : null;
      const referenceToPrevious = /^(?:con |the con )|\b(?:no|cai do|he thong nay|phan tren)\b/.test(query);
      const shortPhase = query.match(/^(?:(?:luc|khi|con|the con) )?(?:che do )?(tang|giu|giam|xa)(?: (?:thi )?(?:the nao|sao|lam sao|nhu the nao))?$/)?.[1];
      const phases = distinct(query.match(PHASE_CLAUSE) || []);
      const phase = phases.length === 1 ? phases[0] : SHORT_PRESSURE[shortPhase];
      const hydraulic = /\b(?:thuy_luc|dau phanh)\b/.test(query);
      const absFollowup = phase || phases.length || hydraulic || /\b(?:che do ap suat|he_so_truot|khi_nen)\b/.test(query);
      const absContext = previousTopic?.lesson === '10.3.5' && (previousTopic.key.startsWith('abs') || previousTopic.key === 'wheel-sensor');
      const absMentioned = phraseIn(query, 'abs');
      const otherTopic = hits.some(hit => hit.source.lesson !== '10.3.5');
      const absFromLesson = currentLesson === '10.3.5' && Boolean(phase || phraseIn(query, 'he_so_truot'));
      const absScope = (!localReference || currentLesson === '10.3.5') && (!code || code === '10.3.5') && (!chapter || chapter === 10);
      if (absScope && (absMentioned || !otherTopic && (absContext || absFromLesson)) && absFollowup) {
        const slip = phraseIn(query, 'he_so_truot') || /\b(?:tan so|lan giay)\b/.test(query);
        const air = phraseIn(query, 'khi_nen') || previousTopic?.key === 'abs-air' && !hydraulic;
        if (slip) return answerFrom([topics.get('abs-slip')], {figure: intent.figure});
        if (phase && !air && !hydraulic && previousTopic?.key !== 'abs-oil') {
          return pressureChoices(phase);
        }
        return pressureAnswer(air ? 'abs-air' : 'abs-oil', phase, intent.figure);
      }
      if (absScope && absMentioned && /\b(?:tan so|lan giay|quang duong)\b/.test(query)) {
        return answerFrom([topics.get('abs-slip')], {figure: intent.figure});
      }
      if (previousTopic?.key === 'tipper' && shortPhase && !absMentioned && !code && !chapter && !localReference) {
        return answerFrom([previousTopic]);
      }
      if (!absMentioned && !absContext && !absFromLesson && !code && !hits.length && phase
        && (shortPhase || relevant.length <= 2)) {
        return pressureChoices(phase);
      }
      if (previousTopic && referenceToPrevious && !code && !chapter && hits.length === 0 && relevant.length < 4) {
        return intent.figure ? relatedFigure(previousTopic, currentLesson) : answerFrom([previousTopic]);
      }

      const lesson = code || (localReference ? currentLesson : '');
      if (localReference && !lesson) {
        return {type: 'info', title: 'Chọn bài học',
          paragraphs: ['Mở bài cần tra cứu hoặc nhập mã bài, ví dụ Bài 10.3.5.']};
      }
      if (lesson && !relevant.filter(word => !['nay', 'dang', 'mo', 'dung', 'giang'].includes(word)).length) {
        if (intent.overview && !intent.figure && !intent.operation && !intent.structure) return lessonOverview(lesson);
        const records = (byLesson.get(lesson) || []).map(entry => entry.source);
        const wanted = intent.figure ? 'figure' : intent.structure ? 'figure' : intent.operation ? 'simulation' : 'topic';
        const source = records.find(record => record.kind === wanted && (!intent.figure || record.figure?.image))
          || records.find(record => record.kind === 'simulation') || records[0];
        if (source) return intent.figure ? relatedFigure(source, currentLesson) : answerFrom([source]);
      }
      const exact = !lesson && hits.find(hit => topicLabels.get(hit.source.key).some(([label]) => label === query));
      if (exact && !queryTerms.some(word => !INTENT_WORDS.has(word))) {
        return answerFrom([exact.source], {figure: intent.figure});
      }
      if (!lesson && !chapter && /^(?:dong co|may dong luc)(?: la gi)?$/.test(query)) {
        return answerFrom([topics.get('engine-purpose')]);
      }
      if (!lesson && !exact && !relevant.some(word => technicalTerms.has(word) || df.has(word) && idf(word) > 2.25)) {
        return {type: 'missing', title: 'Tra cứu học liệu', paragraphs: [REFUSAL]};
      }

      const results = rank(query, queryTerms, {lesson, chapter, current: currentLesson, intent});
      let best = results.find(hit => hit.source.kind !== 'lesson') || results[0];
      if (hits.length && !lesson && !chapter) {
        const specific = exact || hits.find(hit => hit.strength >= 2 || relevant.length <= 2
          || absMentioned && hit.source.key === 'abs' && !intent.structure);
        const candidate = specific && results.find(hit => hit.source.id === specific.source.id);
        if (candidate && (exact || !best || candidate.score > best.score * .65)) best = candidate;
      }
      if (QUESTION_QUANTITY.test(query) && (!best || !best.longest && best.coverage < .8)) {
        return {type: 'missing', title: 'Chưa đủ dữ kiện để xác định',
          paragraphs: ['Hãy nêu đại lượng cần tính và điều kiện đang xét. Có thể nhập mã bài để tìm công thức hoặc ví dụ.']};
      }
      const minCoverage = relevant.length >= 3 ? .59 : .47;
      if (!best || (!best.longest && (best.coverage < minCoverage || best.score < 6))) {
        return {type: 'missing', title: 'Tra cứu học liệu', paragraphs: [REFUSAL]};
      }
      const first = best.source;
      return intent.figure ? relatedFigure(first, currentLesson) : answerFrom([first]);
    }

    function pressureChoices(phase) {
      return {type: 'info', title: 'Chọn sơ đồ ABS cần tra cứu',
        paragraphs: ['Bạn đang hỏi về điều áp ABS thủy lực hay ABS khí nén?'],
        suggestions: [
          {label: 'ABS thủy lực', question: PRESSURE_LABELS[phase] + ' ABS thủy lực'},
          {label: 'ABS khí nén', question: PRESSURE_LABELS[phase] + ' ABS khí nén'},
        ]};
    }

    return {answer, pagesText};
  }

  global.NTAssistantSearch = {create, normalize, pagesText};
  if (typeof module === 'object' && module.exports) module.exports = global.NTAssistantSearch;
})(typeof window === 'undefined' ? globalThis : window);
