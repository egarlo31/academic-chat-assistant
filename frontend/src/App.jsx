import { Fragment, useEffect, useMemo, useRef, useState } from 'react';

const API_BASE = import.meta.env.VITE_API_BASE_URL || '';
const STORAGE_KEY = 'academic-chat-assistant-history-v1';

const defaultMessages = [
  createMessage(
    'assistant',
    'Hola. Soy tu asistente académico para programación en C. ¿En qué te gustaría trabajar hoy?'
  ),
];

function createMessage(role, content) {
  return {
    id: `${role}-${Date.now()}-${Math.random().toString(16).slice(2)}`,
    role,
    content,
  };
}

function formatPrompt(prompt) {
  return `${prompt} Responde siempre con enfoque en lenguaje C, explica con claridad, usa ejemplos concretos y presenta la información con formato técnico limpio.`;
}

async function askAssistant(prompt) {
  const response = await fetch(`${API_BASE || ''}/api/v1/chat`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ message: prompt }),
  });

  const payload = await response.json().catch(() => ({}));

  if (!response.ok) {
    const detail = payload?.detail || 'No se pudo completar la solicitud.';
    throw new Error(typeof detail === 'string' ? detail : 'Error del asistente.');
  }

  if (!payload || typeof payload.answer !== 'string' || !payload.answer.trim()) {
    throw new Error('La respuesta recibida no tiene el formato esperado.');
  }

  return payload.answer.trim();
}

function renderInlineMarkdown(text) {
  if (!text) return null;

  const pattern = /(\*\*.*?\*\*|__.*?__|\*.*?\*|_.*?_|\[.*?\]\(.*?\)|`.*?`)/g;
  const segments = [];
  let lastIndex = 0;
  let match;

  while ((match = pattern.exec(text)) !== null) {
    if (match.index > lastIndex) {
      segments.push({ type: 'text', value: text.slice(lastIndex, match.index) });
    }

    const value = match[0];
    if (value.startsWith('**') || value.startsWith('__')) {
      segments.push({ type: 'strong', value: value.slice(2, -2) });
    } else if (value.startsWith('*') || value.startsWith('_')) {
      segments.push({ type: 'em', value: value.slice(1, -1) });
    } else if (value.startsWith('[') && value.includes('](')) {
      const linkText = value.slice(1, value.indexOf(']'));
      const href = value.slice(value.indexOf('(') + 1, -1);
      segments.push({ type: 'link', value: linkText, href });
    } else if (value.startsWith('`') && value.endsWith('`')) {
      segments.push({ type: 'code', value: value.slice(1, -1) });
    }

    lastIndex = match.index + value.length;
  }

  if (lastIndex < text.length) {
    segments.push({ type: 'text', value: text.slice(lastIndex) });
  }

  return (
    <>
      {segments.map((segment, index) => {
        if (segment.type === 'text') {
          return <Fragment key={`text-${index}`}>{segment.value}</Fragment>;
        }
        if (segment.type === 'strong') {
          return <strong key={`strong-${index}`}>{segment.value}</strong>;
        }
        if (segment.type === 'em') {
          return <em key={`em-${index}`}>{segment.value}</em>;
        }
        if (segment.type === 'link') {
          return (
            <a key={`link-${index}`} href={segment.href} target="_blank" rel="noreferrer">
              {segment.value}
            </a>
          );
        }
        return <code key={`code-inline-${index}`} className="inline-code">{segment.value}</code>;
      })}
    </>
  );
}

