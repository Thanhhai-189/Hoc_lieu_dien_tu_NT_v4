(function () {
  'use strict';

  const course = window.OTO_ALL_DATA;
  if (!course) return;

  const assets = 'nt/assistant/';
  const compactLayout = matchMedia('(max-width: 620px)');
  const top = document.querySelector('#nt-chat-top');
  const SVG = {
    chat: '<path d="M20 11.5a7.8 7.8 0 0 1-8.2 7.4c-1.1 0-2.1-.2-3-.5L4 20l1.3-3.8a7 7 0 0 1-1.5-4.7A7.8 7.8 0 0 1 12 4.1a7.8 7.8 0 0 1 8 7.4Z"/><path d="M8 11.7h.01m4 0h.01m4 0h.01" stroke-width="2.6"/>',
    clear: '<path d="M6 7h12M10 4h4m3 3-.8 13H7.8L7 7m3 3v6m4-6v6"/>',
    down: '<path d="m6 9 6 6 6-6"/>',
    send: '<path d="m4 4 16 8-16 8 3-8-3-8Zm3 8h13"/>',
  };
  const promptSuggestions = [
    'ABS hoạt động như thế nào?',
    'So sánh phanh khí nén và phanh thủy lực',
    'Thuật ngữ: Common rail',
  ];
  let searchPromise;
  let search;
  let studyCatalog;
  let searchLoading = false;
  let conversation = 0;
  let context = null;
  let lastFocus = null;
  let inertElements = [];
  let suggestionChoices = [];
  let suggestionIndex = -1;

  function el(tag, className = '', value = '') {
    const node = document.createElement(tag);
    if (className) node.className = className;
    if (value) node.textContent = value;
    return node;
  }

  function icon(name) {
    const node = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
    node.setAttribute('viewBox', '0 0 24 24');
    node.setAttribute('aria-hidden', 'true');
    node.innerHTML = SVG[name];
    return node;
  }

  function button(className, label, symbol = '') {
    const node = el('button', className);
    node.type = 'button';
    if (symbol) {
      node.append(icon(symbol));
      node.setAttribute('aria-label', label);
      node.title = label;
    } else node.textContent = label;
    return node;
  }

  function link(label, href, external = false) {
    const node = el('a', '', label);
    node.href = href;
    if (external) {
      node.target = '_blank';
      node.rel = 'noopener noreferrer';
    }
    return node;
  }

  function useAssistantImage(container) {
    const image = el('img', 'nt-chat-assistant-image');
    image.alt = '';
    image.addEventListener('load', () => container.replaceChildren(image), {once: true});
    image.src = assets + 'AI_VKB.png';
  }

  const launch = button('nt-chat-launch', 'Mở Trợ lý tra cứu', 'chat');
  useAssistantImage(launch);
  launch.id = 'nt-chat-launch';
  launch.setAttribute('aria-expanded', 'false');
  launch.setAttribute('aria-controls', 'nt-chat');
  launch.setAttribute('aria-haspopup', 'dialog');
  const scrim = button('nt-chat-scrim', 'Đóng Trợ lý tra cứu');
  scrim.textContent = '';
  scrim.tabIndex = -1;
  scrim.hidden = true;
  scrim.setAttribute('aria-hidden', 'true');
  const panel = el('section', 'nt-chat');
  panel.id = 'nt-chat';
  panel.hidden = true;
  panel.setAttribute('role', 'dialog');
  panel.setAttribute('aria-labelledby', 'nt-chat-title');

  const header = el('header', 'nt-chat-header');
  const headerIcon = el('span', 'nt-chat-header-icon');
  headerIcon.append(icon('chat'));
  useAssistantImage(headerIcon);
  const heading = el('div', 'nt-chat-heading');
  const title = el('h2', '', 'Trợ lý tra cứu');
  title.id = 'nt-chat-title';
  heading.append(title, el('p', 'nt-chat-status', 'Học tập ngoại tuyến · Theo học liệu'));
  const reset = button('nt-chat-icon-btn', 'Bắt đầu cuộc trò chuyện mới', 'clear');
  const close = button('nt-chat-icon-btn', 'Thu gọn Trợ lý tra cứu', 'down');
  header.append(headerIcon, heading, reset, close);

  const history = el('div', 'nt-chat-history');
  history.tabIndex = 0;
  history.setAttribute('role', 'log');
  history.setAttribute('aria-label', 'Cuộc trò chuyện');
  history.setAttribute('aria-live', 'polite');
  history.setAttribute('aria-relevant', 'additions text');

  const composer = el('div', 'nt-chat-composer');
  const suggestions = el('ul', 'nt-chat-autocomplete');
  suggestions.id = 'nt-chat-autocomplete';
  suggestions.hidden = true;
  suggestions.setAttribute('role', 'listbox');
  suggestions.setAttribute('aria-label', 'Gợi ý tra cứu');
  const form = el('form', 'nt-chat-form');
  const hint = el('div', 'nt-chat-hint');
  hint.hidden = true;
  hint.setAttribute('role', 'status');
  const input = el('input');
  input.id = 'nt-chat-question';
  input.type = 'text';
  input.placeholder = 'Hỏi về một nội dung trong bài…';
  input.autocomplete = 'off';
  input.maxLength = 600;
  input.setAttribute('aria-label', 'Câu hỏi tra cứu');
  input.setAttribute('role', 'combobox');
  input.setAttribute('aria-autocomplete', 'list');
  input.setAttribute('aria-controls', suggestions.id);
  input.setAttribute('aria-expanded', 'false');
  const submit = button('nt-chat-send', 'Gửi câu hỏi', 'send');
  submit.type = 'submit';
  form.append(input, submit);
  composer.append(hint, suggestions, form);
  panel.append(header, history, composer);
  document.body.append(scrim, launch, panel);

  function currentLesson() {
    const code = new URLSearchParams(location.hash.slice(1)).get('lesson');
    return code && Object.hasOwn(course.lessons, code) ? code : '';
  }

  function loadScript(file) {
    return new Promise((resolve, reject) => {
      const script = el('script');
      script.src = assets + file;
      script.onload = () => { script.remove(); resolve(); };
      script.onerror = () => { script.remove(); reject(new Error(file)); };
      document.head.append(script);
    });
  }

  function prepareSearch() {
    if (!searchPromise) {
      searchPromise = Promise.all([
        window.NTAssistantSearch || loadScript('retrieval.js'),
        window.NT_ASSISTANT_CORPUS || loadScript('corpus.js'),
        window.NTStudyCatalog || loadScript('study.js'),
        window.NT_STUDY_GLOSSARY || loadScript('study-glossary.js'),
      ]).then(() => {
        search = window.NTAssistantSearch.create(course, window.NT_ASSISTANT_CORPUS);
        studyCatalog = window.NTStudyCatalog.create(course, window.NT_ASSISTANT_CORPUS, window.NT_STUDY_GLOSSARY);
      }).catch(error => {
        searchPromise = null;
        throw error;
      });
    }
    return searchPromise;
  }

  function showAnswer(answer) {
    if (panel.hidden || !answer) return;
    const top = answer.getBoundingClientRect().top - history.getBoundingClientRect().top;
    history.scrollTop += top - 12;
  }

  function setModalState() {
    for (const element of inertElements) element.inert = false;
    inertElements = [];
    const modal = !panel.hidden && compactLayout.matches;
    scrim.hidden = !modal;
    if (modal) {
      panel.setAttribute('aria-modal', 'true');
      for (const node of document.body.children) {
        if (node !== panel && node !== scrim && node instanceof HTMLElement && !node.inert) {
          node.inert = true;
          inertElements.push(node);
        }
      }
    } else panel.removeAttribute('aria-modal');
  }

  function openPanel() {
    if (panel.hidden) {
      lastFocus = document.activeElement;
      panel.hidden = false;
      launch.setAttribute('aria-expanded', 'true');
      launch.setAttribute('aria-label', 'Thu gọn Trợ lý tra cứu');
      setModalState();
      showAnswer([...history.querySelectorAll('.nt-chat-answer')].at(-1));
      prepareSearch().then(() => {
        if (document.activeElement === input) updateSuggestions();
      }).catch(() => {});
    }
    input.focus({preventScroll: true});
  }

  function closePanel(returnFocus = true) {
    if (panel.hidden) return;
    panel.hidden = true;
    launch.setAttribute('aria-expanded', 'false');
    launch.setAttribute('aria-label', 'Mở Trợ lý tra cứu');
    // top.setAttribute('aria-expanded', 'false');
    clearSuggestions();
    setModalState();
    if (returnFocus) (lastFocus?.isConnected ? lastFocus : launch).focus({preventScroll: true});
  }

  function appendSuggestions(items) {
    if (!items.length) return;
    const group = el('div', 'nt-chat-suggestions');
    for (const item of items) {
      const choice = button('', item.label || item);
      choice.addEventListener('click', () => ask(item.question || item, item));
      group.append(choice);
    }
    history.append(group);
  }

  function clearSuggestions() {
    suggestionChoices = [];
    suggestionIndex = -1;
    suggestions.hidden = true;
    suggestions.replaceChildren();
    input.setAttribute('aria-expanded', 'false');
    input.removeAttribute('aria-activedescendant');
  }

  function updateSuggestions() {
    clearSuggestions();
    if (!studyCatalog || panel.hidden || document.activeElement !== input) return;
    suggestionChoices = studyCatalog.suggest(input.value);
    if (!suggestionChoices.length) return;
    suggestionChoices.forEach((item, i) => {
      const choice = el('li', '', item.label);
      choice.id = 'nt-chat-option-' + i;
      choice.setAttribute('role', 'option');
      choice.setAttribute('aria-selected', 'false');
      choice.addEventListener('pointerdown', event => event.preventDefault());
      choice.addEventListener('click', () => ask(item.question, item));
      suggestions.append(choice);
    });
    suggestions.hidden = false;
    input.setAttribute('aria-expanded', 'true');
  }

  function moveSuggestion(step) {
    const length = suggestionChoices.length;
    suggestionIndex = suggestionIndex === -1 ? (step === 1 ? 0 : length - 1)
      : (suggestionIndex + step + length) % length;
    Array.from(suggestions.children).forEach((node, i) => {
      node.setAttribute('aria-selected', String(i === suggestionIndex));
    });
    const active = suggestions.children[suggestionIndex];
    input.setAttribute('aria-activedescendant', active.id);
    active.scrollIntoView({block: 'nearest'});
  }

  function welcome() {
    const intro = el('div', 'nt-chat-welcome');
    intro.append(el('p', '', 'Nhập câu hỏi, mã bài, số hiệu hình hoặc thuật ngữ...'));
    intro.append(link('Hướng dẫn tra cứu ↗', assets + 'huong-dan.html', true));
    history.replaceChildren(intro);
    const prompts = [...promptSuggestions];
    const code = currentLesson();
    if (code) prompts.unshift({label: 'Nội dung bài đang học', question: `Tóm tắt bài ${code}`});
    appendSuggestions(prompts);
  }

  function openSource(event) {
    if (event.button || event.metaKey || event.ctrlKey || event.altKey || event.shiftKey) return;
    if (compactLayout.matches) {
      closePanel(false);
      document.querySelector('#main').focus({preventScroll: true});
    }
  }

  function appendSources(container, sources) {
    if (!sources?.length) return;
    const block = el('div', 'nt-chat-sources');
    block.append(el('b', '', 'Nguồn trong học liệu'));
    for (const source of sources) {
      const lesson = course.lessons[source.lesson];
      const row = el('div', 'nt-chat-source-row');
      const label = `Bài ${lesson.code} · ${lesson.title}`;
      const target = link(label, `#lesson=${encodeURIComponent(lesson.code)}`);
      target.addEventListener('click', openSource);
      row.append(target);
      if (source.kind === 'html' || source.anchor) {
        const anchor = source.anchor ? `#${encodeURIComponent(source.anchor)}` : '';
        row.append(link('Mở đoạn gốc ↗', `${lesson.file}${anchor}`, true));
      }
      if (source.pages?.length) {
        row.append(pdfLink(source.pages[0], `Tập 2 · PDF tr. ${search.pagesText(source.pages)} ↗`));
      }
      block.append(row);
    }
    container.append(block);
  }

  function pdfLink(page, label) {
    return link(label, `nt/tai-lieu-tap2-2026.pdf#page=${page}`, true);
  }

  function appendAnswer(answer) {
    const bubble = el('section', 'nt-chat-answer');
    const first = answer.sources?.[0];
    if (first) {
      const lesson = course.lessons[first.lesson];
      const label = answer.excerpt ? 'Trích đoạn học liệu' : `Chương ${lesson.chapter} · ${lesson.chapterTitle}`;
      bubble.append(el('p', 'nt-chat-meta', label));
    }
    bubble.append(el('h3', '', answer.title));
    for (const text of answer.paragraphs) bubble.append(el('p', '', text));
    if (answer.pdfPage) bubble.append(pdfLink(answer.pdfPage, 'Mở trang PDF ↗'));
    if (answer.chapter) {
      const chapterLink = link('Xem toàn chương →', `#chapter=${answer.chapter}`);
      chapterLink.addEventListener('click', openSource);
      bubble.append(chapterLink);
    }
    if (answer.figure?.image) {
      const figure = el('figure', 'nt-chat-figure');
      const imageLink = link('', answer.figure.image, true);
      const image = el('img');
      image.src = answer.figure.image;
      image.alt = answer.figure.caption;
      imageLink.setAttribute('aria-label', 'Phóng to ' + answer.figure.caption);
      imageLink.append(image);
      figure.append(imageLink, el('figcaption', '', answer.figure.caption));
      bubble.append(figure);
    }
    appendSources(bubble, answer.sources);
    history.append(bubble);
    appendSuggestions(answer.suggestions || []);
    return bubble;
  }

  function addPronunciation(container, term) {
    if (!('speechSynthesis' in window) || !('SpeechSynthesisUtterance' in window)) return;
    const speak = button('nt-chat-link-button', 'Nghe phát âm');
    const message = el('span', 'nt-chat-meta');
    message.setAttribute('role', 'status');
    speak.addEventListener('click', () => {
      const synthesis = window.speechSynthesis;
      // Chỉ chọn giọng cài trên thiết bị để hoạt động ngoại tuyến.
      const voice = synthesis.getVoices().find(voice => voice.localService && /^en\b/i.test(voice.lang));
      if (!voice) {
        message.textContent = 'Chưa có giọng tiếng Anh cài trên máy.';
        return;
      }
      synthesis.cancel();
      const utterance = new SpeechSynthesisUtterance(term);
      utterance.voice = voice;
      utterance.lang = voice.lang;
      utterance.rate = .9;
      utterance.onerror = event => {
        if (event.error !== 'canceled' && event.error !== 'interrupted') {
          message.textContent = 'Trình duyệt chưa phát được âm thanh.';
        }
      };
      message.textContent = '';
      synthesis.speak(utterance);
    });
    container.append(speak, message);
  }

  function appendGlossary(card) {
    const bubble = el('section', 'nt-chat-answer nt-chat-glossary');
    bubble.append(el('p', 'nt-chat-meta', 'Thuật ngữ Việt–Anh'), el('h3', '', card.term));
    if (card.ipa) bubble.append(el('p', 'nt-chat-ipa', card.ipa));
    const audio = el('div', 'nt-chat-audio');
    addPronunciation(audio, card.term);
    if (audio.childElementCount) bubble.append(audio);
    if (card.image) {
      const image = el('img', 'nt-chat-glossary-image');
      image.src = card.image;
      image.alt = 'Minh họa ' + card.term;
      image.loading = 'lazy';
      image.addEventListener('error', () => image.remove(), {once: true});
      bubble.append(image);
    }
    const definitions = el('dl');
    const english = el('dd', '', card.en);
    english.lang = 'en';
    definitions.append(el('dt', '', 'Tiếng Việt'), el('dd', '', card.vi), el('dt', '', 'English'), english);
    bubble.append(definitions);
    bubble.append(el('p', 'nt-chat-meta', 'Nguồn: Bộ thuật ngữ đính kèm.'));
    if (card.lesson) {
      const target = link('Bài liên quan ' + card.lesson + ' · ' + course.lessons[card.lesson].title,
        '#lesson=' + encodeURIComponent(card.lesson));
      target.addEventListener('click', openSource);
      bubble.append(target);
    }
    history.append(bubble);
    return bubble;
  }

  async function ask(value, choice = {}) {
    const question = String(value || '').trim().slice(0, 600);
    if (!question || searchLoading) return;
    clearSuggestions();
    input.value = '';
    input.focus({preventScroll: true});
    submit.disabled = true;
    const currentConversation = conversation;
    if (!search) {
      searchLoading = true;
      hint.textContent = 'Đang mở dữ liệu học liệu…';
      hint.hidden = false;
      try {
        await prepareSearch();
      } catch (_) {
        if (currentConversation !== conversation) return;
        showAnswer(appendAnswer({title: 'Chưa tải được dữ liệu tra cứu',
          paragraphs: ['Kiểm tra đã giải nén toàn bộ học liệu rồi gửi lại câu hỏi.']}));
        if (!input.value) input.value = question;
        return;
      } finally {
        searchLoading = false;
        hint.hidden = true;
        submit.disabled = !input.value.trim();
      }
    }
    if (currentConversation !== conversation) return;
    while (history.childElementCount > 72) history.firstElementChild.remove();
    history.append(el('div', 'nt-chat-user', question));
    const card = choice.card || (!choice.topic && studyCatalog.findTerm(question));
    if (card) {
      context = null;
      showAnswer(appendGlossary(card));
      return;
    }
    const result = search.answer(question, {currentLesson: currentLesson(), context, topic: choice.topic || ''});
    if (result.type === 'missing' && result.title === 'Tra cứu học liệu' && !choice.topic) {
      const fallbackCard = studyCatalog.findTerm(question);
      if (fallbackCard) {
        context = null;
        showAnswer(appendGlossary(fallbackCard));
        return;
      }
    }
    if (result.context || result.type === 'answer' || result.type === 'chapter' || result.type === 'page') {
      context = result.context || null;
    }
    showAnswer(appendAnswer(result));
  }

  launch.addEventListener('click', () => panel.hidden ? openPanel() : closePanel());
  close.addEventListener('click', () => closePanel());
  scrim.addEventListener('click', () => closePanel());
  reset.addEventListener('click', () => {
    conversation++;
    context = null;
    input.value = '';
    submit.disabled = true;
    hint.hidden = true;
    clearSuggestions();
    welcome();
    input.focus({preventScroll: true});
  });
  input.addEventListener('input', () => {
    submit.disabled = searchLoading || !input.value.trim();
    updateSuggestions();
  });
  input.addEventListener('focus', updateSuggestions);
  input.addEventListener('blur', clearSuggestions);
  input.addEventListener('keydown', event => {
    if (!suggestionChoices.length || event.isComposing) return;
    if (event.key === 'Escape') {
      event.stopPropagation();
      clearSuggestions();
    } else if (event.key === 'ArrowDown' || event.key === 'ArrowUp') {
      event.preventDefault();
      moveSuggestion(event.key === 'ArrowDown' ? 1 : -1);
    } else if (event.key === 'Enter' && suggestionIndex >= 0) {
      event.preventDefault();
      const choice = suggestionChoices[suggestionIndex];
      ask(choice.question, choice);
    }
  });
  form.addEventListener('submit', event => { event.preventDefault(); ask(input.value); });
  compactLayout.addEventListener('change', setModalState);
  panel.addEventListener('keydown', event => {
    if (event.key === 'Escape') {
      event.preventDefault();
      closePanel();
    }
    if (event.key !== 'Tab' || !compactLayout.matches) return;
    const targets = [...panel.querySelectorAll('a[href], button, input, [tabindex="0"]')]
      .filter(node => !node.disabled && !node.closest('[hidden]'));
    const first = targets[0];
    const last = targets.at(-1);
    if (event.shiftKey && document.activeElement === first) { event.preventDefault(); last.focus(); }
    if (!event.shiftKey && document.activeElement === last) { event.preventDefault(); first.focus(); }
  });
  window.addEventListener('hashchange', () => {
    context = null;
    if (!history.querySelector('.nt-chat-user')) welcome();
  });
  document.addEventListener('click', event => {
    if (event.target.closest('[data-open-nt-assistant]')) openPanel();
  });
  submit.disabled = true;
  welcome();
})();