function renderMarkdown(content) {
  const lines = content.split('\n');
  const blocks = [];
  let paragraphBuffer = [];
  let listBuffer = [];
  let orderedBuffer = [];
  let codeBuffer = [];
  let codeLanguage = 'c';
  let inCodeBlock = false;
  let tableBuffer = [];
  let inTable = false;

  const pushParagraph = () => {
    if (!paragraphBuffer.length) return;
    blocks.push({ type: 'paragraph', value: paragraphBuffer.join(' ') });
    paragraphBuffer = [];
  };

  const pushList = () => {
    if (!listBuffer.length) return;
    blocks.push({ type: 'list', items: listBuffer });
    listBuffer = [];
  };

  const pushOrdered = () => {
    if (!orderedBuffer.length) return;
    blocks.push({ type: 'ordered-list', items: orderedBuffer });
    orderedBuffer = [];
  };

  const pushCodeBlock = () => {
    if (!codeBuffer.length) return;
    blocks.push({ type: 'code', value: codeBuffer.join('\n'), language: codeLanguage });
    codeBuffer = [];
    codeLanguage = 'c';
  };

  const pushTable = () => {
    if (!tableBuffer.length) return;

    const parsedRows = tableBuffer
      .map((row) => row.trim())
      .filter(Boolean)
      .map((row) => row.split('|').map((cell) => cell.trim()).filter((_, idx, arr) => !(idx === 0 && arr[0] === '') && !(idx === arr.length - 1 && arr[arr.length - 1] === '')));

    if (parsedRows.length >= 2) {
      const [header, separator, ...rows] = parsedRows;
      const hasSeparator = separator.every((cell) => /^:?-{3,}:?$/.test(cell));
      if (hasSeparator) {
        blocks.push({ type: 'table', header, rows });
        tableBuffer = [];
        inTable = false;
        return;
      }
    }

    const text = tableBuffer.join(' | ');
    blocks.push({ type: 'paragraph', value: text });
    tableBuffer = [];
    inTable = false;
  };

  for (let index = 0; index < lines.length; index += 1) {
    const line = lines[index];
    const trimmed = line.trim();

    if (trimmed.startsWith('```')) {
      pushParagraph();
      pushList();
      pushOrdered();
      pushTable();
      if (!inCodeBlock) {
        inCodeBlock = true;
        codeLanguage = trimmed.slice(3).trim() || 'c';
      } else {
        pushCodeBlock();
        inCodeBlock = false;
      }
      continue;
    }

    if (inCodeBlock) {
      codeBuffer.push(line);
      continue;
    }

    if (trimmed.startsWith('|') && trimmed.includes('|')) {
      const nextLine = lines[index + 1]?.trim() || '';
      const isTableSeparator = /^\|?\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)+\|?$/.test(nextLine);
      if (isTableSeparator || inTable) {
        inTable = true;
        tableBuffer.push(trimmed);
        if (!isTableSeparator && index === lines.length - 1) {
          pushTable();
        }
        continue;
      }
    }

    if (inTable) {
      pushTable();
    }

    if (!trimmed) {
      pushParagraph();
      pushList();
      pushOrdered();
      continue;
    }

    if (/^\s*[-*]\s+/.test(line)) {
      pushParagraph();
      pushOrdered();
      listBuffer.push(line.replace(/^\s*[-*]\s+/, '').trim());
      continue;
    }

    if (/^\s*\d+\.\s+/.test(line)) {
      pushParagraph();
      pushList();
      orderedBuffer.push(line.replace(/^\s*\d+\.\s+/, '').trim());
      continue;
    }

    if (/^\s*#+\s+/.test(line)) {
      pushParagraph();
      pushList();
      pushOrdered();
      blocks.push({ type: 'heading', value: line.replace(/^\s*#+\s+/, '').trim() });
      continue;
    }

    if (/^\s*>\s?/.test(line)) {
      pushParagraph();
      listBuffer.push(line.replace(/^\s*>\s?/, '').trim());
      continue;
    }

    paragraphBuffer.push(trimmed);
  }

  pushParagraph();
  pushList();
  pushOrdered();
  if (inCodeBlock) pushCodeBlock();
  if (inTable) pushTable();

  if (!blocks.length && paragraphBuffer.length) {
    blocks.push({ type: 'paragraph', value: paragraphBuffer.join(' ') });
  }

  return (
    <div className="markdown-content">
      {blocks.map((block, index) => {
        if (block.type === 'paragraph') {
          return (
            <p key={`paragraph-${index}`} className="md-paragraph">
              {renderInlineMarkdown(block.value)}
            </p>
          );
        }

        if (block.type === 'heading') {
          return (
            <h3 key={`heading-${index}`} className="md-heading">
              {renderInlineMarkdown(block.value)}
            </h3>
          );
        }

        if (block.type === 'list') {
          return (
            <ul key={`list-${index}`} className="md-list">
              {block.items.map((item, itemIndex) => (
                <li key={`${item}-${itemIndex}`}>{renderInlineMarkdown(item)}</li>
              ))}
            </ul>
          );
        }

        if (block.type === 'ordered-list') {
          return (
            <ol key={`ordered-${index}`} className="md-ordered-list">
              {block.items.map((item, itemIndex) => (
                <li key={`${item}-${itemIndex}`}>{renderInlineMarkdown(item)}</li>
              ))}
            </ol>
          );
        }

        if (block.type === 'table') {
          const { header, rows } = block;
          return (
            <div key={`table-${index}`} className="md-table-wrap">
              <table className="md-table">
                <thead>
                  <tr>
                    {header.map((cell, cellIndex) => (
                      <th key={`th-${cellIndex}`}>{renderInlineMarkdown(cell)}</th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {rows.map((row, rowIndex) => (
                    <tr key={`tr-${rowIndex}`}>
                      {row.map((cell, cellIndex) => (
                        <td key={`td-${rowIndex}-${cellIndex}`}>{renderInlineMarkdown(cell)}</td>
                      ))}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          );
        }

        return (
          <pre key={`code-${index}`} className="md-code-block">
            <code>{block.value}</code>
          </pre>
        );
      })}
    </div>
  );
}

export default function App() {
  const [messages, setMessages] = useState(defaultMessages);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [notice, setNotice] = useState('');
  const messagesEndRef = useRef(null);

  const examplePrompts = useMemo(
    () => [
      'Explica qué es un puntero en C y cómo se usa.',
      '¿Cómo se usa malloc para reservar memoria dinámica en C?',
      'Explica la diferencia entre printf y scanf en C.',
      '¿Qué significa un segmentation fault en C?',
    ],
    []
  );

  useEffect(() => {
    try {
      const stored = localStorage.getItem(STORAGE_KEY);
      if (stored) {
        const parsed = JSON.parse(stored);
        if (Array.isArray(parsed) && parsed.length > 0) {
          setMessages(parsed);
          return;
        }
      }
    } catch {
      // Si el almacenamiento está bloqueado o contiene datos inválidos, se usa el chat inicial.
    }

    setMessages(defaultMessages);
  }, []);

  useEffect(() => {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(messages));
    } catch {
      // El chat sigue funcionando aunque el navegador impida el almacenamiento local.
    }
  }, [messages]);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, loading]);

  const canSend = input.trim().length > 0 && !loading;

  const appendMessage = (role, content) => {
    setMessages((prev) => [...prev, createMessage(role, content)]);
  };

  const handleResetChat = () => {
    setMessages(defaultMessages);
    setError('');
    setNotice('El chat se reinició correctamente.');
    setTimeout(() => setNotice(''), 1800);
  };

  const handleCopy = async (content) => {
    try {
      await navigator.clipboard.writeText(content);
      setNotice('Respuesta copiada al portapapeles.');
      setTimeout(() => setNotice(''), 1800);
    } catch {
      setError('No fue posible copiar la respuesta.');
    }
  };

  const handleComposerKeyDown = (event) => {
    if ((event.ctrlKey || event.metaKey) && event.key === 'Enter') {
      event.preventDefault();
      event.currentTarget.form?.requestSubmit();
    }
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    const trimmed = input.trim();
    if (!trimmed || loading) return;

    setLoading(true);
    setError('');
    setNotice('');
    appendMessage('user', trimmed);
    setInput('');

    try {
      const answer = await askAssistant(formatPrompt(trimmed));
      appendMessage('assistant', answer);
    } catch (err) {
      const message = err.message || 'Ocurrió un error inesperado.';
      setError(message);
      appendMessage('assistant', 'No pude responder tu pregunta en este momento. Revisa que el backend esté levantado y que la API esté disponible.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-shell">
      <header className="topbar">
        <div className="brand-block">
          <p className="eyebrow">Academic Chat Assistant</p>
          <h1>Asistente académico en C</h1>
        </div>

        <button type="button" className="ghost-button" onClick={handleResetChat}>
          Reiniciar chat
        </button>
      </header>

      <main className="chat-panel">
        <section className="chat-column">
          <div className="messages" aria-live="polite">
            {messages.map((message) => (
              <div key={message.id} className={`message-row ${message.role}`}>
                <div className="avatar">{message.role === 'user' ? 'Tú' : 'AI'}</div>

                <div className="bubble-wrap">
                  <div className="bubble">
                    <div className="message-role">
                      {message.role === 'user' ? 'Usuario' : 'Asistente'}
                    </div>
                    {message.role === 'assistant' ? renderMarkdown(message.content) : (
                      <div className="message-content plain-user-message">{message.content}</div>
                    )}
                  </div>

                  {message.role === 'assistant' && (
                    <div className="message-actions">
                      <button
                        type="button"
                        aria-label="Copiar respuesta al portapapeles"
                        onClick={() => handleCopy(message.content)}
                      >
                        Copiar
                      </button>
                    </div>
                  )}
                </div>
              </div>
            ))}

            {loading && (
              <div className="message-row assistant">
                <div className="avatar">AI</div>
                <div className="bubble typing">
                  <span />
                  <span />
                  <span />
                </div>
              </div>
            )}

            <div ref={messagesEndRef} />
          </div>

          {error && <div className="error-banner" role="alert">{error}</div>}
          {notice && <div className="notice-banner" role="status">{notice}</div>}

          <div className="prompt-suggestions" aria-label="Preguntas sugeridas">
            {examplePrompts.map((prompt) => (
              <button key={prompt} type="button" className="prompt-chip" onClick={() => setInput(prompt)}>
                {prompt}
              </button>
            ))}
          </div>

          <form onSubmit={handleSubmit} className="composer">
            <textarea
              aria-label="Pregunta sobre programación en C"
              value={input}
              onChange={(event) => setInput(event.target.value)}
              onKeyDown={handleComposerKeyDown}
              placeholder="Escribe tu duda sobre C..."
              rows={4}
              disabled={loading}
            />

            <div className="composer-actions">
              <span className="helper-text">Enfoque actual: lenguaje C · Ctrl/Cmd + Enter para enviar</span>
              <button type="submit" disabled={!canSend}>
                {loading ? 'Enviando...' : 'Enviar'}
              </button>
            </div>
          </form>
        </section>
      </main>
    </div>
  );
}
